"""Tests for SpotifyCodeGen."""

from pathlib import Path

import pytest

from spotifycodegen.main import SpotifyCodeGen


@pytest.fixture
def artist_uri() -> str:
    """Pytest fixture for artist uri."""
    return "spotify:artist:5AyEXCtu3xnnsTGCo4RVZh"


@pytest.fixture
def album_uri() -> str:
    """Pytest fixture for album uri."""
    return "spotify:album:2S3289mypNw2zP0OpFexMb"


@pytest.fixture
def track_uri() -> str:
    """Pytest fixture for track uri."""
    return "spotify:track:74tDlAxO8vGECwUCaZHujI"


@pytest.fixture
def artist_url() -> str:
    """Pytest fixture for artist url."""
    return "https://open.spotify.com/artist/5AyEXCtu3xnnsTGCo4RVZh?si=Zu-zX5YTQHW97PaDbVY_Eg"


@pytest.fixture
def album_url() -> str:
    """Pytest fixture for album url."""
    return "https://open.spotify.com/album/2S3289mypNw2zP0OpFexMb?si=pl3A3Y5bQUmqZFmUGWTLJw"


@pytest.fixture
def track_url() -> str:
    """Pytest fixture for track url."""
    return "https://open.spotify.com/track/74tDlAxO8vGECwUCaZHujI?si=703973a3d84c4187"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Pytest fixture for creating a temparary output directory."""
    d = tmp_path / "output_dir"
    d.mkdir()
    return d


def count_files(dir: Path) -> int:
    """Count amount of files in given directory."""
    i = 0
    for _file in dir.iterdir():
        i += 1
    return i


def test_url_to_uri(
    artist_uri: str,
    album_uri: str,
    track_uri: str,
    artist_url: str,
    album_url: str,
    track_url: str,
    output_dir: Path,
) -> None:
    """Tests for correct conversion from URL to URI."""
    scg = SpotifyCodeGen(output_dir)
    assert scg._url_to_uri(artist_url) == artist_uri
    assert scg._url_to_uri(album_url) == album_uri
    assert scg._url_to_uri(track_url) == track_uri

    # bad input: no url
    with pytest.raises(Exception) as exc_info:
        scg._url_to_uri("no_url_as_input")
    assert str(exc_info.value) == "couldn't extract uri from: no_url_as_input"


def test_query_to_uri(
    output_dir: Path, artist_uri: str, album_uri: str, track_uri: str
) -> None:
    """Tests for correct conversion from query to URI."""
    scg = SpotifyCodeGen(output_dir=output_dir)
    assert scg._query_to_uri("duster", "artist") == artist_uri
    assert scg._query_to_uri("duster stratosphere", "album") == album_uri
    assert scg._query_to_uri("moon age duster", "track") == track_uri

    # bad search type
    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("asdfdasfdsafdsafasf", "bad_search_type")
    assert (
        str(exc_info.value)
        == "please provide a correct search type: artist, album, track!"
    )

    # empty query
    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("", "album")
    assert str(exc_info.value) == "please provide a valid search term!"

    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("   ", "album")
    assert str(exc_info.value) == "please provide a valid search term!"


def test_generate_codes(
    output_dir: Path, track_uri: str, album_uri: str, artist_uri: str
) -> None:
    """Tests for generation of codes from list of URIs."""
    # with empy list
    scg = SpotifyCodeGen(output_dir=output_dir)
    scg.gen_codes_uris([])
    assert count_files(output_dir) == 0

    # with one none in uri
    uri_list = [track_uri, artist_uri]
    fname_list = [x.replace(":", "-") + ".png" for x in [track_uri, artist_uri]]

    scg = SpotifyCodeGen(output_dir=output_dir)
    scg.gen_codes_uris(uri_list)

    for fname in fname_list:
        tmp_path = output_dir / fname
        assert tmp_path.exists()

    # valid input
    uri_list = [track_uri, album_uri, artist_uri]
    fname_list = [x.replace(":", "-") + ".png" for x in uri_list]

    scg = SpotifyCodeGen(output_dir=output_dir)
    scg.gen_codes_uris(uri_list)

    for fname in fname_list:
        tmp_path = output_dir / fname
        assert tmp_path.exists()


def test_missing_scopes(output_dir: Path) -> None:
    """Tests for correct behavior when scopes are missing."""
    scg = SpotifyCodeGen(output_dir=output_dir)

    with pytest.raises(Exception) as exc_info:
        scg._get_saved_album_uris()
    assert (
        str(exc_info.value) == "the following scopes need to be set: user-library-read"
    )

    with pytest.raises(Exception) as exc_info:
        scg._get_50_artist_uris()
    assert (
        str(exc_info.value) == "the following scopes need to be set: user-follow-read"
    )


def test_gen_codes_urls(
    output_dir: Path, track_url: str, album_url: str, artist_url: str
) -> None:
    """Tests generation of codes from list of URLs."""
    url_list = [track_url, album_url, artist_url]

    # empty input
    scg = SpotifyCodeGen(output_dir=output_dir)
    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_urls([""])
    assert str(exc_info.value) == "couldn't extract uri from: "
    assert count_files(output_dir) == 0

    # valid input
    scg = SpotifyCodeGen(output_dir=output_dir)
    scg.gen_codes_urls(url_list)
    assert count_files(output_dir) == 3


def test_gen_codes_query(output_dir: Path) -> None:
    """Test for generating codes with query."""
    scg = SpotifyCodeGen(output_dir=output_dir)

    # bad search type
    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("duster", "bad__search_type")
    assert (
        str(exc_info.value)
        == "please provide a correct search type: artist, album, track!"
    )

    # empty input
    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("", "artist")
    assert str(exc_info.value) == "please provide a valid search term!"

    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("    ", "artist")
    assert str(exc_info.value) == "please provide a valid search term!"

    # valid input
    scg = SpotifyCodeGen(output_dir=output_dir)
    scg.gen_codes_query("duster", "artist")
    assert count_files(output_dir) == 1
