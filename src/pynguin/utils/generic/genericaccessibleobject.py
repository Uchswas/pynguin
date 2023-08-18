#  This file is part of Pynguin.
#
#  SPDX-FileCopyrightText: 2019-2023 Pynguin Contributors
#
#  SPDX-License-Identifier: MIT
#
"""Provide wrappers around constructors, methods, function, fields and enums.

Think of these like the reflection classes in Java.
"""
from __future__ import annotations

import abc
import enum
import typing

from types import BuiltinFunctionType
from types import ClassMethodDescriptorType
from types import FunctionType
from types import MethodDescriptorType
from types import WrapperDescriptorType

from pynguin.analyses.typesystem import InferredSignature
from pynguin.analyses.typesystem import Instance
from pynguin.utils.orderedset import OrderedSet


TypesOfCallables = (
    FunctionType
    | BuiltinFunctionType
    | WrapperDescriptorType
    | MethodDescriptorType
    | ClassMethodDescriptorType
)

if typing.TYPE_CHECKING:
    from pynguin.analyses.typesystem import ProperType
    from pynguin.analyses.typesystem import TypeInfo


class GenericAccessibleObject(metaclass=abc.ABCMeta):
    """Abstract base class for something that can be accessed."""

    def __init__(self, owner: TypeInfo | None):
        """Constructor.

        Args:
            owner: The owning type
        """
        self._owner = owner

    @abc.abstractmethod
    def generated_type(self) -> ProperType:
        """Provides the type that is generated by this accessible object.

        Returns:
            The generated type  # noqa: DAR202
        """

    @property
    def owner(self) -> TypeInfo | None:
        """The type which owns this accessible object.

        Returns:
            The owner of this accessible object
        """
        return self._owner

    def is_enum(self) -> bool:
        """Is this an enum?

        Returns:
            Whether this is an enum
        """
        return False

    def is_method(self) -> bool:
        """Is this a method?

        Returns:
            Whether this is a method
        """
        return False

    def is_constructor(self) -> bool:
        """Is this a constructor?

        Returns:
            Whether this is a constructor
        """
        return False

    def is_function(self) -> bool:
        """Is this a function?

        Returns:
            Whether this is a function
        """
        return False

    def is_field(self) -> bool:
        """Is this a field?

        Returns:
            Whether this is a field
        """
        return False

    def is_static(self) -> bool:
        """Is this static?

        Returns:
            Whether this is static
        """
        return False

    def get_num_parameters(self) -> int:
        """Number of parameters.

        Returns:
            The number of parameters
        """
        return 0

    @abc.abstractmethod
    def get_dependencies(
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        """A set of types that are required to use this accessible.

        Returns:
            A set of types  # noqa: DAR202
        """


class GenericEnum(GenericAccessibleObject):
    """Models an enum."""

    def __init__(self, owner: TypeInfo):
        """Constructs an enum-representing object.

        Args:
            owner: The owning class
        """
        super().__init__(owner)
        self._generated_type = Instance(owner)
        self._names = [
            e.name
            for e in typing.cast(
                list[enum.Enum], list(typing.cast(type[enum.Enum], owner.raw_type))
            )
        ]

    def generated_type(self) -> ProperType:  # noqa: D102
        return self._generated_type

    @property
    def names(self) -> list[str]:
        """All names that this enum has.

        Returns:
        All possible values of this enum.
        """
        return self._names

    def is_enum(self) -> bool:  # noqa: D102
        return True

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        return OrderedSet()

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericEnum):
            return False
        return self._owner == other._owner

    def __hash__(self):
        return hash(self._owner)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.owner})"


