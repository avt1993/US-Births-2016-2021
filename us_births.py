import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__, suppress_callback_exceptions = True)
server = app.server

#--------------------------------------------------------------------------------------------------
# Import and clean data (import csv into pandas)

df = pd.read_csv("us_births_2016_2021_updated.csv")
#map_df = pd.read_csv("us_births_2016_2021_updated.csv")

ed_level_list = df['Education Level of Mother'].unique().tolist()
state_list = df['State'].unique().tolist()

#--------------------------------------------------------------------------------------------------
##003f5c
app.layout = html.Div(
    className = 'Main Container',
    style = {'background-color': 'grey', 'padding': '10px'},
    children = [

        #html.Br(),
        html.H1("US Births Data From 2016 - 2021", style = {'text-align': 'center', 'color': 'white', 'fontSize': '45px'}),

        html.Div(
            className = 'Dropdowns and Map Container',
            style = {'display': 'flex', 'height': '635px'},

            children = [
                html.Div(
                    id = 'drop-down-container',
                    className = 'Dropdowns Container',
                    style = {'flex': '15%', 'padding': '15px', 'text-align': 'center', 'background-color': 'lightcoral', 'border-width': '7px', 'border-style': 'solid', 'border-color': '#333333', 'box-shadow': '4px 4px 6px rgba(0, 0, 0, 0.5)'},

                    children = [
                        html.H3("Map Data Display Options", style = {'color': 'white'}),
                        dcc.Dropdown(options = ['Percentage of Education Level', 'Avg. Age of Mother by Ed Level'], id = 'map-mode', value = 'Percentage of Education Level', searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'}),
                        html.Br(),
                        html.H3("Mother's Education Level", style = {'color': 'white'}),
                        dcc.Dropdown(options = ed_level_list, id = 'ed-level-selected', value = ed_level_list[0], searchable = False, style = {'whiteSpace': 'normal', 'wordWrap': 'break-word'}),
                        html.Br(),
                        html.H3("Year", style = {'color': 'white'}), 
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
                            tooltip = {'placement': 'bottom', 'always_visible': True},
                        )
                ]),

                html.Div(
                    style = {'flex': '0.5%'}
                ),


                html.Div(
                    className = 'Map Container',
                    style = {'flex': '85%', 'box-shadow': '4px 4px 6px rgba(0, 0, 0, 0.5)', 'border-width': '7px', 'border-style': 'solid', 'border-color': '#333333'},

                    children = [
                        dcc.Graph(id = 'map', style = {'width': '100%', 'height': '100%'})
                ]),
        ]),

        html.Br(),

        html.Div(
            className = 'Bar Charts Container',
            style = {'box-shadow': '4px 4px 6px rgba(0, 0, 0, 0.5)', 'border-width': '7px', 'border-style': 'solid', 'border-color': '#333333', 'height': '350px'},  

            children = [
                dcc.Graph(id = 'bar-graph', style = {'width': '100%', 'height': '100%'}),
        ])                       

]) # app.layout = html.Div([

         


@app.callback(
    [Output('bar-graph', 'figure'),
    Output('drop-down-container', 'style')],
    [Input('map', 'clickData'),
     Input('year-selected', 'value'),
     Input('map-mode', 'value'),
     Input('ed-level-selected', 'value')]
)

def render_bar_graph(state_clicked, year_selected, map_mode, ed_level_sel):

    if state_clicked is not None:
        state_selected = state_clicked['points'][0]['location']
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
    
    filtered_df_for_fig = filtered_df_for_fig.sort_values('Percentage of Births by Ed Level', ascending = False).reset_index()
    filtered_df_for_fig2 = filtered_df_for_fig2.sort_values('Average Age of Mother (years)', ascending = False).reset_index()

    if (map_mode == 'Percentage of Education Level'):

        position = filtered_df_for_fig[filtered_df_for_fig['Education Level of Mother'] == ed_level_sel].index[0]
        colors = ['lightgrey',] * 9
        colors[position] = 'firebrick'

        fig = go.Figure(data = [
                    go.Bar(
                    x = filtered_df_for_fig['Education Level of Mother'],
                    y = filtered_df_for_fig['Percentage of Births by Ed Level'],
                    text = filtered_df_for_fig['Percentage of Births by Ed Level'],
                    marker_color = colors # marker color can be a single color value or an iterable
                    )
        ])
        fig.update_layout(
            title = ('Births by Education Level of Mother<br>' + 'State: ' + state_selected + '  /  ' + 'Year: ' + year_title),
            xaxis_title = "",
            yaxis_title = False,
            yaxis_visible = False,
            xaxis_visible = True,
            plot_bgcolor = 'rgba(0,0,0,0)'  # Set the plot background color to transparent
        )
        fig.update_traces(textposition = "outside", cliponaxis = False, texttemplate = '%{text}%')

        return fig, {'flex': '15%', 'padding': '15px', 'text-align': 'center', 'background-color': 'lightcoral', 'border-width': '7px', 'border-style': 'solid', 'border-color': '#333333', 'box-shadow': '4px 4px 6px rgba(0, 0, 0, 0.5)'}

    else:

        position = filtered_df_for_fig2[filtered_df_for_fig2['Education Level of Mother'] == ed_level_sel].index[0]
        colors = ['lightgrey',] * 9
        colors[position] = 'steelblue'

        fig2 = go.Figure(data = [
                    go.Bar(
                    x = filtered_df_for_fig2['Education Level of Mother'],
                    y = filtered_df_for_fig2['Average Age of Mother (years)'],
                    text = filtered_df_for_fig2['Average Age of Mother (years)'],
                    marker_color = colors # marker color can be a single color value or an iterable
                    )
        ])
        fig2.update_layout(
            title = ('Average Age of Mother by Education Level<br>' + 'State: ' + state_selected + '  /  ' + 'Year: ' + year_title),
            xaxis_title = "",
            yaxis_title = False,
            yaxis_visible = False,
            xaxis_visible = True,
            plot_bgcolor = 'rgba(0,0,0,0)'  # Set the plot background color to transparent
        )
        fig2.update_traces(textposition = "outside", cliponaxis = False)

        return fig2, {'flex': '15%', 'padding': '15px', 'text-align': 'center', 'background-color': 'steelblue', 'border-width': '7px', 'border-style': 'solid', 'border-color': '#333333', 'box-shadow': '4px 4px 6px rgba(0, 0, 0, 0.5)'}
    

    
