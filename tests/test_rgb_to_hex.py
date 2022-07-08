from spotifyartcode.cli.sac import _rgb_to_hex


def test_rgb_to_hex():
    assert _rgb_to_hex((0,0,0)) == "000000"
    assert _rgb_to_hex((255,0,0)) == "ff0000"
