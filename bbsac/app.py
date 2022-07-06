from dash import Dash, dcc, html, Input, Output, State
from bbsac import get_art_with_code
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

from urllib.request import urlopen
import base64
import re

app = Dash("Spotify Art+Code",
           external_scripts=["https://cdn.tailwindcss.com"])

server = app.server

app.index_string = '''
        <!DOCTYPE html>
        <html>
        <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-FGF24ELJ9L"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-FGF24ELJ9L');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.Div([
        html.H1("Append Album / Artist / Song Art with Spotify Code!",
                className="text-4xl text-green-500"),

        # Search By
        html.Div(
            [html.H1("Search By", className="text-xl text-white"),
             dcc.Dropdown(
                id="search_by",
                options=["metadata", "uri"],
                value="metadata",
                clearable=False,
                className="h-10"),
             ], className="grid align-center space-y-2 w-64 p-2"),

        # Search By Metadata
        html.Div(
            [html.H1("Search by Metadata", className="text-xl text-white"),
             dcc.Dropdown(id="search_type",
                          options=["album", "artist", "track"],
                          value="album",
                          clearable=False,
                          className="h-10"),
             dcc.Input(id="search_general",
                       type="text",
                       debounce=True,
                       placeholder="General Search:",
                       className="h-10 p-2")
             ], className="grid align-center space-y-2 w-64 p-2"),
        # Search by URI
        html.Div(
            [html.H1("Search by URI", className="text-xl text-white"),
             dcc.Input(id="search_uri",
                       type="text",
                       debounce=True,
                       placeholder="Spotify URI",
                       className="h-10 p-2")
             ],
            className="grid align-center space-y-4 w-64 p-2"),
        html.Div([html.H1("Search by URL",className="text-xl text-white"),
        dcc.Input(id="search_url",
                       type="text",
                       debounce=True,
                       placeholder="Spotify URL",
                       className="h-10 p-2")
                    ],className="grid align-center space-y-4 w-64 p-2"),
        # Search Button
        html.Div([
            html.Button(html.H1('Search!', className="text-xl font-bold"),
                        id='search-trigger',
                        n_clicks=0,
                        className="bg-green-400 rounded-lg h-10 w-64")
                        ]),
        html.Div([html.P("This is hobby project!", className="text-white")])], className="space-y-4"),

    # Result
    html.Div(
        [html.Div(id="picture",
                  className="object-contain drop-shadow-[0_8px_5px_rgba(34,197,94,0.1)]")
         ], className="h-screen"),
    dcc.Store(id="search_uriresult")
], className="grid grid-cols-2 w-screen h-fit bg-neutral-900 p-4")


sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())


@ app.callback(Output("picture", "children"),
               State("search_by", "value"),
               State("search_type", "value"),
               State("search_uri", "value"),
               State("search_general", "value"),
               Input('search-trigger', 'n_clicks'),

               prevent_initial_call=True)
def search(search_by, search_type, search_uri, search_general, n_clicks,):

    if search_by == "uri":
        if search_uri is not None:
            uri = search_uri
        else:
            return html.Div()

    elif search_by == "metadata":
        if search_general is None:
            return html.Div()

        results = sp.search(q=search_general, limit=1, type=search_type)
        if search_type == "album":
            uri = results["albums"]["items"][0]["uri"]
        elif search_type == "track":
            uri = results["tracks"]["items"][0]["uri"]
        elif search_type == "artist":
            uri = results["artists"]["items"][0]["uri"]

    elif search_by == "url":
        #re.match(r".*album/([A-Za-z0-9]{22}).*", "https://open.spotify.com/album/6A0PfJD05hLKUNXAmXr7I5?si=hxYYJZwlS-OR5JUY7-_BHw")
        None
    img = get_art_with_code(uri, sp)
    return html.Img(src=img)


if __name__ == "__main__":
    app.run_server(debug=True)