class GenericCallableAccessibleObject(GenericAccessibleObject, metaclass=abc.ABCMeta):
    """Abstract base class for something that can be called."""

    def __init__(
        self,
        owner: TypeInfo | None,
        callable_: TypesOfCallables,
        inferred_signature: InferredSignature,
        raised_exceptions: set[str] = frozenset(),  # type: ignore[assignment]
    ) -> None:
        """Initializes the object.

        Args:
            owner: An optional owner of the callable
            callable_: The callable itself
            inferred_signature: The signature of the callable
            raised_exceptions: A set of raised exceptions, if any exist
        """
        super().__init__(owner)
        self._callable = callable_
        self._inferred_signature = inferred_signature
        self._raised_exceptions = raised_exceptions

    def generated_type(self) -> ProperType:  # noqa: D102
        return self._inferred_signature.return_type

    @property
    def inferred_signature(self) -> InferredSignature:
        """Provides access to the inferred type signature information.

        Returns:
            The inferred type signature
        """
        return self._inferred_signature

    @property
    def raised_exceptions(self) -> set[str]:
        """Provides the set of exceptions that is expected to be raised by this.

        Returns:
            The set of exceptions that is expected to be raised by this callable
        """
        return self._raised_exceptions

    @property
    def callable(  # noqa: A003
        self,
    ) -> TypesOfCallables:
        """Provides the callable.

        Returns:
            The callable
        """
        return self._callable

    def get_num_parameters(self) -> int:  # noqa: D102
        return len(self.inferred_signature.original_parameters)

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        return OrderedSet(self.inferred_signature.get_parameter_types(memo).values())


class GenericConstructor(GenericCallableAccessibleObject):
    """A constructor."""

    def __init__(
        self,
        owner: TypeInfo,
        inferred_signature: InferredSignature,
        raised_exceptions: set[str] = frozenset(),  # type: ignore[assignment]
    ) -> None:
        """Initializes a constructor-representing object.

        Args:
            owner: The owning class type
            inferred_signature: The signature
            raised_exceptions: A set of raised exceptions, if there are any
        """
        super().__init__(
            owner,
            owner.raw_type.__init__,  # type: ignore[misc]
            inferred_signature,
            raised_exceptions,
        )
        self._generated_type = Instance(owner)

    def generated_type(self) -> ProperType:  # noqa: D102
        return self._generated_type

    def is_constructor(self) -> bool:  # noqa: D102
        return True

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericConstructor):
            return False
        return self._owner == other._owner

    def __hash__(self):
        return hash(self._owner)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.owner}, {self.inferred_signature})"

    def __str__(self):
        assert self.owner
        return self.owner.full_name


class GenericMethod(GenericCallableAccessibleObject):
    """A method."""

    def __init__(
        self,
        owner: TypeInfo,
        method: TypesOfCallables,
        inferred_signature: InferredSignature,
        raised_exceptions: set[str] = frozenset(),  # type: ignore[assignment]
        method_name: str | None = None,
    ) -> None:
        """Initializes a new method-representing object.

        Args:
            owner: The owning class type
            method: The type of the method
            inferred_signature: The signature of the method
            raised_exceptions: A set of raised exceptions, if there are any
            method_name: The optional name of the method
        """
        super().__init__(owner, method, inferred_signature, raised_exceptions)
        self._generated_type = inferred_signature.return_type
        self._method_name = method_name

    @property
    def owner(self) -> TypeInfo:  # noqa: D102
        assert self._owner is not None
        return self._owner

    @property
    def method_name(self):
        """Returns the name of a generic method.

        Returns:
            The name of a generic method.
        """
        return self._method_name

    def is_method(self) -> bool:  # noqa: D102
        return True

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        assert self.owner is not None, "Method must have an owner"
        dependencies = super().get_dependencies(memo)
        dependencies.add(Instance(self.owner))
        return dependencies

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericMethod):
            return False
        return self._callable == other._callable

    def __hash__(self):
        return hash(self._callable)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.owner},"
            f" {self._callable.__name__}, {self.inferred_signature})"
        )

    def __str__(self):
        return f"{self.owner.full_name}.{self._callable.__name__}"


