from spotifyartcode.cli.sac import save_art_with_code
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from PIL import Image
from PIL import ImageChops

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def test_save_art_with_code(tmp_path):
    # create empty output dir
    d = tmp_path / "output"
    d.mkdir()
    uri1 = "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
    assert len(list(d.glob('*.*'))) == 0

    # save one item
    save_art_with_code(str(d),[uri1],sp)
    output_folder_contents = list(d.glob('*.*'))
    
    # check output folder contents
    assert len(output_folder_contents) == 1

    # check for correct image
    img_artist = Image.open(output_folder_contents[0])
    exp_img_artist = Image.open("tests/spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png")
    diff_artist = ImageChops.difference(img_artist, exp_img_artist)
    assert diff_artist.getbbox() is None

def test_save_art_with_code_emptyurilist(tmp_path):
    d = tmp_path / "output"
    d.mkdir()
    assert len(list(d.glob('*.*'))) == 0
    save_art_with_code(str(d),[],sp)
    assert len(list(d.glob('*.*'))) == 0

