"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """spotify-codegen."""


if __name__ == "__main__":
    main(prog_name="spotify-codegen")  # pragma: no cover
