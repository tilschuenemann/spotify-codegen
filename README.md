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

Spotify removed the feature to get a stitched image of an album / artist / track cover with their own Spotify Code. This package mimicks that behaviour and creates stitches, based on supplied

- URL
- URI
- query

It's also possible to use create stitches for:

- all saved albums
- 50 followed artists (limit imposed by Spotify API)

[You can also try the Streamlit showcase here.](https://tilschuenemann-showcase-showcasesstart-0ndtb3.streamlit.app/spotify_codegen)

## Requirements

You'll need to have a Spotify Client ID & Secret in order to make API requests. Specify as environment variable like this:

```console
$ export SPOTIPY_CLIENT_ID="your_client_id"
$ export SPOTIPY_CLIENT_ID="your_client_secret"
```

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
