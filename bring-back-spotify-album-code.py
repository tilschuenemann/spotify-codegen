import spotipy
from colorthief import ColorThief
from PIL import Image
from spotipy.oauth2 import SpotifyClientCredentials
import argparse
import os
import time
from urllib.request import urlopen
import io

start = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("--out",dest="out",type=str,required=True,help="filepath for output")
parser.add_argument("--uris",dest="uris",nargs="+",type=str,required=True, help="Spotify album URI(s)")
args = parser.parse_args()

if(os.path.isdir(args.out)==False):
    print("supplied path is not a folder")
    exit()

# SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET need to be exported first
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

for album_uri in args.uris:
    
    cover_time_start = time.time()

    ## get album cover from spotify API
    results = spotify.album(album_uri)
    link_to_cover = results["images"][0]["url"]
    cover_size = results["images"][0]["height"]
    album_art = Image.open(urlopen(link_to_cover))

    cover_time_end = time.time()
    print(f"{album_uri}\t[x][ ][ ]\t{cover_time_end-cover_time_start:.1f}s\tdownloaded cover")

    ### get dominant color from cover
    # this doesnt write to disc and still allows colorthief to grab most dominant color
    with io.BytesIO() as file_object:
        album_art.save(file_object, "PNG")
        cf = ColorThief(file_object)
        dominant_color_rgb = cf.get_color(quality=1)

    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb
    dominant_color_hex = rgb_to_hex(dominant_color_rgb).replace("#", "")
    code_color = "white" if (dominant_color_rgb[0] 
                            + dominant_color_rgb[1] 
                            + dominant_color_rgb[2]) / 3 > 127 else "black"
    album_uri_call = album_uri.replace(":", "%3A")

    ## get spotify code 
    code_time_start = time.time()
    url = f"https://www.spotifycodes.com/downloadCode.php?uri=png%2F{dominant_color_hex}%2F{code_color}%2F{cover_size}%2F{album_uri_call}"
    album_code = Image.open(urlopen(url))

    code_time_end = time.time()
    print(f"{album_uri}\t[x][x][ ]\t{code_time_end-code_time_start:.1f}s\tdownloaded spotify code")

    ## merge images
    merge_start = time.time()
    final_height = album_code.size[1]+cover_size

    im = Image.new(mode="RGB", size=(cover_size, final_height))
    im.paste(album_art, (0,0))
    im.paste(album_code, (0,cover_size))
    im.save(f"{args.out}x_{album_uri}.png")
    merge_end = time.time()
    print(f"{album_uri}\t[x][x][x]\t{merge_end-merge_start:.1f}s\tmerged images")

end = time.time()
print(f"finished in {end-start:.1f}s")