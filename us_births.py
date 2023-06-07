import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__)

#--------------------------------------------------------------------------------------------------
# Import and clean data (import csv into pandas)

df = pd.read_csv("us_births_2016_2021.csv")
#--------------------------------------------------------------------------------------------------

app.layout = html.Div([

    html.H1("US Births From 2016 - 2021", style = {'text-align': 'center'}),

    html.Div(
        style = {'width': '25%'},
        children = [dcc.RangeSlider(
                    min = 2016, 
                    max = 2021, 
                    step = 1, 
                    marks = {
                        2016: '2016',
                        2017: '2017',
                        2018: '2018',
                        2019: '2019',
                        2020: '2020',
                        2021: '2021'
                    },
                    value = [2018, 2020],
                    tooltip = {'placement': 'bottom', 'always_visible': True})

    ])
    

]) # app.layout = html.Div([


if __name__ == '__main__':
    app.run_server(debug = True)

