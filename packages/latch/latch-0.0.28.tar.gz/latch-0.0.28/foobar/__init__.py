"""
foobar
~~
Some biocompute
"""

from pathlib import Path

from latch import small_task, workflow
from latch.types import LatchFile, LatchOutputFile


@small_task
def foobar_task(sample_input: LatchFile, sample_output: LatchOutputFile) -> LatchFile:

    with open(sample_input, "r") as f:
        print(f.read())

    return LatchFile(str(Path(sample_input)), "latch:///chuck-norris")


@workflow
def foobar(sample_input: LatchFile, sample_output: LatchOutputFile) -> LatchFile:
    """Description...

    foobar markdown
    ----

    Write some documentation about your workflow in
    markdown here:

    bump this

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
          input

          __metadata__:
            display_name: Sample Input

        sample_output:
          output

          __metadata__:
            display_name: Sample Output
    """
    return foobar_task(
        sample_input=sample_input,
        sample_output=sample_output,
    )
