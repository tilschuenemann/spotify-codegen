from urllib.request import urlopen
from PIL import Image
import base64
from dash import Dash, dcc, html, Input, Output
import requests
import plotly.express as px


from io import BytesIO
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Picture Test"),
    dcc.Input(id="uri", type="text",
              placeholder="https://imgs.xkcd.com/comics/the_universe_by_scientific_field.png"),
    html.Div(id="picture")])


@app.callback(Output("picture", "children"), Input("uri", "value"))
def load_image(uri):

    if uri is None:
        return html.Div()

    b64_picture = base64.b64encode(requests.get(uri).content).decode("UTF-8")
    mime = 'data:image/png;base64,' + b64_picture
    return html.Img(src=mime)

    # response = requests.get(uri)
    # img = Image.open(BytesIO(response.content))
    # return html.Img(src=img)


if __name__ == "__main__":
    app.run_server(debug=True)
