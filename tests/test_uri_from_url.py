from spotifyartcode.cli.sac import uri_from_url

def test_uri_from_url():
    assert uri_from_url("https://open.spotify.com/artist/1aSxMhuvixZ8h9dK9jIDwL?si=661IYYYSS3y4KGWDTCtLUg") == "spotify:artist:1aSxMhuvixZ8h9dK9jIDwL"
    assert uri_from_url("https://open.spotify.com/album/5BWl0bB1q0TqyFmkBEupZy?si=AIoP41dtQaaaPHQ0E4le2A") == "spotify:album:5BWl0bB1q0TqyFmkBEupZy"
    assert uri_from_url("https://open.spotify.com/track/75FEaRjZTKLhTrFGsfMUXR?si=c856ab1d654b4141") == "spotify:track:75FEaRjZTKLhTrFGsfMUXR"
    
def test_uri_from_url_bad_input():
    assert uri_from_url("abcdefgh") == None

def test_uri_from_url_blank_input():
    assert uri_from_url("") == None