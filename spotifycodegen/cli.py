import argparse
import pathlib
from spotifycodegen.main import spotifycodegen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_dir", type=pathlib.Path, help="output directory, defaults to current directory.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url_list", nargs="*", type=str, help="generates code with cover for list of URLs.")
    group.add_argument("--uri_list", nargs="*", type=str, help="generates code with cover for list of URIs.")
    group.add_argument("--track", nargs="?", type=str, help="generates code with tracks album cover.")
    group.add_argument("--album", nargs="?", type=str, help="generates code with album cover.")
    group.add_argument("--artist", nargs="?", type=str, help="generates code with artist cover.")
    group.add_argument(
        "--saved-albums",
        action="store_true",
        help="Generates code with album for all saved albums. Requires OAuth login.",
    )
    group.add_argument(
        "--followed-artists",
        action="store_true",
        help="Generates code with artist cover for 50 followed artists. Requires OAuth login.",
    )
    args = parser.parse_args()

    s = spotifycodegen(output_dir=args.output_dir)

    if args.url_list is not None:
        s.gen_codes_urls(args.url_list)
    elif args.uri_list is not None:
        s.gen_codes_uris(args.uri_list)
    elif args.track is not None:
        s.gen_codes_query(args.track, "track")
    elif args.album is not None:
        s.gen_codes_query(args.album, "album")
    elif args.artist is not None:
        s.gen_codes_query(args.artist, "artist")

    elif args.saved - albums is True:
        s = spotifycodegen(output_dir=args.output_dir, scopes=["user-library-read"])
        s.gen_codes_album_lib()
    elif args.followed - artists is True:
        s = spotifycodegen(output_dir=args.output_dir, scopes=["user-follow-read"])
        s.gen_codes_followed_artists()


if __name__ == "__main__":
    main()
