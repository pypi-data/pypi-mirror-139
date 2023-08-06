from os import PathLike
from typing import Annotated, Optional, Union

# Note this only exists in flaightkit fork.
from flytekit.core.with_metadata import FlyteMetadata
from flytekit.types.file import FlyteFile
from latch.types.url import LatchURL


class LatchFile(FlyteFile):
    """Represents a file object in the context of a task execution.

    The local path identifies the file object's location on local disk in
    the context of a task execution. `LatchFile` inherits implementation of
    `__fsopen__` from `FlyteFile`, so methods like `open` can retrieve a string
    representation of self.

    ..
        @task
        def task(file: LatchFile):

            with open(file, "r") as f:
                print(f.read())

            mypath = Path(file).resolve()


    The remote path identifies a remote location. The remote location, either a
    latch or s3 url, can be inspected from an object passed to the task to
    reveal its remote source.

    It can also to deposit the file to a latch path when the object is returned
    from a task.

    ..

        @task
        def task(file: LatchFile):

            path = file.remote_path # inspect remote location

            # Returning a different file to LatchData.
            return LatchFile("./foobar.txt", "latch:///foobar.txt")
    """

    def __init__(self, path: Union[str, PathLike], remote_path: PathLike, **kwargs):

        self._remote_path = LatchURL(remote_path).url  # validates url string

        if kwargs.get("downloader") is not None:
            super().__init__(path, kwargs["downloader"], remote_path)
        else:

            def noop():
                ...

            super().__init__(path, noop, remote_path)

        # This will manually download object to local disk in the case of a
        # user wishing to access self locally without referencing the path
        # through `__fspath__`, eg. through `self.local_path`.
        self.__fspath__()

    @property
    def local_path(self) -> str:
        """File path local to the environment executing the task."""
        return self._path

    @property
    def remote_path(self) -> Optional[str]:
        """A url referencing in object in LatchData or s3."""
        return self._remote_path


LatchOutputFile = Annotated[
    LatchFile,
    FlyteMetadata(
        {"output": True},
    ),
]
"""A LatchFile tagged as the output of some workflow.

The Latch Console uses this metadata to avoid checking for existence of the
file at its remote path and displaying an error. This check is normally made to
avoid launching workflows with LatchFiles that point to objects that don't
exist.
"""
