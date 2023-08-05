import enum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    no_type_check,
)

from pydantic import Field as PydanticField
from pydantic.fields import FieldInfo, ModelField
from pydantic.fields import Undefined as _PydanticUndefinedInstance
from pydantic.json import ENCODERS_BY_TYPE
from pydantic.main import ModelMetaclass
from pydantic.typing import resolve_annotations
from typing_extensions import ClassVar, Type, get_args, get_origin

from ts_ids_core.annotations import DictStrAny, Required
from ts_ids_core.errors import (
    InvalidConstField,
    InvalidField,
    InvalidNonMandatoryField,
    MultipleTypesError,
    UndefinedTypeError,
)


class IdsFieldCategory(enum.Flag):
    """
    Indicate the type of an IDS field defined
    """

    NULLABLE = enum.auto()
    REQUIRED = enum.auto()


T = TypeVar("T")


class IdsUndefinedType:
    """
    Placeholder indicating that the the value of the `IdsElement` field is unknown or
    non-existent.

    This is distinct from the `IdsElement`'s field being `None`.

    This was partially copied from `pydantic.UndefinedType`. It intentionally does not
    inherit from `pydantic.UndefinedType` so that it fails `isinstance` and
    `issubclass` checks.
    """

    #: An instance's 'type' in JSON Schema.
    JSON_SCHEMA_TYPE = "Undefined"

    def __repr__(self) -> str:
        return "IdsUndefined"

    def __reduce__(self) -> str:
        """Enable pickling this instance."""
        return self.JSON_SCHEMA_TYPE

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[..., Any], None, None]:
        """
        Yield functions that `pydantic` calls during type validation.

        This method must be implemented so `BaseModel` fields can have `IdsUndefinedType`
        type.

        See [the pydantic documentation](https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types)
        for more info on custom `pydantic` field types.
        """
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> "IdsUndefinedType":
        """
        Assert that the value is an instance of this class.

        This method is boilerplate for custom `pydantic` field types.
        """
        if isinstance(value, cls):
            return value

        raise UndefinedTypeError()

    @classmethod
    def __modify_schema__(cls, field_schema):
        """
        Return the schema representation of this instance.

        When `pydantic` converts this class to JSON Schema via `IdsElement.schema`,
        an empty dictionary is passed in to `field_schema`. Otherwise, if `field_schema`
        remains empty, `pydantic.schema.field_singleton_schema` fails.

        See the [pydantic docs](https://pydantic-docs.helpmanual.io/usage/schema/#modifying-schema-in-custom-fields)
        for further info.
        """
        field_schema["type"] = cls.JSON_SCHEMA_TYPE


#: A workaround to prevent `IdsUndefinedType` from breaking `IdsElement.schema`.
ENCODERS_BY_TYPE[IdsUndefinedType] = lambda _: "IdsUndefined"


#: Sentinel indicating that a field's value is unknown or irrelevant. This is distinct
#: from a field being NULL (`None`).
IDS_UNDEFINED = IdsUndefinedType()
#: By default, `pydantic` passes `default=PYDANTIC_UNDEFINED` to the `Field` function
#: and the `FieldInfo` constructor.
PYDANTIC_UNDEFINED = _PydanticUndefinedInstance


class RawPydanticField(NamedTuple):
    """
    :ivar name:
        The field name.
    :ivar raw_type_hint:
        The type annotation in the class definition -- i.e. the value associated with
        the field in `__annotations__`.
    :ivar raw_value:
        The value that the field is assigned in the class definition. For example,
        consider the following class,

        ```python
        from pydantic import BaseModel

        class MyClass(BaseModel):
            foo: str = IdsField()
            bar: str
            baz: str = "BAZ"
        ```

        The `raw_value` of `foo` is the return value of `IdsField()`.

        `bar` is only present in the `__annotations__` of the class and its
        `raw_value` should be `IDS_UNDEFINED`.

        The `raw_value` associated with the `baz` field should be `"BAZ"`.
    """

    name: str
    raw_type_hint: Type
    raw_value: Any = IDS_UNDEFINED


