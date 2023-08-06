
"""
testwf
~~
Some biocompute
"""

from flytekit import task, workflow
from flytekit.types.file import FlyteFile
from flytekit.types.directory import FlyteDirectory

@task()
def testwf_task(
    sample_input: FlyteFile, output_dir: FlyteDirectory
) -> str:
    return "foo"


@workflow
def testwf(
    sample_input: FlyteFile, output_dir: FlyteDirectory
) -> str:
    """Description...

    testwf markdown
    ----

    Write some documentation about your workflow in
    markdown here:

    > Markdown syntax works as expected.

    ## Foobar

    __metadata__:
        display_name: testwf
        author:
            name: n/a
            email:
            github:
        repository:
        license:
            id: MIT

    Args:

        sample_input:
          A description

          __metadata__:
            display_name: Sample Param

        output_dir:
          A description

          __metadata__:
            display_name: Output Directory
    """
    return testwf_task(
        sample_input=sample_input,
        output_dir=output_dir
    )
