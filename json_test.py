import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_leaflet as dl
import json


# Load the US states data from the JSON file
with open('us-states.json') as f:
    us_states_data = json.load(f)

# Define the layout of your Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("US States Map"),
    dl.Map([
        dl.TileLayer(),
        dl.GeoJSON(data=us_states_data, options={'style': {'color': 'blue'}})
    ], style={'width': '100%', 'height': '600px'}, center=[37.0902, -95.7129], zoom=4),
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)