import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


app = Dash(__name__, suppress_callback_exceptions = True)

#--------------------------------------------------------------------------------------------------
# Import and clean data (import csv into pandas)

df = pd.read_csv("us_births_2016_2021.csv")
ed_level_list = df['Education Level of Mother'].unique().tolist()
state_list = df['State'].unique().tolist()
#--------------------------------------------------------------------------------------------------

app.layout = html.Div(
    style = {'background-color': 'lightblue'},
    children = [

        html.H1("US Births From 2016 - 2021", style = {'text-align': 'center'}),

        html.Div(
            style = {'display': 'flex', 'flex-direction': 'row', 'background-color': 'blue', 'height': '900px'},
            children = [

                html.Div(
                    style = {'padding': 10, 'flex': '20%', 'background-color': 'red', 'height': '500px'},
                    children = [

                        html.Label("Select Year Range"),
                        dcc.RangeSlider(
                            id = 'year-selected',
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
                            value = [2016, 2021],
                            tooltip = {'placement': 'bottom', 'always_visible': True}),

                        html.Br(),
                        html.Label("Select Education Level"),
                        dcc.Dropdown(options = ed_level_list, id = 'ed-level-selected', value = ed_level_list[0], searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'}),

                        html.Br(),
                        html.Label("Select State"),
                        dcc.Dropdown(options = state_list, id = 'state-selected', value = state_list[0], searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'})

                ]), # html.Div ---- Sliders/DropsBoxes/Headings

                html.Div(

                    style = {'padding': 10, 'flex': '80%', 'background-color': 'green', 'height': '700px'},
                    children = [

                        dcc.Graph(id = 'bar-graph')
                        

                ]) # html.Div ---- Sliders/DropsBoxes/Headings


        ])

        


    

]) # app.layout = html.Div([


    



@app.callback(
    Output('bar-graph', 'figure'),
    [Input('ed-level-selected', 'value'),
     Input('state-selected', 'value'),
     Input('year-selected', 'value')]
)

def render_bar_graph(ed_level_selected, state_selected, year_selected):

    start_range = year_selected[0]
    end_range = year_selected[1]
    year_condition = df['Year'].between(start_range, end_range)
    state_condition = df['State'] == state_selected
    ed_condition = df['Education Level of Mother'] == ed_level_selected

    filtered_df = df[state_condition & year_condition & ed_condition].groupby('Year')['Number of Births'].sum().reset_index()

    fig = px.bar(filtered_df, x = 'Year', y = 'Number of Births')


    return fig
    

        









if __name__ == '__main__':
    app.run_server(debug = True)

