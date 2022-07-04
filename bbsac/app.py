from dash import Dash, dcc, html, Input, Output
from dash import Dash, dcc, html, Input, Output
from bbsac.bbsac import get_album_code
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

from urllib.request import urlopen
import base64
import re

app = Dash(__name__,external_stylesheets=["https://cdnjs.cloudflare.com/ajax/libs/tailwindcss/2.2.19/tailwind.min.css"])

server = app.server

app.layout = html.Div([
    html.H1("Bring Back Spotify Album Codes",className="text-4xl text-center"),
    dcc.Input(id="uri", type="text",debounce=True,
              placeholder="Enter Spotify Album URI here!"),
    html.Div(id="picture")],className="w-full h-screen bg-violet-800")


sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials())


@app.callback(Output("picture", "children"), Input("uri", "value"))
def load_image(uri):

    if uri is None:
        return html.Div()

    if re.match(r"^spotify:album:\d{20}$", uri): 
        img = get_album_code(uri, sp)
        return html.Img(src=img)
    else:
        return html.Span("Please supply a valid Spotify album URI!")

if __name__ == "__main__":
    app.run_server(debug=True)
