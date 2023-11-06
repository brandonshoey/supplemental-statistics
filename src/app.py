from dash import Dash, dash_table, dcc, html, Input, Output, State
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import dash
import requests

markets = requests.get("https://us-central1-industrial-demand.cloudfunctions.net/initialize", {"name": "Markets"}).json()

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.H1(children="Supplemental Market Statistics"),

        dcc.Dropdown(id="my-dropdown", multi=False,
                     options = [{"label": x, "value": x} for x in markets],
                     value = "Kansas City - MO"),

        # dcc.Graph(id="bar-chart-output", figure={})
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)