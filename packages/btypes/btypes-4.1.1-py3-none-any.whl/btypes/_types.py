from collections import ChainMap, Counter, OrderedDict, abc, defaultdict, deque
from collections.abc import (
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    ByteString,
    Callable,
    Collection,
    Container,
    Coroutine,
    Generator,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Mapping,
    MappingView,
    MutableMapping,
    MutableSequence,
    MutableSet,
    Reversible,
    Sequence,
    ValuesView,
)
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    NamedTuple,
    Protocol,
    Text,
    TypedDict,
    TypeVar,
    Union,
)
from typing_extensions import Never, TypeAlias

__all__ = [
    "AbstractSet",
    "Any",
    "AsyncGenerator",
    "AsyncIterable",
    "AsyncIterator",
    "Awaitable",
    "Bool",
    "ByteArray",
    "ByteString",
    "Bytes",
    "Callable",
    "ChainMap",
    "Collection",
    "Complex",
    "Container",
    "Coroutine",
    "Counter",
    "Dict",
    "Final",
    "Float",
    "FrozenSet",
    "Generator",
    "Generic",
    "Int",
    "ItemsView",
    "Iterable",
    "Iterator",
    "KeysView",
    "List",
    "Literal",
    "Mapping",
    "MappingView",
    "MutableMapping",
    "MutableSequence",
    "MutableSet",
    "NamedTuple",
    "Never",
    "Object",
    "OrderedDict",
    "Protocol",
    "Reversible",
    "Sequence",
    "Set",
    "Slice",
    "Str",
    "Str",
    "Text",
    "Tuple",
    "Type",
    "TypeAlias",
    "TypedDict",
    "Union",
    "ValuesView",
]

T_co = TypeVar("T_co", covariant=True)

# builtin types
Bool = bool
ByteArray = bytearray
Bytes = bytes
Complex = complex
Dict = dict
Float = float
FrozenSet = frozenset
Int = int
List = list
Object = object
Set = set
Slice = slice
Str = str
Tuple = tuple
Type: TypeAlias = type[T_co]

# collections
DefaultDict = defaultdict
Deque = deque

# abstract base classes
AbstractSet = abc.Set
