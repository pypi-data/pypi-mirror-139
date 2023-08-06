import typing
from typing_extensions import ParamSpec

_T = typing.TypeVar("_T")
_ArgsT = ParamSpec("_ArgsT")
_ReturnT = typing.TypeVar("_ReturnT")

ObjectRefFullName = "typed_ray.ray_types.ObjectRef"


__all__ = ["OPTIONS_KWARGS", "ObjectRef", "ActorHandle"]


OPTIONS_KWARGS = {
    "num_gpus": "builtins.int", "num_cpus": "builtins.int", "name": "builtins.str"
}


class ObjectRef(typing.Generic[_T]):
    """Object returned by ray.put"""


class ActorHandle(typing.Generic[_T]):
    """Actor handle returned by decorating class with tray.remote_cls"""


class _RemoteFunctionOptions(typing.Protocol[_ArgsT, _ReturnT]):
    """Options for remote function"""
    def __call__(
        self,
        num_gpus: typing.Optional[int] = None,
        num_cpus: typing.Optional[int] = None,
        name: str = "",
    ) -> "RemoteFunction[_ArgsT, _ReturnT]": ...



class RemoteFunction(typing.Generic[_ArgsT, _ReturnT]):
    @property
    def remote(self) -> typing.Callable[_ArgsT, ObjectRef[_ReturnT]]:
        """
        Call a remote function.
        """
        raise NotImplementedError

    @property
    def options(self) -> _RemoteFunctionOptions[_ArgsT, _ReturnT]:
        """
        Set options for a remote function.
        """
        raise NotImplementedError
