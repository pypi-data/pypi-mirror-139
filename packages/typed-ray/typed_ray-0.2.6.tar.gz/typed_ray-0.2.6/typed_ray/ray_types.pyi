import typing

from typing_extensions import ParamSpec

ObjectRefFullName: str

_T = typing.TypeVar("_T")

class ObjectRef(typing.Generic[_T]): ...
class ActorHandle(typing.Generic[_T]): ...

_ArgsT = ParamSpec("_ArgsT")
_ReturnT = typing.TypeVar("_ReturnT")

OPTIONS_KWARGS: typing.Dict[str, str]

class _RemoteFunctionOptions(typing.Protocol[_ArgsT, _ReturnT]):
    def __call__(
        self,
        num_gpus: typing.Optional[int] = ...,
        num_cpus: typing.Optional[int] = ...,
        name: str = ...,
    ) -> "RemoteFunction[_ArgsT, _ReturnT]": ...

class RemoteFunction(typing.Generic[_ArgsT, _ReturnT]):
    @property
    def options(self) -> _RemoteFunctionOptions[_ArgsT, _ReturnT]: ...
    @property
    def remote(self) -> typing.Callable[_ArgsT, ObjectRef[_ReturnT]]: ...
