"""CLI for using SpotifyCodeGen."""
from pathlib import Path
from typing import List

import click
from click import Context

from spotifycodegen.main import SpotifyCodeGen


@click.group()
@click.option(
    "-o",
    "--output_dir",
    type=click.Path(
        path_type=Path,
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
    ),
    help="Output directory where files get written to.",
)
@click.pass_context
def cli(ctx: Context, output_dir: Path) -> None:
    """Used for passing context."""
    ctx.ensure_object(dict)
    ctx.obj["output_dir"] = output_dir


@cli.command("uris", help="Get codes for a list of URIs.")
@click.argument("uris", nargs=-1, required=True)
@click.pass_context
def uri_list(ctx: Context, uris: List[str]) -> None:
    """Get codes for a list of URIs."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"])
    s.gen_codes_urls(uris)


@cli.command("urls", help="Get codes for a list of URLs.")
@click.argument("urls", nargs=-1, required=True)
@click.pass_context
def url_list(ctx: Context, urls: List[str]) -> None:
    """Get codes for a list of URLs."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"])
    s.gen_codes_urls(urls)


@cli.command("album", help="Query Spotify for an album name and generate code.")
@click.argument("album", nargs=1, required=True)
@click.pass_context
def album(ctx: Context, query: str) -> None:
    """Query Spotify for an album name and generate code."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"])
    s.gen_codes_query(query, "album")


@cli.command("artist", help="Query Spotify for an artist name and generate code.")
@click.argument("artist", nargs=1, required=True)
@click.pass_context
def artist(ctx: Context, query: str) -> None:
    """Query Spotify for an artist name and generate code."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"])
    s.gen_codes_query(query, "artist")


@cli.command("track", help="Query Spotify for a track name and generate code.")
@click.argument("track", nargs=1, required=True)
@click.pass_context
def track(ctx: Context, query: str) -> None:
    """Query Spotify for a track name and generate code."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"])
    s.gen_codes_query(query, "track")


@cli.command("saved-albums", help="Get codes for all saved albums.")
@click.argument("saved-albums", nargs=1, required=True)
@click.pass_context
def saved_albums(ctx: Context) -> None:
    """Get codes for all saved albums."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"], scopes=["user-library-read"])
    s.gen_codes_album_lib()


@cli.command("followed-artists", help="Get codes for 50 followed artists.")
@click.argument("followed-artists", nargs=1, required=True)
@click.pass_context
def followed_artists(ctx: Context) -> None:
    """Get codes for 50 followed artists."""
    s = SpotifyCodeGen(output_dir=ctx.obj["output_dir"], scopes=["user-follow-read"])
    s.gen_codes_followed_artists()


if __name__ == "__main__":
    cli()
