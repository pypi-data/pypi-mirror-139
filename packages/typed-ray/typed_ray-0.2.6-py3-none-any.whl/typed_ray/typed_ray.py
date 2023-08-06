import typing

import ray
from typing_extensions import ParamSpec

from typed_ray.ray_types import ActorHandle, ObjectRef, RemoteFunction


T = typing.TypeVar("T")




def put(value: T) -> ObjectRef[T]:
    """
    Put a value into the object store.

    Args:
        value: The value to put into the object store.

    Returns:
        An ObjectRef object that can be used to get the value back later.
    """
    return ray.put(value)  # type: ignore


@typing.overload
def get(object_refs: ObjectRef[T]) -> T:
    pass


@typing.overload
def get(object_refs: typing.List[ObjectRef[T]]) -> typing.List[T]:
    pass


def get(
    object_refs: typing.Union[ObjectRef[T], typing.List[ObjectRef[T]]]
) -> typing.Union[T, typing.List[T]]:
    """
    Get the value wrapped by ObjectRef.

    Args:
        object_refs: The ObjectRef object usually returned by ray.put.

    Returns:
        The value that was wrapped by ObjectRef.
    """
    return ray.get(object_refs)  # type: ignore


def wait(
    object_refs: typing.List[ObjectRef[T]],
    *,
    num_returns: int = 1,
    timeout: typing.Optional[float],
    fetch_local: bool = True
) -> typing.Tuple[typing.List[ObjectRef[T]], typing.List[ObjectRef[T]]]:
    """Return a list of IDs that are ready and a list of IDs that are not.

    If timeout is set, the function returns either when the requested number of
    IDs are ready or when the timeout is reached, whichever occurs first. If it
    is not set, the function simply waits until that number of objects is ready
    and returns that exact number of object refs.

    This method returns two lists. The first list consists of object refs that
    correspond to objects that are available in the object store. The second
    list corresponds to the rest of the object refs (which may or may not be
    ready).

    Ordering of the input list of object refs is preserved. That is, if A
    precedes B in the input list, and both are in the ready list, then A will
    precede B in the ready list. This also holds true if A and B are both in
    the remaining list.

    This method will issue a warning if it's running inside an async context.
    Instead of ``ray.wait(object_refs)``, you can use
    ``await asyncio.wait(object_refs)``.

    Args:
        object_refs (List[ObjectRef]): List of object refs for objects that may
            or may not be ready. Note that these IDs must be unique.
        num_returns (int): The number of object refs that should be returned.
        timeout (float): The maximum amount of time in seconds to wait before
            returning.
        fetch_local (bool): If True, wait for the object to be downloaded onto
            the local node before returning it as ready. If False, ray.wait()
            will not trigger fetching of objects to the local node and will
            return immediately once the object is available anywhere in the
            cluster.

    Returns:
        A list of object refs that are ready and a list of the remaining object
        IDs.
    """
    return ray.wait(  # type: ignore
        object_refs, num_returns=num_returns, timeout=timeout, fetch_local=fetch_local
    )


_ArgsT = ParamSpec("_ArgsT")
_ReturnT = typing.TypeVar("_ReturnT")


def remote_func(
    func: typing.Callable[_ArgsT, _ReturnT]
) -> RemoteFunction[_ArgsT, _ReturnT]:
    """
    Make a remote function.

    Args:
        func: The function to make remote.

    Returns:
        A remote function.
    """
    return ray.remote(func)  # type: ignore


def remote_cls(cls: typing.Type[typing.Any]) -> typing.Any:
    """
    Make a remote class.

    Args:
        cls: The class to make remote.

    Returns:
        A remote class.
    """
    return ray.remote(cls)  # type: ignore


def get_actor(
    name: str, namespace: typing.Optional[str] = None
) -> ActorHandle[typing.Any]:
    """Get a handle to a namd actor.

    Gets a handle to an actor with the given name. The actor must
    have been created with Actor.options(name="name").remote(). This
    works for both detached & non-detached actors.

    Args:
        name: The name of the actor.
        namespace: The namespace of the actor, or None to specify the current
            namespace.

    Returns:
        ActorHandle to the actor.

    Raises:
        ValueError if the named actor does not exist.
    """
    return ray.get_actor(name, namespace)  # type: ignore


def kill(actor: ActorHandle[typing.Any]) -> None:
    """Kill an actor forcefully.

    This will interrupt any running tasks on the actor, causing them to fail
    immediately. ``atexit`` handlers installed in the actor will not be run.

    If you want to kill the actor but let pending tasks finish,
    you can call ``actor.__ray_terminate__.remote()`` instead to queue a
    termination task. Any ``atexit`` handlers installed in the actor *will*
    be run in this case.

    If the actor is a detached actor, subsequent calls to get its handle via
    ray.get_actor will fail.

    Args:
        actor (ActorHandle): Handle to the actor to kill.
        no_restart (bool): Whether or not this actor should be restarted if
            it's a restartable actor.
    """
    ray.kill(actor)  # type: ignore


