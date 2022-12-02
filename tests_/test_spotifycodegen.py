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

    assert scg._url_to_uri("no_url_as_input") == None


def test_query_to_uri(output_dir, artist_uri, album_uri, track_uri):
    scg = spotifycodegen(output_dir=output_dir)
    assert scg._query_to_uri("duster", "artist") == artist_uri
    assert scg._query_to_uri("duster stratosphere", "album") == album_uri
    assert scg._query_to_uri("moon age duster", "track") == track_uri

    # bad search type
    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("asdfdasfdsafdsafasf", "bad_search_type")
    assert str(exc_info.value) == "please provide a correct search type: artist, album, track!"

    # empty query
    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("", "album")
    assert str(exc_info.value) == "please provide a valid search term!"

    with pytest.raises(Exception) as exc_info:
        scg._query_to_uri("   ", "album")
    assert str(exc_info.value) == "please provide a valid search term!"


def test_generate_codes(output_dir, track_uri, album_uri, artist_uri):
    # with empy list
    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_uris([])

    i = 0
    for file in output_dir.iterdir():
        i += 1
    assert i == 0

    # with one none in uri
    uri_list = [track_uri, None, artist_uri]
    fname_list = [x.replace(":", "-") + ".png" for x in [track_uri, artist_uri]]

    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_uris(uri_list)

    for fname in fname_list:
        tmp_path = output_dir / fname
        assert tmp_path.exists()

    # valid input
    uri_list = [track_uri, album_uri, artist_uri]
    fname_list = [x.replace(":", "-") + ".png" for x in uri_list]

    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_uris(uri_list)

    for fname in fname_list:
        tmp_path = output_dir / fname
        assert tmp_path.exists()


def test_missing_scopes(output_dir):
    scg = spotifycodegen(output_dir=output_dir)

    with pytest.raises(Exception) as exc_info:
        scg._get_saved_album_uris()
    assert str(exc_info.value) == "the following scopes need to be set: user-library-read"

    with pytest.raises(Exception) as exc_info:
        scg._get_50_artist_uris()
    assert str(exc_info.value) == "the following scopes need to be set: user-follow-read"


def test_gen_codes_urls(output_dir, track_url, album_url, artist_url):
    url_list = [track_url, album_url, artist_url]

    # empty input
    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_urls([])

    i = 0
    for file in output_dir.iterdir():
        i += 1
    assert i == 0

    # valid input
    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_urls(url_list)

    i = 0
    for file in output_dir.iterdir():
        i += 1
    assert i == 3


def test_gen_codes_query(output_dir):
    scg = spotifycodegen(output_dir=output_dir)

    # bad search type
    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("duster", "bad__search_type")
    assert str(exc_info.value) == "please provide a correct search type: artist, album, track!"

    # empty input
    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("", "artist")
    assert str(exc_info.value) == "please provide a valid search term!"

    with pytest.raises(Exception) as exc_info:
        scg.gen_codes_query("    ", "artist")
    assert str(exc_info.value) == "please provide a valid search term!"

    # valid input
    scg = spotifycodegen(output_dir=output_dir)
    scg.gen_codes_query("duster", "artist")

    i = 0
    for file in output_dir.iterdir():
        i += 1
    assert i == 1
