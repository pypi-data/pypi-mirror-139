from typing import Optional, List
from pathlib import Path

import click
from pytodotxt.todotxt import TodoTxt, Task  # type: ignore[import]

from . import parse_projects, full_backup, locate_todotxt_file, prompt_todo


def run(todotxt_file: Optional[Path], add_due: bool, time_format: str) -> None:
    # handle argument
    tfile = locate_todotxt_file(todotxt_file)
    if tfile is None:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    assert tfile is not None

    # read from main todo.txt file
    todos: TodoTxt = TodoTxt(tfile)

    # backup todo.txt file
    full_backup(tfile)

    # list of sources, done.txt will be added if it exists
    todo_sources: List[TodoTxt] = [todos]

    done_file: Path = tfile.parent / "done.txt"
    if not done_file.exists():
        click.secho(
            f"Could not find the done.txt file at {done_file}", err=True, fg="red"
        )
    else:
        todo_sources.append(TodoTxt(done_file))

    for t in todo_sources:
        t.parse()

    # prompt user for new todo
    new_todo: Optional[Task] = prompt_todo(
        add_due=add_due,
        time_format=time_format,
        projects=list(parse_projects(todo_sources)),
    )

    # write back to file
    if new_todo is not None:
        todos.tasks.append(new_todo)
        click.echo(
            "{}: {}".format(click.style("Adding Todo", fg="green"), str(new_todo))
        )
        todos.save(safe=True)


@click.command()
@click.argument(
    "todotxt-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    required=False,
)
@click.option(
    "--add-due/--no-add-due",
    is_flag=True,
    default=False,
    help="Add due: key/value flag based on deadline:",
    show_default=True,
)
@click.option(
    "--time-format",
    default="%Y-%m-%d-%H-%M",
    show_default=True,
    help="Specify a different time format for deadline:",
)
def cli(todotxt_file: Optional[Path], add_due: bool, time_format: str) -> None:
    run(todotxt_file, add_due, time_format)


if __name__ == "__main__":
    cli(prog_name="full_todotxt")
