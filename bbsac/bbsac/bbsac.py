from colorthief import ColorThief
from PIL import Image
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import tqdm

import argparse
import io
import os
from urllib.request import urlopen


def rgb_to_hex(rgb):
    return "%02x%02x%02x" % rgb


def generate_album_codes(output_folder: str, album_uris: str):
    """Generates images for each supplied album_uri that merges
    the album cover and its Spotify code.

    Parameters
    -------
    output_folder: str
        folder to save results in
    album_uris: str
        list of album uris
    """
    if output_folder is None:
        output_folder = os.path.dirname(os.path.realpath(__file__))
    else:
        if os.path.isdir(output_folder) is False:
            print("supplied path is not a folder")
            exit()

    if not (album_uris and album_uris.strip()):
        exit("uris are blank")
    else:
        album_uris = album_uris.split(",")

    # SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET need to be exported first
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

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
        im.save(f"{output_folder}/{album_uri}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        dest="uris",
        nargs=1,
        type=str,
        required=True,
        help="comma separated Spotify album URI(s)",
    )
    parser.add_argument(
        "-o", dest="out", type=str, required=False, help="path to output folder"
    )
    args = parser.parse_args()

    generate_album_codes(args.out, args.uris[0])
