"""Main CLI application."""
from itertools import compress
from pathlib import Path
from typing import List, Optional

import tomli
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from typer import Argument, BadParameter, Context, Exit, Option, Typer, echo

from databooks.common import expand_paths
from databooks.config import TOML_CONFIG_FILE, get_config
from databooks.conflicts import conflicts2nbs, path2conflicts
from databooks.logging import get_logger
from databooks.metadata import clear_all
from databooks.version import __version__

logger = get_logger(__file__)

app = Typer()


def _version_callback(show_version: bool) -> None:
    """Return application version."""
    if show_version:
        echo("databooks version: " + __version__)
        raise Exit()


def _help_callback(ctx: Context, show_help: Optional[bool]) -> None:
    """Reimplement `help` command to execute eagerly."""
    if show_help:
        echo(ctx.command.get_help(ctx))
        raise Exit()


def _config_callback(ctx: Context, config_path: Optional[Path]) -> Optional[Path]:
    """Get config file and inject values into context to override default args."""
    target_paths = expand_paths(
        paths=[Path(p) for p in ctx.params.get("paths", ())], rglob="*"
    )
    config_path = (
        get_config(
            target_paths=target_paths,
            config_filename=TOML_CONFIG_FILE,
        )
        if config_path is None and target_paths
        else config_path
    )
    logger.debug(f"Loading config file from: {config_path}")

    ctx.default_map = ctx.default_map or {}  # initialize defaults

    if config_path is not None:  # config may not be specified
        with config_path.open("r") as f:
            conf = (
                tomli.load(f)
                .get("tool", {})
                .get("databooks", {})
                .get(ctx.command.name, {})
            )
        # Merge configuration
        ctx.default_map.update({k.replace("-", "_"): v for k, v in conf.items()})
    return config_path


@app.callback()
def callback(  # noqa: D103
    version: Optional[bool] = Option(
        None, "--version", callback=_version_callback, is_eager=True
    )
) -> None:
    """CLI tool to resolve git conflicts and remove metadata in notebooks."""


@app.command(add_help_option=False)
def meta(
    paths: List[Path] = Argument(..., is_eager=True, help="Path(s) of notebook files"),
    ignore: List[str] = Option(["!*"], help="Glob expression(s) of files to ignore"),
    prefix: str = Option("", help="Prefix to add to filepath when writing files"),
    suffix: str = Option("", help="Suffix to add to filepath when writing files"),
    rm_outs: bool = Option(False, help="Whether to remove cell outputs"),
    rm_exec: bool = Option(True, help="Whether to remove the cell execution counts"),
    nb_meta_keep: List[str] = Option([], help="Notebook metadata fields to keep"),
    cell_meta_keep: List[str] = Option([], help="Cells metadata fields to keep"),
    cell_fields_keep: List[str] = Option(
        [],
        help="Other (excluding `execution_counts` and `outputs`) cell fields to keep",
    ),
    overwrite: bool = Option(
        False, "--overwrite", "-w", help="Confirm overwrite of files"
    ),
    check: bool = Option(
        False,
        "--check",
        help="Don't write files but check whether there is unwanted metadata",
    ),
    verbose: bool = Option(
        False, "--verbose", "-v", help="Log processed files in console"
    ),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        is_eager=True,
        callback=_config_callback,
        resolve_path=True,
        exists=True,
        help="Get CLI options from configuration file",
    ),
    help: Optional[bool] = Option(
        None, is_eager=True, callback=_help_callback, help="Show this message and exit"
    ),
) -> None:
    """Clear both notebook and cell metadata."""
    if any(path.suffix not in ("", ".ipynb") for path in paths):
        raise BadParameter(
            "Expected either notebook files, a directory or glob expression."
        )
    nb_paths = expand_paths(paths=paths, ignore=ignore)
    if not nb_paths:
        logger.info(f"No notebooks found in {paths}. Nothing to do.")
        raise Exit()

    if not bool(prefix + suffix) and not check:
        if not overwrite:
            raise BadParameter(
                "No prefix nor suffix were passed."
                " Please specify `--overwrite` or `-w` to overwrite files."
            )
        else:
            logger.warning(f"{len(nb_paths)} files will be overwritten")

    write_paths = [p.parent / (prefix + p.stem + suffix + p.suffix) for p in nb_paths]
    cell_fields_keep = list(
        compress(["outputs", "execution_count"], (not v for v in (rm_outs, rm_exec)))
    ) + list(cell_fields_keep)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        metadata = progress.add_task("[yellow]Removing metadata", total=len(nb_paths))

        are_equal = clear_all(
            read_paths=nb_paths,
            write_paths=write_paths,
            progress_callback=lambda: progress.update(metadata, advance=1),
            notebook_metadata_keep=nb_meta_keep,
            cell_metadata_keep=cell_meta_keep,
            cell_fields_keep=cell_fields_keep,
            check=check,
            verbose=verbose,
        )
    if check:
        if all(are_equal):
            logger.info("No unwanted metadata!")
        else:
            logger.info(
                f"Found unwanted metadata in {sum(not eq for eq in are_equal)} out of"
                f" {len(are_equal)} files"
            )
            raise Exit(code=1)
    else:
        logger.info(
            f"The metadata of {sum(not eq for eq in are_equal)} out of {len(are_equal)}"
            " notebooks were removed!"
        )


@app.command(add_help_option=False)
def fix(
    paths: List[Path] = Argument(
        ..., is_eager=True, help="Path(s) of notebook files with conflicts"
    ),
    ignore: List[str] = Option(["!*"], help="Glob expression(s) of files to ignore"),
    metadata_head: bool = Option(
        True, help="Whether or not to keep the metadata from the head/current notebook"
    ),
    cells_head: Optional[bool] = Option(
        None,
        help="Whether to keep the cells from the head/base notebook. Omit to keep both",
    ),
    cell_fields_ignore: List[str] = Option(
        [
            "id",
            "execution_count",
        ],
        help="Cell fields to remove before comparing cells",
    ),
    interactive: bool = Option(
        False,
        "--interactive",
        "-i",
        help="Interactively resolve the conflicts (not implemented)",
    ),
    verbose: bool = Option(False, help="Log processed files in console"),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        is_eager=True,
        callback=_config_callback,
        resolve_path=True,
        exists=True,
        help="Get CLI options from configuration file",
    ),
    help: Optional[bool] = Option(
        None, is_eager=True, callback=_help_callback, help="Show this message and exit"
    ),
) -> None:
    """
    Fix git conflicts for notebooks.

    Perform by getting the unmerged blobs from git index, comparing them and returning
     a valid notebook summarizing the differences - see
     [git docs](https://git-scm.com/docs/git-ls-files).
    """
    filepaths = expand_paths(paths=paths, ignore=ignore)
    conflict_files = path2conflicts(nb_paths=filepaths)
    if not conflict_files:
        raise BadParameter(
            f"No conflicts found at {', '.join([str(p) for p in filepaths])}."
        )
    if interactive:
        raise NotImplementedError

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
    ) as progress:
        conflicts = progress.add_task(
            "[yellow]Removing metadata", total=len(conflict_files)
        )
        conflicts2nbs(
            conflict_files=conflict_files,
            meta_first=metadata_head,
            cells_first=cells_head,
            cell_fields_ignore=cell_fields_ignore,
            verbose=verbose,
            progress_callback=lambda: progress.update(conflicts, advance=1),
        )
    logger.info(f"Resolved the conflicts of {len(conflict_files)}!")


@app.command()
def diff() -> None:
    """Show differences between notebooks (not implemented)."""
    raise NotImplementedError
