from spotifyartcode.cli.sac import get_art_with_code
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from PIL import Image
from PIL import ImageChops

def test_get_art_with_code():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    img_artist = get_art_with_code("spotify:artist:1aSxMhuvixZ8h9dK9jIDwL",sp)
    img_album = get_art_with_code("spotify:album:5BWl0bB1q0TqyFmkBEupZy",sp)
    img_track = get_art_with_code("spotify:track:75FEaRjZTKLhTrFGsfMUXR",sp)

    exp_img_artist = Image.open("tests\\spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png")
    exp_img_album = Image.open("tests\\spotify-album-5BWl0bB1q0TqyFmkBEupZy.png")
    exp_img_track = Image.open("tests\\spotify-track-75FEaRjZTKLhTrFGsfMUXR.png")

    diff_artist = ImageChops.difference(img_artist, exp_img_artist)
    diff_album = ImageChops.difference(img_album, exp_img_album)
    diff_track = ImageChops.difference(img_track, exp_img_track)

    assert diff_artist.getbbox() is None
    assert diff_album.getbbox() is None
    assert diff_track.getbbox() is None

def test_get_art_with_code_blankuri():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    img_artist = get_art_with_code("",sp)
    assert img_artist is None

def test_get_art_with_code_baduri():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    img_artist = get_art_with_code("spotify:track:0000000000000000000000",sp)
    assert img_artist is None