"""
foobar
~~
Some biocompute
"""

from pathlib import Path

from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from latch.types import LatchFile


@task()
def foobar_task(sample_input: LatchFile) -> LatchFile:

    with open(sample_input, "r") as f:
        print(f.read())

    return LatchFile(str(Path(sample_input)), "latch:///chuck-norris")


@workflow
def foobar(sample_input: LatchFile, num: int) -> LatchFile:
    """Description...

    foobar markdown
    ----

    Write some documentation about your workflow in
    markdown here:

    > Markdown syntax works as expected.

    ## Foobar

    __metadata__:
        display_name: foobar
        author:
            name: n/a
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        sample_input:
          test this out

          __metadata__:
            display_name: Sample Param
    """
    return foobar_task(
        sample_input=sample_input,
    )
