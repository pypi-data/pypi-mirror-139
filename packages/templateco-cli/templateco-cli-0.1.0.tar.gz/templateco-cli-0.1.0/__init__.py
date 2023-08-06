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
    template: str = typer.Argument(None, help="Template to generate."),
    folder: str = typer.Argument(None, help="Folder to output to."),
    namespaces: List[str] = typer.Option(
        ["templateco"],
        help="Specify custom Templateco namespaces.",
    ),
    force: bool = typer.Option(False, help="Force creation of the template."),
) -> None:
    """
    Make a new templated folder.
    """
    if not template:
        raise typer.BadParameter(param_hint="TEMPLATE", message="Template is required.")
    elif not folder:
        raise typer.BadParameter(
            param_hint="FOLDER", message="Output folder is required."
        )
    elif Path(folder).exists() and not force:
        raise typer.BadParameter(
            param_hint="FOLDER",
            message=f"Folder [{folder}] already exists. To override use --force.",
        )

    try:
        templateco(template, output_folder=folder, namespaces=namespaces)
    except NoPluginsFoundException:
        raise typer.BadParameter(
            param_hint="TEMPLATE",
            message="No plugins matching this template can be found. "
            f"Try `pip install {namespaces[0]}_{template}_plugin`.",
        )
    except PluginOperationException as err:
        typer.secho(
            "** Templateco encountered a problem:",
            fg=typer.colors.RED,
            err=True,
            bold=True,
        )
        typer.secho(err, err=True)


__all__ = ["app"]
