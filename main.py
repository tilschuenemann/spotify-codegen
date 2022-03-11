import spotipy
import wget
from colorthief import ColorThief
from PIL import Image
from spotipy.oauth2 import SpotifyClientCredentials

list_of_albums = ["spotify:album:3USQKOw0se5pBNEndu82Rb",]

# SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET need to be exported first
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

for album_uri in list_of_albums:

    ## get album cover and height from spotify API
    results = spotify.album(album_uri)

    link_to_cover = results["images"][0]["url"]
    cover_size = results["images"][0]["height"]

    wget.download(link_to_cover, out=f"{album_uri}.png",bar=None)

    ### get dominant color from cover
    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    color_thief = ColorThief(f"{album_uri}.png")
    dominant_color_rgb = color_thief.get_color(quality=1)
    dominant_color_hex = rgb_to_hex(dominant_color_rgb).replace("#", "")
    code_color = "white" if (dominant_color_rgb[0] 
                            + dominant_color_rgb[1] 
                            + dominant_color_rgb[2]) / 3 > 127 else "black"
    album_uri_call = album_uri.replace(":", "%3A")

    ## get spotify code 
    url = f"https://www.spotifycodes.com/downloadCode.php?uri=png%2F{dominant_color_hex}%2F{code_color}%2F{cover_size}%2F{album_uri_call}"

    wget.download(url, out = f"{album_uri}_code.png",bar=None)

    ## merge images
    album_art = Image.open(f"{album_uri}.png")
    album_code = Image.open(f"{album_uri}_code.png")

    # TODO investigate if rounding errors map code to a lesser image size
    final_height = int(cover_size*1.25)

    im = Image.new(mode="RGB", size=(cover_size, final_height))
    im.paste(album_art, (0,0))
    im.paste(album_code, (0,cover_size))
    im.save(f"x_{album_uri}.png")
