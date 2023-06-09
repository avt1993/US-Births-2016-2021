import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_leaflet as dl
import json
from dash_extensions.javascript import arrow_function

app = Dash(__name__, suppress_callback_exceptions = True)

#--------------------------------------------------------------------------------------------------
# Import and clean data (import csv into pandas)

df = pd.read_csv("us_births_2016_2021.csv")
#us_states_data = pd.read_json('us-states.json')
with open('us-states.json') as f:
    us_states_data = json.load(f)

ed_level_list = df['Education Level of Mother'].unique().tolist()
state_list = df['State'].unique().tolist()
#--------------------------------------------------------------------------------------------------

app.layout = html.Div(
    style = {'background-color': 'lightblue'},
    children = [

        html.H1("US Births From 2016 - 2021", style = {'text-align': 'center'}),

        html.Div(
            style = {'display': 'flex', 'flex-direction': 'row', 'background-color': 'blue', 'height': '1200px'},
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

                    style = {'padding': 10, 'flex': '80%', 'background-color': 'green', 'height': '860px'},
                    children = [

                        dcc.Graph(id = 'bar-graph'),
                        dcc.Graph(id = 'bar-graph2'),

                        html.Br(),
                        dl.Map(
                            style = {'width': '100%', 'height': '600px'},
                            children = [
                                dl.TileLayer(),
                                dl.GeoJSON(data = us_states_data, 
                                           id = 'state-layer', 
                                           options = {'style': {'color': 'blue'}},
                                           hoverStyle = arrow_function(dict(weight = 10, color = '#666', dashArray = '')))
                                           
                            ], center = [37.0902, -95.7129], zoom = 4),

                            html.Div(id = 'state_name')


                        





                        

                ]) # html.Div ---- Sliders/DropsBoxes/Headings


        ])

        


    

]) # app.layout = html.Div([




@app.callback(
        Output("state_name", "children"), 
        [Input("state-layer", "hover_feature")]
)

def state_hover(feature):
    if feature is not None:
        return f"{feature['properties']['name']}"
    



@app.callback(
    [Output('bar-graph', 'figure'),
    Output('bar-graph2', 'figure')],
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

    df_by_ed_level = df[state_condition & year_condition].groupby('Education Level of Mother')['Number of Births'].sum().reset_index()
    df_by_ed_level['Formatted Number of Births Value'] = [f'{val:,}' for val in df_by_ed_level['Number of Births']]
    df_by_ed_level = df_by_ed_level.sort_values(by = 'Number of Births', ascending = False)



    fig2 = px.bar(df_by_ed_level, x = 'Education Level of Mother', y = 'Number of Births', text = 'Formatted Number of Births Value')

    fig2.update_layout(
        title = ('Total Births by Education Level of Mother in ' + state_selected),
        xaxis_title = "",
        yaxis_title = False,
        yaxis_visible = False,
        xaxis_visible = True,
        plot_bgcolor = 'rgba(0,0,0,0)',  # Set the plot background color to transparent
        #paper_bgcolor = 'rgba(0,0,0,0)',  # Set the paper background color to transparent
    )
    fig2.update_traces(textposition = "outside", cliponaxis = False)



    return fig, fig2
    

        









if __name__ == '__main__':
    app.run_server(debug = True)

