from dash import Dash, dcc, html, Input, Output, State

from spotifyartcode.cli.sac import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image
from urllib.request import urlopen
import base64
import re


placeholder = Image.open("spotifyartcode/app/assets/katebush.png")

app = Dash("Spotify Art+Code",
           external_scripts=["https://cdn.tailwindcss.com", "https://cdn.jsdelivr.net/npm/tw-elements/dist/js/index.min.js"],
           assets_folder="assets"           
           )
app.config.suppress_callback_exceptions = True
app.title = "Spotify Art+Code"
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


sp = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())

app.layout = html.Div([
    # Sidebar
    html.Div([
        # Content Start
        html.Div([
            # Search by
            html.P("Search by", className="text-xl text-white"),
                dcc.Dropdown(
                        id="search_by",
                        options=["Metadata", "URI", "URL"],
                        value="Metadata",
                        clearable=False, 
                        className="pb-2"),
            # menu
            html.Div([
                html.Div(id="sidebar_metadata"),
                html.Div(id="sidebar_uri"),
                html.Div(id="sidebar_url"),
            
            ],id="menu_container"),
            # Search Button
            html.Button(html.H1('Search!', className="text-xl font-bold"),
                    id='search-trigger',
                    n_clicks=0,
                    className="bg-green-400 rounded-xl w-full h-12"),
                
        ],className="grid content-start space-y-2"),
        # Content End
        html.Div([
            html.Div(html.A('Personal Blog', href="https://tilschuenemann.github.io/",target="_blank",className="text-xl text-white font-bold text-center"),
                    className="grid bg-neutral-900 rounded-lg w-full h-12 items-center"),
            html.Div(html.A('Project on Github', href="https://github.com/tilschuenemann/bring-back-spotify-album-code",target="_blank",className="text-xl text-white font-bold text-center"),
                    className="grid bg-neutral-900 rounded-lg w-full h-12 items-center"),
            html.Div(html.A('Buy me a coffee!', href="https://www.buymeacoffee.com/tilschuenemann", target="_blank",className="text-xl font-bold text-center"),
                    className="grid bg-yellow-400 rounded-lg w-full h-12 items-center")
            
        ],className="grid content-end space-y-2")
    ],className="grid w-64 bg-neutral-800 p-4"),

    # Content
    html.Div([

        # Title
        html.P("Spotify Art + Code Generator",className="text-4xl font-semibold text-green-500 text-center"),
        html.Div([
            # Result
            html.Div([
            html.Img(src=placeholder,className="border-green-500 rounded-md h-96 drop-shadow-[0_20px_20px_rgba(34,197,94,0.33)]")

            ],id="result")

        ],className="flex grow col-span-4 grid place-content-center"),
        

    ],className="flex flex-col grow bg-neutral-900"),
    dcc.Store(id="search_uriresult")
],className="flex bg-neutral-900 w-screen h-screen")

@app.callback(
               Output("sidebar_metadata", "children"),
               Output("sidebar_uri", "children"),
               Output("sidebar_url", "children"),
    #Output("sidebar_menu","children"),
    Input("search_by", "value"))
def load_sidebar(search_by):

    url_visibility = {'display': 'none'}
    uri_visbility = {'display': 'none'}
    metadata_visbility = {'display': 'none'}

    if search_by == "Metadata":
        metadata_visbility = {'display': 'block'}
    elif search_by == "URI":
        uri_visbility = {'display': 'block'}
    elif search_by == "URL":
        url_visibility = {'display': 'block'}

    metadata = html.Div([
        dcc.Dropdown(id="search_type",
                    options=["album", "artist", "track"],
                    value="track",
                    clearable=False),
        dcc.Input(id="search_general",
                type="text",
                debounce=True,
                placeholder="kate bush running up that hill",
                className="w-full h-10 rounded p-2")
        ], className="grid",style=metadata_visbility),

    uri = html.Div(
            [dcc.Input(id="search_uri",
                       type="text",
                       debounce=True,
                       placeholder="Spotify URI",
                       className="w-full h-10 rounded p-2")
             ],
            className="grid", style=uri_visbility)

    # url field
    url = html.Div(
            [dcc.Input(id="search_url",
                       type="text",
                       debounce=True,
                       placeholder="Spotify URL",
                       className="w-full h-10 rounded p-2")
             ], className="grid", style=url_visibility)

    return metadata,uri,url

@app.callback(Output("result", "children"),
              State("search_by", "value"),
              State("search_type", "value"),
              State("search_uri", "value"),
              State("search_general", "value"),
              State("search_url", "value"),
              Input('search-trigger', 'n_clicks'),
              prevent_initial_call=True,
              )
def search(search_by, search_type, search_uri, search_general, search_url, n_clicks,):

    EMPTY = html.Div()    

    if search_by == "URI":
            uri = search_uri
    elif search_by == "Metadata":
        uri = uri_from_query(search_general, search_type, sp)
    elif search_by == "URL":
        uri = uri_from_url(search_url)

    if uri is None:
        return EMPTY
        
    img = get_art_with_code(uri, sp)
    return html.Img(src=img, className="border-green-500 h-96 drop-shadow-[0_20px_20px_rgba(34,197,94,0.33)]")


if __name__ == "__main__":
    app.run_server(debug=True)

