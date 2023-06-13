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

df = pd.read_csv("us_births_2016_2021_updated.csv")
#map_df = pd.read_csv("us_births_2016_2021_updated.csv")

with open('us-states.json') as f:
    us_states_GEOJSON = json.load(f)

ed_level_list = df['Education Level of Mother'].unique().tolist()
state_list = df['State'].unique().tolist()

#--------------------------------------------------------------------------------------------------

app.layout = html.Div(
    style = {'background-color': 'lightblue'},
    children = [

        html.H1("US Births From 2016 - 2021", style = {'text-align': 'center'}),

        html.Div(
            style = {'display': 'flex', 'flex-direction': 'row', 'background-color': 'darkblue', 'height': '1200px'},
            children = [

                html.Div(
                    style = {'padding': 10, 'flex': '20%', 'background-color': 'red', 'height': '1000px'},
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
                            value = [2016, 2016],
                            tooltip = {'placement': 'bottom', 'always_visible': True}),

                        html.Br(),
                        html.Br(),
                        html.Label("Select Education Level"),
                        dcc.Dropdown(options = ed_level_list, id = 'ed-level-selected', value = ed_level_list[0], searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'}),

                        html.Br(),
                        html.Br(),
                        #html.Label("Select State"),
                        #dcc.Dropdown(options = state_list, id = 'state-selected', value = state_list[0], searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'})

                ]), # html.Div ---- Sliders/DropsBoxes/Headings

                html.Div(

                    style = {'padding': 10, 'flex': '80%', 'background-color': 'green', 'height': '860px'},
                    children = [

                        dcc.Graph(id = 'map'),
                        dcc.Graph(id = 'bar-graph1'),
                        dcc.Graph(id = 'bar-graph2'),
                        html.Div(id = 'state'),




                        html.Br(),


                            

                    

                        

                ]) # html.Div ---- Sliders/DropsBoxes/Headings


        ])

        


    

]) # app.layout = html.Div([




# Define the callback to capture click events
#@app.callback(
    #Output('state', 'children'),
    ###Input('map', 'clickData')
#)
#def select_state_on_click(click_data):
    #if click_data is not None:
        #state_name = click_data['points'][0]['location']
        #return f"You clicked on state: {state_name}"
    #else:
        #return ""
    



@app.callback(
    [Output('bar-graph1', 'figure'),
     Output('bar-graph2', 'figure')],
    [Input('map', 'clickData'),
     Input('year-selected', 'value')]
)

def render_bar_graph(state_clicked, year_selected):

    if state_clicked is not None:
        state_selected = state_clicked['points'][0]['location']
        #return f"You clicked on state: {state_name}"
    else:
        state_selected = 'CA'

    if year_selected[0] == year_selected[1]:
    
        filtered_df_for_fig = df[(df['Year'] == year_selected[0]) & (df['State Abbreviation'] == state_selected)] 
        
        filtered_df_for_fig2 = df[(df['Year'] == year_selected[0]) & (df['State Abbreviation'] == state_selected)].groupby('Education Level of Mother')['Number of Births', 'Average Age of Mother (years)'].sum().reset_index()

        year_title = str(year_selected[0])
    else:
        filtered_df_for_fig = df[(df['Year'].between(year_selected[0], year_selected[1])) & (df['State Abbreviation'] == state_selected)].groupby('Education Level of Mother')['Number of Births', 'Total Births in State'].sum().reset_index()
        
        filtered_df_for_fig2 = df[(df['Year'].between(year_selected[0], year_selected[1])) & (df['State Abbreviation'] == state_selected)].groupby('Education Level of Mother')['Number of Births', 'Average Age of Mother (years)'].sum().reset_index()
        filtered_df_for_fig2['Average Age of Mother (years)'] = (filtered_df_for_fig2['Average Age of Mother (years)'] / ((year_selected[1] - year_selected[0]) + 1)).round(1)

        year_title = (str(year_selected[0]) + ' - ' + str(year_selected[1]))

    filtered_df_for_fig['Percentage of Births by Ed Level'] = ((filtered_df_for_fig['Number of Births'] / filtered_df_for_fig['Total Births in State'])*100).round(1)
    
    filtered_df_for_fig = filtered_df_for_fig.sort_values('Percentage of Births by Ed Level', ascending = False)

    filtered_df_for_fig2 = filtered_df_for_fig2.sort_values('Average Age of Mother (years)', ascending = False)



    


    fig = px.bar(filtered_df_for_fig, x = 'Education Level of Mother', y = 'Percentage of Births by Ed Level', text = 'Percentage of Births by Ed Level')
    fig.update_layout(
        title = ('Births by Education Level of Mother<br>' + 'State: ' + state_selected + '  /  ' + 'Year: ' + year_title),
        xaxis_title = "",
        yaxis_title = False,
        yaxis_visible = False,
        xaxis_visible = True,
        plot_bgcolor = 'rgba(0,0,0,0)'  # Set the plot background color to transparent
    )
    fig.update_traces(textposition = "outside", cliponaxis = False, texttemplate = '%{text}%')

    fig2 = px.bar(filtered_df_for_fig2, x = 'Education Level of Mother', y = 'Average Age of Mother (years)', text = 'Average Age of Mother (years)')
    fig2.update_layout(
        title = ('Average Age of Mother by Education Level<br>' + 'State: ' + state_selected + '  /  ' + 'Year: ' + year_title),
        xaxis_title = "",
        yaxis_title = False,
        yaxis_visible = False,
        xaxis_visible = True,
        plot_bgcolor = 'rgba(0,0,0,0)'  # Set the plot background color to transparent
    )
    fig2.update_traces(textposition = "outside", cliponaxis = False)

    return fig, fig2
    

    