class ProcessedField(NamedTuple):
    """
    `IdsElement` fields and metadata converted to the form used by `IdsElement`.

    :ivar name:
        The name of the field.
    :ivar category:
        The type of the IDS field. See `IdsFieldCategory` for details.
    :ivar type_hint:
        The type annotation of the field.
    :ivar field_info:
        The `FieldInfo` created using the `name`, `category` and `type_hint` values.
    """

    name: str
    category: IdsFieldCategory
    type_hint: Type
    field_info: FieldInfo


def _separate_required_nullable_type_hints(
    field_type_hint: Type, category: IdsFieldCategory = IdsFieldCategory(0)
) -> Tuple[Type, IdsFieldCategory]:
    """
    Implementation of `separate_required_nullable_type_hints` called recursively.

    See `separate_required_nullable_type_hints` for details.
    """
    origin = get_origin(field_type_hint)
    if origin is Required:
        field_subtype = get_args(field_type_hint)[0]
        category |= IdsFieldCategory.REQUIRED
        return _separate_required_nullable_type_hints(field_subtype, category)
    if origin is Union:
        field_subtypes = set(get_args(field_type_hint))
        if type(None) in field_subtypes:
            category |= IdsFieldCategory.NULLABLE
        else:
            raise MultipleTypesError()
        # Instead of using an `if` statement, first add `type(None)` such that it's
        # guaranteed to be in `field_subtypes`. Then, remove it such that the only
        # remaining type is non-NULL.
        field_subtypes.add(type(None))
        field_subtypes.remove(type(None))
        non_null_subtype = field_subtypes.pop()
        return _separate_required_nullable_type_hints(non_null_subtype, category)
    return field_type_hint, category


def separate_required_nullable_type_hints(
    field_type_hint: Type,
) -> Tuple[Type, IdsFieldCategory]:
    """
    Remove `Required` and `Nullable` from a type hint.

    Note that generics e.g. `Dict` and `Tuple` are not inspected for `Nullable` and
    `Required` types. Thus, `Required` and `Nullable` are only removed from the
    top-level type hint.

    :param field_type_hint:
        The type hint from which to remove `Required` and `Nullable`.
    :return:
        The updated type hint and whether the type hint is `Required` and/or
        `Nullable`, indicated by the `IdsFieldCategory` enum.
    """
    stripped_type_hint, type_category = _separate_required_nullable_type_hints(
        field_type_hint, category=IdsFieldCategory(0)
    )
    return stripped_type_hint, type_category


def _validate_raw_value(raw_value: Any) -> None:
    """
    Some values can be assigned to `pydantic.BaseModel` fields but not to those of IDS
    Schema classes. This function validates that `raw_value` can be used by
    IDS Schema -- i.e. the `IdsElement` class.

    :param raw_value:
        The value assigned to the field in the class definition. See the documentation
        for `RawPydanticField.raw_value` for a more detailed description.
    :raise InvalidField:
        If the value of `raw_value` cannot be parsed into an IDS field.
    """
    if raw_value is Ellipsis:
        raise InvalidField(
            "Whether a field is required should be set via the `Required` type hint, "
            "not using an ellipsis."
        )
    if isinstance(raw_value, FieldInfo) and "required" in raw_value.extra:
        raise InvalidField(
            "Whether a field is required should be set via the `Required` type hint, "
            "not by setting `required`."
        )


