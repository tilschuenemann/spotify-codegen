import pytest
from spotifycodegen.main import spotifycodegen


@pytest.fixture
def artist_uri():
    return "spotify:artist:5AyEXCtu3xnnsTGCo4RVZh"


@pytest.fixture
def album_uri():
    return "spotify:album:2S3289mypNw2zP0OpFexMb"


@pytest.fixture
def track_uri():
    return "spotify:track:74tDlAxO8vGECwUCaZHujI"


@pytest.fixture
def artist_url():
    return "https://open.spotify.com/artist/5AyEXCtu3xnnsTGCo4RVZh?si=Zu-zX5YTQHW97PaDbVY_Eg"


@pytest.fixture
def album_url():
    return "https://open.spotify.com/album/2S3289mypNw2zP0OpFexMb?si=pl3A3Y5bQUmqZFmUGWTLJw"


@pytest.fixture
def track_url():
    return "https://open.spotify.com/track/74tDlAxO8vGECwUCaZHujI?si=703973a3d84c4187"


@pytest.fixture
def output_dir(tmp_path):
    d = tmp_path / "output_dir"
    d.mkdir()
    return d


def test_url_to_uri(artist_uri, album_uri, track_uri, artist_url, album_url, track_url, output_dir):
    scg = spotifycodegen(output_dir)
    assert scg._url_to_uri(artist_url) == artist_uri
    assert scg._url_to_uri(album_url) == album_uri
    assert scg._url_to_uri(track_url) == track_uri

    assert scg._url_to_uri("abcdef") == None


def test_query_to_uri(output_dir, artist_uri, album_uri, track_uri):
    scg = spotifycodegen(output_dir=output_dir)
    assert scg._query_to_uri("duster", "artist") == artist_uri
    assert scg._query_to_uri("duster stratosphere", "album") == album_uri
    assert scg._query_to_uri("moon age duster", "track") == track_uri

    assert scg._query_to_uri("asdfdasfdsafdsafasf", "track") == None
    assert scg._query_to_uri("moon age duster", "somethingelse") == None


def test_generate_codes(output_dir, track_uri, album_uri, artist_uri):
    uri_list = [track_uri, album_uri, artist_uri]
    fname_list = [x.replace(":", "-") + ".png" for x in uri_list]

    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_uris(uri_list)

    for fname in fname_list:
        tmp_path = output_dir / fname
        assert tmp_path.exists()