def cancel(
    object_ref: ObjectRef[typing.Any], *, force: bool = False, recursive: bool = True
) -> None:
    """Cancels a task according to the following conditions.

    If the specified task is pending execution, it will not be executed. If
    the task is currently executing, the behavior depends on the ``force``
    flag. When ``force=False``, a KeyboardInterrupt will be raised in Python
    and when ``force=True``, the executing task will immediately exit.
    If the task is already finished, nothing will happen.

    Only non-actor tasks can be canceled. Canceled tasks will not be
    retried (max_retries will not be respected).

    Calling ray.get on a canceled task will raise a TaskCancelledError or a
    WorkerCrashedError if ``force=True``.

    Args:
        object_ref (ObjectRef): ObjectRef returned by the task
            that should be canceled.
        force (boolean): Whether to force-kill a running task by killing
            the worker that is running the task.
        recursive (boolean): Whether to try to cancel tasks submitted by the
            task specified.
    Raises:
        TypeError: This is also raised for actor tasks.
    """
    return ray.kill(object_ref, force=force, recursive=recursive)  # type: ignore


def get_gpu_ids() -> typing.List[str]:
    """Get the IDs of the GPUs that are available to the worker.

    If the CUDA_VISIBLE_DEVICES environment variable was set when the worker
    started up, then the IDs returned by this method will be a subset of the
    IDs in CUDA_VISIBLE_DEVICES. If not, the IDs will fall in the range
    [0, NUM_GPUS - 1], where NUM_GPUS is the number of GPUs that the node has.

    Returns:
        A list of GPU IDs.
    """
    return ray.get_gpu_ids()  # type: ignore


def shutdown(_exiting_interpreter: bool = False) -> None:
    """Disconnect the worker, and terminate processes started by ray.init().

    This will automatically run at the end when a Python process that uses Ray
    exits. It is ok to run this twice in a row. The primary use case for this
    function is to cleanup state between tests.

    Note that this will clear any remote function definitions, actor
    definitions, and existing actors, so if you wish to use any previously
    defined remote functions or actors after calling ray.shutdown(), then you
    need to redefine them. If they were defined in an imported module, then you
    will need to reload the module.

    Args:
        _exiting_interpreter (bool): True if this is called by the atexit hook
            and false otherwise. If we are exiting the interpreter, we will
            wait a little while to print any extra error messages.
    """
    return ray.shutdown()  # type: ignore


def method(num_returns: int) -> typing.Any:
    """Annotate an actor method.

    .. code-block:: python

        @ray.remote
        class Foo:
            @ray.method(num_returns=2)
            def bar(self):
                return 1, 2

        f = Foo.remote()

        _, _ = f.bar.remote()

    Args:
        num_returns: The number of object refs that should be returned by
            invocations of this actor method.
    """
    return ray.method(num_returns)  # type: ignore


def nodes() -> typing.List[
    typing.Dict[str, typing.Union[float, typing.Dict[str, float]]]
]:
    """Get a list of the nodes in the cluster (for debugging only).

    Returns:
        Information about the Ray clients in the cluster.
    """
    return ray.nodes()  # type: ignore


def cluster_resources() -> typing.Dict[str, float]:
    """Get the current total cluster resources.

    Note that this information can grow stale as nodes are added to or removed
    from the cluster.

    Returns:
        A dictionary mapping resource name to the total quantity of that
            resource in the cluster.
    """
    return ray.cluster_resources()  # type: ignore


def available_resources() -> typing.Dict[str, float]:
    """Get the current available cluster resources.

    This is different from `cluster_resources` in that this will return idle
    (available) resources rather than total resources.

    Note that this information can grow stale as tasks start and finish.

    Returns:
        A dictionary mapping resource name to the total quantity of that
            resource in the cluster.
    """
    return ray.available_resources()  # type: ignore


def timeline() -> typing.List[typing.Dict[str, typing.Any]]:
    """Return a list of profiling events that can viewed as a timeline.

    Ray profiling must be enabled by setting the RAY_PROFILING=1 environment
    variable prior to starting Ray.

    To view this information as a timeline, simply dump it as a json file by
    passing in "filename" or using using json.dump, and then load go to
    chrome://tracing in the Chrome web browser and load the dumped file.

    Args:
        filename: If a filename is provided, the timeline is dumped to that
            file.

    Returns:
        If filename is not provided, this returns a list of profiling events.
            Each profile event is a dictionary.
    """
    return ray.timeline()  # type: ignore