def process_raw_field(
    field: RawPydanticField,
) -> ProcessedField:
    """
    Convert the field definition in the class namespace to that usable by `IdsElement`.

    :param field:
        The field in the class definition.

        The attributes of `field` are as follows:

        `name`:
            The name of the variable to which the field is bound.
        `raw_type_hint`:
            The field's type annotation, processed in such a way as to be usable by
            `IdsElement`.
        `raw_value`:
            The value assigned to the field prior to processing. See the documentation
            of `RawPydanticField.raw_value` for a more detailed description. If a field
            is defined only by a type hint, `raw_value` should be `IDS_UNDEFINED`.
    :return:
        The processed field.
    """
    _validate_raw_value(field.raw_value)
    stripped_type_hint, category = separate_required_nullable_type_hints(
        field.raw_type_hint
    )

    field_info = field.raw_value
    if not isinstance(field_info, FieldInfo):
        field_info = IdsField(default=field.raw_value)

    if category & IdsFieldCategory.REQUIRED:
        field_info.extra["required"] = True
    else:
        field_info.extra["required"] = False

    processed_type_hint = stripped_type_hint
    # Required, Nullable
    if category is (IdsFieldCategory.NULLABLE | IdsFieldCategory.REQUIRED):
        processed_type_hint = Union[stripped_type_hint, None]
    elif category is IdsFieldCategory.NULLABLE:  # not Required, Nullable
        processed_type_hint = Union[processed_type_hint, IdsUndefinedType, None]
    elif category is ~(
        IdsFieldCategory.NULLABLE | IdsFieldCategory.REQUIRED
    ):  # not Required, not Nullable
        processed_type_hint = Union[processed_type_hint, IdsUndefinedType]

    # Note: Required, not Nullable type hint does not need to be updated.

    return ProcessedField(
        name=field.name,
        category=category,
        type_hint=processed_type_hint,
        field_info=field_info,
    )


NON_FIELD_TYPES = (Callable, property, staticmethod, classmethod, type)


def _is_raw_pydantic_field(annotation: Type, field_name: str, raw_value: Any) -> bool:
    """
    Return whether the item in the class namespace is a `pydantic.BaseModel` field.
    """
    if get_origin(annotation) is ClassVar:
        return False
    if field_name.startswith("__"):
        return False
    if isinstance(raw_value, NON_FIELD_TYPES):
        return False
    return True


def get_raw_pydantic_fields(namespace: DictStrAny) -> List[RawPydanticField]:
    """
    Return the `pydantic` fields in a Python class' namespace.

    :param namespace:
        The namespace of a Python class. This the `namespace` argument typically passed
        to `type.__new__(mcs, name, bases, namespace, **kwargs)`.
    :return:
        The list of `pydantic` fields from the namespace.
    """
    ids_class_type_hints = namespace.get("__annotations__", dict())
    ids_class_module_name = namespace.get("__module__", None)
    # Resolve forward references.
    original_annotations = resolve_annotations(
        raw_annotations=ids_class_type_hints, module_name=ids_class_module_name
    )
    return [
        RawPydanticField(
            name=field_name,
            raw_type_hint=annotation,
            raw_value=namespace.get(
                field_name, RawPydanticField._field_defaults["raw_value"]
            ),
        )
        for field_name, annotation in original_annotations.items()
        if _is_raw_pydantic_field(
            annotation, field_name, namespace.get(field_name, IDS_UNDEFINED)
        )
    ]


class IdsFieldInheritanceType(enum.IntFlag):
    MANDATORY = enum.auto()
    NON_MANDATORY = enum.auto()

    ANY_INHERITANCE_TYPE = MANDATORY | NON_MANDATORY


def set_inheritance_type(
    field: FieldInfo,
    *,
    mandatory: Optional[bool] = None,
    type_: Optional[IdsFieldInheritanceType] = None,
) -> None:
    """
    Set whether the Field has Mandatory or Non-Mandatory inheritance.

    :param field:
        The Field to update.
    :param mandatory:
        If `True`, the Field will have Mandatory inheritance. Otherwise, if `False`,
        the Field will have Non Mandatory inheritance.
    :param type_:
        Set the inheritance type `type_`. If `type_` is
        `IdsFieldInheritanceType.ANY_INHERITANCE_TYPE`, set to Mandatory inheritance.
    :return:
        None. `field` is modified in-place.
    """
    if not (mandatory is None) ^ (type_ is None):
        raise ValueError("Exactly one of `mandatory` and `type_` must be non-null.")
    if mandatory is not None:
        field.extra["inheritance_type"] = (
            IdsFieldInheritanceType.MANDATORY
            if mandatory
            else IdsFieldInheritanceType.NON_MANDATORY
        )
    else:
        field.extra["inheritance_type"] = type_


