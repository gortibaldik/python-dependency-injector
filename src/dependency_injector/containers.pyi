from typing import (
    Type,
    Dict,
    Tuple,
    Optional,
    Any,
    Union,
    ClassVar,
    Callable as _Callable,
    Iterable,
    Iterator,
    TypeVar,
    Awaitable,
    overload,
)

from .providers import Provider, Self, ProviderParent


C_Base = TypeVar('C_Base', bound='Container')
C = TypeVar('C', bound='DeclarativeContainer')
C_Overriding = TypeVar('C_Overriding', bound='DeclarativeContainer')
TT = TypeVar('TT')


class Container:
    provider_type: Type[Provider] = Provider
    providers: Dict[str, Provider]
    dependencies: Dict[str, Provider]
    overridden: Tuple[Provider]
    __self__: Self
    def __init__(self) -> None: ...
    def __deepcopy__(self, memo: Optional[Dict[str, Any]]) -> Provider: ...
    def __setattr__(self, name: str, value: Union[Provider, Any]) -> None: ...
    def __delattr__(self, name: str) -> None: ...
    def set_providers(self, **providers: Provider): ...
    def set_provider(self, name: str, provider: Provider) -> None: ...
    def override(self, overriding: C_Base) -> None: ...
    def override_providers(self, **overriding_providers: Provider) -> None: ...
    def reset_last_overriding(self) -> None: ...
    def reset_override(self) -> None: ...
    def wire(self, modules: Optional[Iterable[Any]] = None, packages: Optional[Iterable[Any]] = None) -> None: ...
    def unwire(self) -> None: ...
    def init_resources(self) -> Optional[Awaitable]: ...
    def shutdown_resources(self) -> Optional[Awaitable]: ...
    def apply_container_providers_overridings(self) -> None: ...
    def reset_singletons(self) -> None: ...
    def check_dependencies(self) -> None: ...
    @overload
    def resolve_provider_name(self, provider: Provider) -> str: ...
    @classmethod
    @overload
    def resolve_provider_name(cls, provider: Provider) -> str: ...
    @property
    def parent(self) -> Optional[ProviderParent]: ...
    @property
    def parent_name(self) -> Optional[str]: ...
    def assign_parent(self, parent: ProviderParent) -> None: ...
    @overload
    def traverse(self, types: Optional[Iterable[Type[TT]]] = None) -> Iterator[TT]: ...
    @classmethod
    @overload
    def traverse(cls, types: Optional[Iterable[Type[TT]]] = None) -> Iterator[TT]: ...


class DynamicContainer(Container): ...


class DeclarativeContainer(Container):
    cls_providers: ClassVar[Dict[str, Provider]]
    inherited_providers: ClassVar[Dict[str, Provider]]
    def __init__(self, **overriding_providers: Union[Provider, Any]) -> None: ...



def override(container: Type[C]) -> _Callable[[Type[C_Overriding]], Type[C_Overriding]]: ...


def copy(container: Type[C]) -> _Callable[[Type[C_Overriding]], Type[C_Overriding]]: ...


def is_container(instance: Any) -> bool: ...
