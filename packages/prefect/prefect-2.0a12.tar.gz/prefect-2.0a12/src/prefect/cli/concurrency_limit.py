"""
Command line interface for working with concurrency limits.
"""
import typer
from rich.pretty import Pretty

from prefect.cli.base import (
    PrefectTyper,
    app,
    console,
    exit_with_error,
    exit_with_success,
)
from prefect.client import get_client
from prefect.utilities.asyncio import sync_compatible

concurrency_limit_app = PrefectTyper(
    name="concurrency-limit",
    help="Commands for managing task-level concurrency limits",
)
app.add_typer(concurrency_limit_app)


@concurrency_limit_app.command()
async def create(tag: str, concurrency_limit: int):
    """
    Create a concurrency limit against a tag.

    This limit controls how many task runs with that tag may simultaneously be in a
    Running state.
    """

    async with get_client() as client:
        await client.create_concurrency_limit(
            tag=tag, concurrency_limit=concurrency_limit
        )
        result = await client.read_concurrency_limit_by_tag(tag)

    console.print(Pretty(result))


@concurrency_limit_app.command()
async def read(tag: str):
    """
    View details about a concurrency limit. `active_slots` shows a list of TaskRun IDs
    which are currently using a concurrency slot.
    """

    async with get_client() as client:
        result = await client.read_concurrency_limit_by_tag(tag=tag)

    console.print(Pretty(result))


@concurrency_limit_app.command()
async def ls(limit: int = 15, offset: int = 0):
    """
    View all concurrency limits.
    """

    async with get_client() as client:
        result = await client.read_concurrency_limits(limit=limit, offset=offset)

    console.print(Pretty(result))


@concurrency_limit_app.command()
async def delete(tag: str):
    """
    Delete the concurrency limit set on the specified tag.
    """

    async with get_client() as client:
        result = await client.delete_concurrency_limit_by_tag(tag=tag)

    if result:
        exit_with_success(f"Deleted concurrency limit set on the tag: {tag}")
    else:
        exit_with_error(f"No concurrency limit found for the tag: {tag}")