@app.callback(
    Output('map', 'figure'),
    [Input('year-selected', 'value'),
    Input('ed-level-selected', 'value'),
    Input('map-mode', 'value')]
)

def update_map(year_selected, ed_level_selected, map_mode):

    if year_selected[0] == year_selected[1]:

        year_title = str(year_selected[0])
        year_chosen = year_selected[0]

        total_births_by_state_and_year = df[(df['Year'] == year_chosen)].groupby(['State', 'State Abbreviation', 'Year'])['Number of Births'].sum().reset_index(name = 'Total Births in State')
        df_by_ed_level_usa = df[(df['Year'] == year_chosen) & (df['Education Level of Mother'] == ed_level_selected)].groupby(['State', 'State Abbreviation', 'Year', 'Education Level of Mother'])['Number of Births'].sum().reset_index()
        merged_df = df_by_ed_level_usa.merge(total_births_by_state_and_year, on = ['State', 'State Abbreviation', 'Year'], suffixes = ('_by ed level', '_by state'))
        merged_df['Percentage of Births by State'] = ((merged_df['Number of Births'] / merged_df['Total Births in State'])* 100).round(2)

    else:
        year_title = (str(year_selected[0]) + ' - ' + str(year_selected[1]))


    if (map_mode == 'Percentage of Education Level'):

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
            layout = go.Layout(
                        margin = dict(l=0, r=0, t=0, b=0),
                        autosize = True
            )
        )   

        map_fig.update_layout(
            title = dict(
                    text = 'Percentage of Births by State<br>' + 'Education Level of Mother: ' + ed_level_selected + '<br>' + 'Year: ' + year_title,
                    x = 0.92,  # Set the horizontal position of the title to the center (0.0 - left, 0.5 - center, 1.0 - right)
                    y = 0.25  # Set the vertical position of the title (0.0 - bottom, 0.5 - middle, 1.0 - top)
            ),
            geo = dict(
                bgcolor = 'rgba(0, 0, 0, 0)',
                scope = 'usa',
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
                projection_scale = 1,  # Adjust the scale to fit the map on the screen
            ),  
        ) 
        

    else:
        merged_df = df[df['Year'].between(year_selected[0],year_selected[1]) & (df['Education Level of Mother'] == ed_level_selected)].groupby(['State', 'State Abbreviation'])['Average Age of Mother (years)'].mean().reset_index()

        map_fig = go.Figure(
            data = go.Choropleth(
                        locations = merged_df['State Abbreviation'], # Spatial coordinates
                        z = merged_df['Average Age of Mother (years)'].astype(float), # Data to be color-coded
                        locationmode = 'USA-states', # set of locations match entries in `locations`
                        colorscale = 'Blues',
                        colorbar_title = "Avgerage Age",
                        marker_line_width = 2,
                        text = merged_df['Average Age of Mother (years)'],
                        hovertemplate = 'State: %{location}<br>Average Age: %{text:.1f}<extra></extra>'
            ),
            layout = go.Layout(
                        margin = dict(l=0, r=0, t=0, b=0),
                        autosize = True
            )
      
        )   

        map_fig.update_layout(
            title = dict(
                    text = 'Average Age of Mother by State<br>' + 'Education Level of Mother: ' + ed_level_selected + '<br>' + 'Year: ' + year_title,
                    x = 0.92,  # Set the horizontal position of the title to the center (0.0 - left, 0.5 - center, 1.0 - right)
                    y = 0.25  # Set the vertical position of the title (0.0 - bottom, 0.5 - middle, 1.0 - top)
            ),
            geo = dict(
                bgcolor = 'rgba(0, 0, 0, 0)',
                scope = 'usa',
                showlakes = True,
                lakecolor = 'rgb(255, 255, 255)',
                projection_scale = 1,  # Adjust the scale to fit the map on the screen

            ),  
        )

    return map_fig





if __name__ == '__main__':
    app.run_server(debug = True)