def has_mandatory_inheritance(field: ModelField) -> bool:
    """Return whether the Field is inherited by child classes."""
    return bool(
        field.field_info.extra["inheritance_type"] & IdsFieldInheritanceType.MANDATORY
    )


def IdsField(
    default: Any = IDS_UNDEFINED, *, mandatory_inheritance: bool = True, **kwargs
) -> FieldInfo:
    """
    Wrap the `pydantic.Field` function such that, fields default to a sentinel value for
    undefined (a.k.a. unknown or missing) values. As such, the field definition is
    compatible with schema defined using `ts_ids_core.schema.base.IdsElement`.

    :param default:
        The default value to use for the field. Default set to a global instance of
        `IdsUndefinedType` that's intended to be used as a singleton.
    :param mandatory_inheritance:
        Set whether the resulting FieldInfo has Mandatory or Non-Mandatory inheritance.
    :param kwargs:
        All other keyword arguments are passed to `pydantic.Field`.
    :return:
        The resulting `FieldInfo` produced by `pydantic.Field`.
    """
    if "default_factory" in kwargs and default is not IDS_UNDEFINED:
        raise ValueError("Cannot specify both `default` and `default_factory`.")
    if "const" in kwargs and kwargs["const"] and default is IDS_UNDEFINED:
        raise InvalidConstField(
            "`const` fields must set a default value. If the intent is to create an "
            "abstract field, pass in `default=NotImplemented`."
        )
    if "default_factory" in kwargs:
        # If the default value is set via default_factory, use `pydantic` behavior.
        field = PydanticField(**kwargs)
    else:
        field = PydanticField(default=default, **kwargs)
    set_inheritance_type(field, mandatory=mandatory_inheritance)
    return field


