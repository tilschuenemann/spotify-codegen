# bring back spotify album + code

![preview](preview.png)

Spotify used to display its album art and spotify code in one picture after clicking the kebab menu. This still works on mobile, but not in the web player nor in the desktop version.

I've already started pinning scannable album covers on my wall and wanted to continue, thus creating this hacked-together script.

# Usage

```bash
/bin/python bbsac/bbsac.py -h
usage: bbsac.py [-h] -u URIS [URIS ...] [-o OUT]

options:
  -h, --help          show this help message and exit
  -u URIS [URIS ...]  Spotify album URI(s)
  -o OUT              path to output folder
```