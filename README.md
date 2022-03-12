# bring back spotify album + code

![preview](preview.png)

Spotify used to display its album art and spotify code in one picture after clicking the kebab menu. This still works on mobile, but not in the web player nor in the desktop version.

I've already started pinning scannable album covers on my wall and wanted to continue, thus creating this hacked-together script.

# Prerequisites and Dependencies

This was written in Python and works in Python 3.10.2 using the following dependencies:
* spotipy
* colorthief
* pil
* wget

Could it be done in a leaner way? Yes!

# Usage

You'll need the URI of each album and enter it into the list_of_albums variable. This will change in the future, where commandline arguments will be read.

To use the Spotify API, you'll have to create an app and export SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET.