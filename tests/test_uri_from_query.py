from spotifyartcode.cli.sac import uri_from_query
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

def test_uri_from_query():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    assert uri_from_query("kate bush","artist", sp) == "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
    assert uri_from_query("kate bush hounds of love remaster","album", sp) == "spotify:album:3OYnManu1Nlxnw9OMng7BH"
    assert uri_from_query("kate bush running up that hill remaster","track", sp) == "spotify:track:29d0nY7TzCoi22XBqDQkiP"

def test_uri_from_query_badinput():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    assert uri_from_query("abcdefgasdfasfasf","track", sp) is None

def test_uri_from_query_blankinput():
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    assert uri_from_query("","track", sp) is None