@app.callback(
    Output('map', 'figure'),
    [Input('year-selected', 'value'),
     Input('ed-level-selected', 'value')]
)

def update_map(year_selected, ed_level_selected):

    if year_selected[0] == year_selected[1]:

        year_title = str(year_selected[0])
        year_chosen = year_selected[0]

        total_births_by_state_and_year = df[(df['Year'] == year_chosen)].groupby(['State', 'State Abbreviation', 'Year'])['Number of Births'].sum().reset_index(name = 'Total Births in State')
        df_by_ed_level_usa = df[(df['Year'] == year_chosen) & (df['Education Level of Mother'] == ed_level_selected)].groupby(['State', 'State Abbreviation', 'Year', 'Education Level of Mother'])['Number of Births'].sum().reset_index()
        merged_df = df_by_ed_level_usa.merge(total_births_by_state_and_year, on = ['State', 'State Abbreviation', 'Year'], suffixes = ('_by ed level', '_by state'))
        merged_df['Percentage of Births by State'] = ((merged_df['Number of Births'] / merged_df['Total Births in State'])* 100).round(2)

    else:
        year_title = (str(year_selected[0]) + ' - ' + str(year_selected[1]))

        total_births_by_state_and_year = df[(df['Year'].between(year_selected[0],year_selected[1]))].groupby(['State', 'State Abbreviation', 'Year'])['Number of Births'].sum().reset_index(name = 'Total Births in State')
        df_by_ed_level_usa = df[(df['Year'].between(year_selected[0],year_selected[1])) & (df['Education Level of Mother'] == ed_level_selected)].groupby(['State', 'State Abbreviation', 'Year', 'Education Level of Mother'])['Number of Births'].sum().reset_index()
        merged_df = df_by_ed_level_usa.merge(total_births_by_state_and_year, on = ['State', 'State Abbreviation', 'Year'], suffixes = ('_by ed level', '_by state'))
        merged_df = merged_df.groupby(['State', 'State Abbreviation'])['Number of Births', 'Total Births in State'].sum().reset_index()
        merged_df['Percentage of Births by State'] = ((merged_df['Number of Births'] / merged_df['Total Births in State'])* 100).round(2)


    map_fig = go.Figure(
        data = go.Choropleth(
        locations = merged_df['State Abbreviation'], # Spatial coordinates
        z = merged_df['Percentage of Births by State'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Reds',
        colorbar_title = "Percentage",
        marker_line_width = 2,
        text = merged_df['Percentage of Births by State'],
        hovertemplate = 'State: %{location}<br>Percentage: %{text:.1f}%<extra></extra>'
        ),
        layout = dict(
                    width = 1320,     
                    height = 600
                )
    )   

    map_fig.update_layout(
        title_text = ('Percentage of Births by State<br>' + 'Education Level of Mother: ' + ed_level_selected + '<br>' + 'Year: ' + year_title),
        geo = dict(
            scope = 'usa',
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)',
        )
    )

    return map_fig





if __name__ == '__main__':
    app.run_server(debug = True)

