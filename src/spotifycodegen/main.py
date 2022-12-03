"""SpotifyCodeGen."""
import io
import os
import pathlib
import re
from typing import List
from urllib.request import urlopen

import spotipy
import tqdm
from colorthief import ColorThief
from PIL import Image
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


class SpotifyCodeGen:
    """SpotifyCodeGen."""

    def __init__(
        self, output_dir: pathlib.Path | None = None, scopes: List[str] | None = None
    ):
        """Initializes Spotify Code-Generator.

        Args:
          output_dir: directory where generated codes should be written to.
          scopes: list of OAuth2 scopes to be passed.
        """
        if scopes is None:
            self.scopes = []
            auth_manager = SpotifyClientCredentials()
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
        else:
            self.scopes = scopes
            self.sp = spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    scope=scopes, redirect_uri="http://127.0.0.1:9090"
                )
            )

        if output_dir is None or output_dir.is_dir() is False:
            self.OUTPUT_DIR = pathlib.Path(os.getcwd())
        else:
            self.OUTPUT_DIR = output_dir

    def __check_query(self, search_term: str, search_type: str) -> None:
        """Checks non-empty search term and a valid search type.

        Args:
          search_term: natural language query
          search_type: either 'track', 'artist' or 'album'
        """
        if not (search_term and search_term.strip()):
            raise Exception("please provide a valid search term!")
        elif search_type not in ["artist", "album", "track"]:
            raise Exception(
                "please provide a correct search type: artist, album, track!"
            )

    def gen_codes_uris(self, uris: List[str]) -> None:
        """Generates Spotify Codes for given URIs.

        Args:
          uris: list of Spotify URIs
        """
        for uri in tqdm.tqdm(uris):
            if uri is None:
                continue
            im = self._generate_code(uri)
            if im is not None:
                fname = uri.replace(":", "-") + ".png"
                im.save(self.OUTPUT_DIR / fname)

    def gen_codes_urls(self, urls: List[str]) -> None:
        """Generates Spotify Codes for given URLs.

        Args:
          urls: list of Spotify URLs
        """
        uris = [self._url_to_uri(x) for x in urls]
        self.gen_codes_uris(uris)

    def gen_codes_query(self, search_term: str, search_type: str) -> None:
        """Generates a Spotify Code for given search_term and search type.

        Args:
          search_term: natural language query
          search_type: either 'track', 'artist' or 'album'
        """
        self.__check_query(search_term, search_type)
        uri = self._query_to_uri(search_term, search_type)
        self.gen_codes_uris([uri])

    def gen_codes_album_lib(self) -> None:
        """Generates Spotify Codes for all liked albums."""
        uri_list = self._get_saved_album_uris()
        self.gen_codes_uris(uri_list)

    def gen_codes_followed_artists(self) -> None:
        """Generates Spotify Codes for 50 followed artists."""
        uri_list = self._get_50_artist_uris()
        self.gen_codes_uris(uri_list)

    def _url_to_uri(self, search_url: str) -> str:
        """Extracts URI from URL.

        Raises:
          Exception if extract wasn't found.
        """
        result = re.match(
            r".*\.com/(?P<search_type>album|artist|track)/(?P<uri>[A-Za-z0-9]{22})\?si=.*$",
            search_url,
        )
        if result is not None:
            search_type = result.group("search_type")
            search_suffix = result.group("uri")
            uri = f"spotify:{search_type}:{search_suffix}"
        else:
            raise Exception(f"couldn't extract uri from: {search_url}")
        return uri

    def _query_to_uri(self, search_term: str, search_type: str) -> str:
        """Searchs with a natural language query for an item and returns an URI.

        Args:
          search_term: natural language query
          search_type: either 'track', 'artist' or 'album'

        Raises:
          Exception if Spotify search didn't yield a result.
        """
        self.__check_query(search_term, search_type)

        try:
            results = self.sp.search(q=search_term, limit=1, type=search_type)
            uri = str(results[f"{search_type}s"]["items"][0]["uri"])
        except Exception as exc:
            raise Exception(
                f"couldn't find a matching {search_type}: {search_term}"
            ) from exc
        return uri

    def _generate_code(self, uri: str) -> Image.Image:
        """Generates a Spotify Code for a given Spotify URI.

        Args:
          uri: Spotify URI

        Raises:
          Exception if uri is not for an artist, album or track.

        """
        if re.match(r"spotify:track:[A-Za-z0-9]{22}", uri):
            track = self.sp.track(uri)
            album_uri = track["album"]["uri"]
            results = self.sp.album(album_uri)
        elif re.match(r"spotify:artist:[A-Za-z0-9]{22}", uri):
            results = self.sp.artist(uri)
        elif re.match(r"spotify:album:[A-Za-z0-9]{22}", uri):
            results = self.sp.album(uri)
        else:
            raise Exception(
                "supplied uri doesn't match artist, album or track pattern!"
            )

        link_to_cover = results["images"][0]["url"]
        cover_size = results["images"][0]["height"]
        cover_image = Image.open(urlopen(link_to_cover))  # noqa:S310

        with io.BytesIO() as file_object:
            cover_image.save(file_object, "PNG")
            cf = ColorThief(file_object)
            dominant_color_rgb = cf.get_color(quality=1)

        dominant_color_hex = "%02x%02x%02x" % dominant_color_rgb
        code_color = (
            "black"
            if (dominant_color_rgb[0] + dominant_color_rgb[1] + dominant_color_rgb[2])
            / 3
            > 127
            else "white"
        )
        uri_call = uri.replace(":", "%3A")

        url = f"https://www.spotifycodes.com/downloadCode.php?uri=png%2F{dominant_color_hex}%2F{code_color}%2F{cover_size}%2F{uri_call}"  # noqa
        album_code = Image.open(urlopen(url))  # noqa:S310

        final_height = album_code.size[1] + cover_size
        im = Image.new(mode="RGB", size=(cover_size, final_height))
        im.paste(cover_image, (0, 0))
        im.paste(album_code, (0, cover_size))
        return im

    def _get_saved_album_uris(self) -> List[str]:
        """Gets list of all followed artist URIs from Spotify user.

        Raises:
          Exception if OAuth2 scope "user-library-read" is missing.
        """
        if "user-library-read" not in self.scopes:
            raise Exception("the following scopes need to be set: user-library-read")
        items = True
        offset = 0
        uri_list = []
        while items:
            results = self.sp.current_user_saved_albums(limit=50, offset=offset)
            for album in results["items"]:
                uri_list.append(album["album"]["uri"])
            offset += 50
            if len(results["items"]) == 0:
                items = False
        return uri_list

    def _get_50_artist_uris(self) -> List[str]:
        """Gets list of 50 artist URIs from Spotify user.

        Raises:
          Exception if OAuth2 scope "user-follow-read" is missing.
        """
        if "user-follow-read" not in self.scopes:
            raise Exception("the following scopes need to be set: user-follow-read")
        uri_list = []
        results = self.sp.current_user_followed_artists(limit=50)
        for artist in results["artists"]["items"]:
            uri_list.append(artist["uri"])
        return uri_list
