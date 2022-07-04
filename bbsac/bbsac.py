from colorthief import ColorThief
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import tqdm

import argparse
import io
import os
from urllib.request import urlopen


def rgb_to_hex(rgb):
    return "%02x%02x%02x" % rgb


def generate_album_codes(output_folder: str, album_uris: list[str],sp: spotipy.Spotify):
    """Generates images for each supplied album_uri that merges
    the album cover and its Spotify code.

    Parameters
    -------
    output_folder: str
        folder to save results in
    album_uris: str
        list of album uris
    """
    for album_uri in tqdm.tqdm(album_uris, desc="generating album codes "):

        # get album cover from spotify API
        results = sp.album(album_uri)
        link_to_cover = results["images"][0]["url"]
        cover_size = results["images"][0]["height"]
        album_art = Image.open(urlopen(link_to_cover))

        # get dominant color from cover
        # this doesnt write to disc and still allows colorthief to grab most dominant color
        with io.BytesIO() as file_object:
            album_art.save(file_object, "PNG")
            cf = ColorThief(file_object)
            dominant_color_rgb = cf.get_color(quality=1)

        dominant_color_hex = rgb_to_hex(dominant_color_rgb)
        code_color = (
            "black"
            if (dominant_color_rgb[0] + dominant_color_rgb[1] + dominant_color_rgb[2])
            / 3
            > 127
            else "white"
        )
        album_uri_call = album_uri.replace(":", "%3A")

        # get spotify code
        url = (
            "https://www.spotifycodes.com/downloadCode.php?uri=png%2F"
            + f"{dominant_color_hex}%2F{code_color}%2F{cover_size}%2F{album_uri_call}"
        )
        album_code = Image.open(urlopen(url))

        # merge images
        final_height = album_code.size[1] + cover_size
        im = Image.new(mode="RGB", size=(cover_size, final_height))
        im.paste(album_art, (0, 0))
        im.paste(album_code, (0, cover_size))

        filename = album_uri.replace(":", "-")
        im.save(f"{output_folder}/{filename}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "-o", dest="out", type=str, required=False, help="path to output folder"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--u",
        dest="uris",
        nargs=1,
        type=str,
        help="comma separated Spotify album URI(s)",
    )
    
    group.add_argument(
        "--a",
        dest="all_albums",
        action="store_true",
        required=False,
        help="flag for fetching all albums in your music library")

    args = parser.parse_args()

    # add current folder as fallback output folder
    if args.out is None:
        output_folder = os.path.dirname(os.path.realpath(__file__))
    else:
        output_folder = args.out
    
    if os.path.isdir(output_folder) is False:
        exit("supplied path is not a folder")

    if args.all_albums is False:
        if not (args.uris and args.uris.strip()):
            exit("uris are blank")
        else:
            uri_list = args.uris.split(",")

        # SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET need to be exported first
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    else:
        scope = "user-library-read"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope=scope, redirect_uri="http://127.0.0.1:9090"))

        # 50 item limit on getting saved albums, this adds the uris in chunks to uri_list
        items = True
        offset = 0
        uri_list = []
        while items:
            results = sp.current_user_saved_albums(limit=50, offset=offset)
            for album in results["items"]:
                uri_list.append(album["album"]["uri"])
            offset+=50
            if len(results["items"])==0:
                items = False

    generate_album_codes(output_folder, uri_list, sp)
