from spotifyartcode.cli.sac import main
import pytest 
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from PIL import Image
from PIL import ImageChops
import os
import pathlib

def test_argparse_noargs(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main()
    captured = capsys.readouterr()
    assert captured.err == ("usage: pytest [-h] [-o OUT] (--u URIS | --a)\n"+
    "pytest: error: one of the arguments --u --a is required\n")

def test_argparse_blankuri(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        main(["--u",""])
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "uris are blank"

def test_argparse_1uri(tmp_path):
    # create empty output dir
    d = tmp_path / "output"
    d.mkdir()
    uri1 = "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
    assert len(list(d.glob('*.*'))) == 0

    # save one item
    main(["-o",str(d),"--u",uri1])

    output_folder_contents = list(d.glob('*.*'))
    
    # check output folder contents
    assert len(output_folder_contents) == 1

    # check for correct image
    img_artist = Image.open(output_folder_contents[0])
    exp_img_artist = Image.open("tests/spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png")
    diff_artist = ImageChops.difference(img_artist, exp_img_artist)
    assert diff_artist.getbbox() is None

def test_argparse_2uri(tmp_path):
    # create empty output dir
    d = tmp_path / "output"
    d.mkdir()
    uri1 = "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
    uri2 = "spotify:album:5BWl0bB1q0TqyFmkBEupZy"
    assert len(list(d.glob('*.*'))) == 0

    # save one item
    main(["-o",str(d),"--u",f"{uri1},{uri2}"])

    output_folder_contents = list(d.glob('*.*'))
    
    # check output folder contents
    assert len(output_folder_contents) == 2


    # check for correct images

    album_path = d / "spotify-album-5BWl0bB1q0TqyFmkBEupZy.png"
    artist_path = d / "spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png"
    img_album = Image.open(album_path)
    img_artist = Image.open(artist_path)
    exp_img_artist = Image.open("tests/spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png")
    exp_img_album = Image.open("tests/spotify-album-5BWl0bB1q0TqyFmkBEupZy.png")
    diff_artist = ImageChops.difference(img_artist, exp_img_artist)
    diff_album = ImageChops.difference(img_album, exp_img_album)
    assert diff_artist.getbbox() is None
    assert diff_album.getbbox() is None

# def test_argparse_defaultoutputfolder(tmp_path):
#     # TODO address this
#     d = pathlib.Path(os.getenv('PYTEST_CURRENT_TEST'))
#     uri1 = "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
#     output_folder_contents = list(d.glob("*.*"))
#     print(output_folder_contents)
#     # save one item
#     main(["--u",uri1])

#     # check for correct image
#     img_artist = Image.open(output_folder_contents[0])
#     exp_img_artist = Image.open("tests/spotify-artist-1aSxMhuvixZ8h9dK9jIDwL.png")
#     diff_artist = ImageChops.difference(img_artist, exp_img_artist)
#     assert diff_artist.getbbox() is None

