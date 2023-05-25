# spotify-codegen

[![PyPI](https://img.shields.io/pypi/v/spotify-codegen.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/spotify-codegen.svg)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/spotify-codegen)][python version]
[![License](https://img.shields.io/pypi/l/spotify-codegen)][license]

[![Read the documentation at https://spotify-codegen.readthedocs.io/](https://img.shields.io/readthedocs/spotify-codegen/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/tilschuenemann/spotify-codegen/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/tilschuenemann/spotify-codegen/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi_]: https://pypi.org/project/spotify-codegen/
[status]: https://pypi.org/project/spotify-codegen/
[python version]: https://pypi.org/project/spotify-codegen
[read the docs]: https://spotify-codegen.readthedocs.io/
[tests]: https://github.com/tilschuenemann/spotify-codegen/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/tilschuenemann/spotify-codegen
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

Spotify stopped giving users an easy way to grab the song, artist or album artwork with the respective Spotify Code - `spotify-codegen` to the rescue!

You can stitch the album | track | artist artwork with the Spotify Code by supplying:

- URL(s)
- URI(s)
- a search query

It's also possible to use create stitches for:

- all of your saved albums
- 50 followed artists (limit imposed by Spotify API)

## Requirements

To use the Spotify API, you'll have to login using your credentials and create an app. That apps ID and secret need to be specified as environment variables:

```console
$ export SPOTIPY_CLIENT_ID="your_client_id"
$ export SPOTIPY_CLIENT_SECRET="your_client_secret"
```

You can now use both the CLI and the Python API!

## Installation

You can install _spotify-codegen_ via [pip] from [PyPI]:

```console
$ pip install spotify-codegen
```

## Usage

Please see the [Command-line Reference] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_spotify-codegen_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[file an issue]: https://github.com/tilschuenemann/spotify-codegen/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/tilschuenemann/spotify-codegen/blob/main/LICENSE
[contributor guide]: https://github.com/tilschuenemann/spotify-codegen/blob/main/CONTRIBUTING.md
[command-line reference]: https://spotify-codegen.readthedocs.io/en/latest/usage.html
