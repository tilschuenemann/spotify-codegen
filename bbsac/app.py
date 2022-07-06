from dash import Dash, dcc, html, Input, Output, State
from bbsac import get_album_code
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

from urllib.request import urlopen
import base64
import re

app = Dash(__name__, external_stylesheets=[
           "https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css"])

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
    html.Div(
        ["Search By", dcc.Dropdown(id="search_by", options=[
            "metadata", "uri"], value="metadata"),
         ], className="w-64"),
    html.Div([
        html.Div([html.H1("Search by Metadata"),
                  dcc.Dropdown(id="search_type", options=[
                      "album", "artist", "track"]),
                  dcc.Input(id="search_general", type="text", debounce=True,
                            placeholder="General Search:"),
                  html.Button('Search!', id='search-trigger',
                              n_clicks=0, className="bg-emerald-400 w-64"),
                  ], className="grid align-center"),
        html.Div([html.H1("Search by URI"),
                  dcc.Input(id="search_uri", type="text", debounce=True,
                            placeholder="Enter Spotify Album URI here!")]),
        html.Div(id="picture"),

        dcc.Store(id="search_uriresult")], className="grid")])


sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())


@ app.callback(Output("picture", "children"),
               State("search_by", "value"),
               State("search_type", "value"),
               State("search_uri", "value"),
               State("search_general","value"),
               Input('search-trigger', 'n_clicks'),
               
               prevent_initial_call=True)
def search(search_by, search_type, search_uri,search_general, n_clicks,):

    if search_by == "uri":
        if search_uri is not None:
            uri = search_uri
        else:
            return html.Div()

    elif search_by == "metadata":
        if search_type is None or search_general is None:
            return html.Div()

        results = sp.search(q=search_general, limit=1, type=search_type)
        if search_type == "album":
            uri = results["albums"]["items"][0]["uri"]
        elif search_type == "track":
            uri = results["tracks"]["items"][0]["uri"]
        elif search_type == "artist":
            uri = results["artists"]["items"][0]["uri"]

    img = get_album_code(uri, sp)
    return html.Img(src=img)


if __name__ == "__main__":
    app.run_server(debug=True)