class IdsModelMetaclass(ModelMetaclass):
    """A Pydantic ModelMetaclass with modified behavior for required and
    nullable fields.

    To define an IDS schema, inherit from the `ts_ids_core.base.ids_element.IdsElement`
    class, which uses `IdsModelMetaclass` as its metaclass.

    # Field Definition
    Fields are expected to be defined in one of the following three ways:

    1. With a type annotation. For example

        ```python
        class Example(IdsElement):
            field_1: str
        ```

    2. With a type annotation and assignment to a default value using an
       equals sign. For example, if the default value is to be "value", do

        ```python
        class Example(IdsElement):
            field_2: str = "value"
        ```
    3. Via the `ts_ids_core.base.ids_element.IdsField` function. For example,

        ```python
        class Example(IdsElement):
            field_1: str = IdsField()
            field_2: str = IdsField(default="value")
        ```

    To specify that a field is "required", use the `Required` type annotation. For example,

    ```python
    from ts_ids_core.annotations import Required

    class Example(IdsElement):
        required_field: Required[str]
    ```

    ## Allowed field types

    Note that fields may be only atomic types or classes whose metaclass is
    `IdsModelMetaclass`. They cannot be containers, e.g. `dict` or `tuple`, or other
    generics, e.g. `TypeVar`.

    ## Required Fields
    Required is defined in the same sense as that in JSON Schema: the field must be assigned
    a value during instantiation. By default, a field not annotated as `Required` is not
    "required" and does not need to be passed a value during instantiation. Fields that
    are not `Required` and whose values not defined, are skipped during serialization to JSON.

    .. note::

        Unlike `pydantic.BaseModel`, one cannot specify whether a field is Required using
        "required" keyword argument. Likewise, `...` cannot be used to specify that a field is
        Required.

    ## Nullable fields
    A "nullable" field may take on the value of `None` in Python (null in JSON). To indicate
    that a field may be "nullable", use the `Nullable` type hint.

    ```python
    from ts_ids_core.annotations import Nullable

    class Example(IdsElement):
        field: Nullable[str]
    ```

    .. note::

        Note that Nullable and Required are not mutually exclusive: for example, a
        `Required[Nullable[str]]` field must be explicitly assigned a string or `None` value
        during instantiation. Also note that, different from `pydantic` behavior, if a field
        is Nullable but not Required, its default value will be `IDS_UNDEFINED`. (`pydantic`
        would default to `None`.)
    """

    __fields__: Dict[str, ModelField]
    _inherited_non_mandatory_fields: Set[str]

    @no_type_check
    def __new__(
        mcs,
        name: str,
        bases: Tuple[Type, ...],
        namespace: DictStrAny,
        *,
        inherit: Iterable[str] = tuple(),
        **kwargs: Any,
    ) -> "IdsModelMetaclass":

        """
        :param name:
            The name of the class to be created.
        :param bases:
            The base classes from which the class is derived, in method-resolution order.
        :param namespace:
            See the class docstring for further info.
        """
        raw_fields = get_raw_pydantic_fields(namespace)
        processed_raw_fields = [process_raw_field(field) for field in raw_fields]
        annotations = namespace.get("__annotations__", dict())
        annotations.update(
            {field.name: field.type_hint for field in processed_raw_fields}
        )
        namespace.update(
            {field.name: field.field_info for field in processed_raw_fields}
        )
        cls = super(IdsModelMetaclass, mcs).__new__(
            mcs, name, bases, namespace, **kwargs
        )
        # Assert that the `schema_extra_metadata` field is not an IDS field because
        # `schema_extra_metadata` is a reserved name.
        if "schema_extra_metadata" in cls.__fields__:
            raise InvalidField(
                "`schema_extra_metadata` is reserved for JSON Schema metadata and thus "
                "cannot be an IDS field name."
            )

        mcs._update_inherited_fields(
            cls, base_classes=bases, add_non_mandatory_fields=inherit
        )

        for field_name in cls.__fields__:
            model_field = cls.__fields__[field_name]
            # Assert that either the `ModelField` instance has already defined `required`
            # e.g. via inheritance, or that the `FieldInfo`'s "required" value was set
            assert (
                "required" in model_field.field_info.extra
                or model_field.required is not PYDANTIC_UNDEFINED
            ), f"Field '{field_name}' did not properly set its 'required' property."
            model_field.required = model_field.field_info.extra.pop(
                "required", model_field.required
            )
            if model_field.field_info.default_factory is None:
                model_field.default = model_field.field_info.default

        return cls

    @staticmethod
    def _update_inherited_fields(
        cls: "IdsModelMetaclass",
        base_classes: Iterable["IdsModelMetaclass"],
        add_non_mandatory_fields: Iterable[str],
    ) -> None:
        """Delete Fields if they're not meant to be inherited."""
        parent_non_mandatory_fields = {
            name
            for base_class in base_classes
            for name, field in base_class.__fields__.items()
            if not has_mandatory_inheritance(field)
        }
        add_non_mandatory_fields = set(add_non_mandatory_fields)
        invalid_non_mandatory_fields = add_non_mandatory_fields.difference(
            parent_non_mandatory_fields
        )
        if len(invalid_non_mandatory_fields) > 0:
            raise InvalidNonMandatoryField(
                f"Attempted to inherit the following invalid Non-Mandatory fields: "
                f"{', '.join(invalid_non_mandatory_fields)}. Perhaps they're spelled "
                f"incorrectly or otherwise missing from the parent class?"
            )

        # Non-Mandatory fields that were inherited by the parent class from the
        # grandparent class are stored in the `_inherited_non_mandatory_fields` class attribute.
        # If `_inherit_optional_fields` has not been bound to a value, bind it to an
        # empty set.
        fields_to_inherit = getattr(cls, "_inherited_non_mandatory_fields", set())
        setattr(cls, "_inherited_non_mandatory_fields", fields_to_inherit)
        # Add the field names passed in by the user to `_inherited_non_mandatory_fields`.
        fields_to_inherit.update(add_non_mandatory_fields)

        not_inherited_fields = parent_non_mandatory_fields.difference(fields_to_inherit)
        for field_name in not_inherited_fields:
            del cls.__fields__[field_name]