class GenericFunction(GenericCallableAccessibleObject):
    """A function, which does not belong to any class."""

    def __init__(
        self,
        function: FunctionType,
        inferred_signature: InferredSignature,
        raised_exceptions: set[str] = frozenset(),  # type: ignore[assignment]
        function_name: str | None = None,
    ) -> None:
        """Initializes the function-representing object.

        Args:
            function: The type of the function
            inferred_signature: The function's signature
            raised_exceptions: A set of raised exceptions, might be empty if there are
                               none
            function_name: The optional name of the function
        """
        self._function_name = function_name
        super().__init__(None, function, inferred_signature, raised_exceptions)

    def is_function(self) -> bool:  # noqa: D102
        return True

    @property
    def function_name(self) -> str | None:
        """Returns the name of a generic function.

        Returns:
            The name of a generic function.
        """
        return self._function_name

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericFunction):
            return False
        return self._callable == other._callable

    def __hash__(self):
        return hash(self._callable)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self._callable.__name__}, "
            f"{self.inferred_signature})"
        )

    def __str__(self):
        return f"{self._callable.__module__}.{self._callable.__qualname__}"


class GenericAbstractField(GenericAccessibleObject, metaclass=abc.ABCMeta):
    """Abstract superclass for fields."""

    def __init__(
        self, owner: TypeInfo | None, field: str, field_type: ProperType
    ) -> None:
        """Constructs the new abstract field object.

        Args:
            owner: An optional type of the field owner (if any)
            field: The name of the field
            field_type: The type of the field
        """
        super().__init__(owner)
        self._field = field
        self._field_type = field_type

    def is_field(self) -> bool:  # noqa: D102
        return True

    def generated_type(self) -> ProperType:  # noqa: D102
        return self._field_type

    @property
    def field(self) -> str:
        """Provides the name of the field.

        Returns:
            The name of the field
        """
        return self._field


class GenericField(GenericAbstractField):
    """A field of an object."""

    def __init__(self, owner: TypeInfo, field: str, field_type: ProperType):
        """Initializes a new field wrapper.

        Args:
            owner: The owner of the field
            field: The name of the field
            field_type: The type of the field
        """
        super().__init__(owner, field, field_type)
        assert owner is not None, "Field must have an owner"

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        assert self._owner, "Field must have an owner"
        return OrderedSet([Instance(self._owner)])

    @property
    def owner(self) -> TypeInfo:  # noqa: D102
        assert self._owner is not None
        return self._owner

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericField):
            return False
        return self._owner == other._owner and self._field == other._field

    def __hash__(self):
        return hash((self._owner, self._field))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.owner}, {self._field},"
            f" {self._field_type})"
        )


class GenericStaticField(GenericAbstractField):
    """Static field of a class."""

    def __init__(self, owner: TypeInfo, field: str, field_type: ProperType):
        """Initializes a new object for a static field.

        Args:
            owner: The owner class of the static field
            field: The name of the field
            field_type: The type of the field
        """
        super().__init__(owner, field, field_type)
        assert owner is not None, "Field must have an owner"

    def is_static(self) -> bool:  # noqa: D102
        return True

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        return OrderedSet()

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericStaticField):
            return False
        return self._owner == other._owner and self._field == other._field

    def __hash__(self):
        return hash(
            (
                self._owner,
                self._field,
            )
        )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.owner}, {self._field},"
            f" {self._field_type})"
        )


class GenericStaticModuleField(GenericAbstractField):
    """Static fields defined in a module."""

    # TODO(fk) combine with regular static field?

    def __init__(self, module: str, field: str, field_type: ProperType) -> None:
        """Constructs the object.

        Args:
            module: Name of the module the field is declared in
            field: The name of the field
            field_type: The type of the field
        """
        super().__init__(None, field, field_type)
        self._module = module

    def is_static(self) -> bool:  # noqa: D102
        return True

    def get_dependencies(  # noqa: D102
        self, memo: dict[InferredSignature, dict[str, ProperType]]
    ) -> OrderedSet[ProperType]:
        return OrderedSet()

    @property
    def module(self) -> str:
        """Provides the name of the module where the field is defined.

        Returns:
            The name of the module where the field is defined.
        """
        return self._module

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, GenericStaticModuleField):
            return False
        return self._module == other._module and self._field == other._field

    def __hash__(self):
        return hash((self._module, self._field))

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self._module}, {self._field},"
            f" {self._field_type})"
        )
