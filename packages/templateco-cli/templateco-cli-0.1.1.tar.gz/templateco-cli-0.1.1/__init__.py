import logging
from pathlib import Path
from typing import List

import typer as typer

from templateco import NoPluginsFoundException, PluginOperationException, templateco

app = typer.Typer(name="templateco")


@app.callback()
def index(verbose: bool = typer.Option(default=None, help="Verbose logging")) -> None:
    """
    Set global running options.

    :param verbose: Enable verbose logging.
    :return: None
    """
    logging_level = logging.INFO if not verbose else logging.DEBUG
    logging.basicConfig(
        level=logging_level, stream=typer.get_text_stream(name="stderr")
    )


@app.command()
def make(
    language: str = typer.Argument(..., help="Language/Type of folder to template."),
    folder: Path = typer.Argument(..., help="Folder to output to."),
    namespaces: List[str] = typer.Option(
        ["templateco"],
        help="Specify custom Templateco namespaces.",
    ),
    force: bool = typer.Option(False, help="Force creation of the template."),
    config: List[str] = typer.Option([], help="KEY=VALUE"),
) -> None:
    """
    Make a new templated folder.
    """
    if folder.exists() and not force:
        raise typer.BadParameter(
            param_hint="FOLDER",
            message=f"Folder [{folder}] already exists. To override use --force.",
        )

    try:
        # Rewrite the config entries into a dictionary.
        dict_config = {entry.split("=")[0]: entry.split("=")[1] for entry in config}
    except IndexError:
        raise typer.BadParameter(
            param_hint="config",
            message="Configuration must be passed using KEY=VALUE e.g. "
            "--config foo=bar",
        )

    try:
        templateco(
            language=language, folder=folder, namespaces=namespaces, config=dict_config
        )
    except NoPluginsFoundException:
        raise typer.BadParameter(
            param_hint="TEMPLATE",
            message="No plugins matching this template can be found. "
            f"Try `pip install {namespaces[0]}_{language}_plugin`.",
        )
    except PluginOperationException as err:
        typer.secho(
            "** Templateco encountered a problem **",
            fg=typer.colors.RED,
            err=True,
            bold=True,
        )
        typer.secho(err, err=True)


__all__ = ["app"]
