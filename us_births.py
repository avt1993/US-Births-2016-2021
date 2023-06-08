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

app.layout = html.Div([

    html.H1("US Births From 2016 - 2021", style = {'text-align': 'center'}),

    html.Div(

        style = {'width': '30%'},
        children = [

            html.H2("Select Year Option", style = {'text-align': 'center'}),

            dcc.Dropdown(options = ['Single Year', 'Year Range'], id = 'year-option', searchable = False, style = {'text-align': 'center', 'fontSize': '20px',
                                                                                                                    'padding': '20px'}),                                                                                                       
            html.H2(id = 'year-option-selected', style = {'text-align': 'center'}),

            html.Div(id = 'slider-or-dropdown'),

            html.H2("Select Education Level", style = {'text-align': 'center'}),

            dcc.Dropdown(options = ed_level_list, id = 'ed-level-selected', searchable = False, style = {'text-align': 'center', 'fontSize': '20px',
                                                                              'padding': '20px', 'whiteSpace': 'normal', 'wordWrap': 'break-word'}),

            html.H2("Select State", style = {'text-align': 'center'}),

            dcc.Dropdown(options = state_list, id = 'state-selected', searchable = False, style = {'text-align': 'center', 'fontSize': '20px',
                                                                              'padding': '20px', 'whiteSpace': 'normal', 'wordWrap': 'break-word'})






    ]) # html.Div(

    

]) # app.layout = html.Div([


@app.callback(
    Output('year-option-selected', 'children'),
    [Input('year-option', 'value')] 
)

def year_selected_heading(year_option):
    if year_option == 'Single Year':
        title = 'Select Single year'
        return title
    
    elif year_option == 'Year Range':
        title = 'Select Year Range'
        return title








@app.callback(
    Output('slider-or-dropdown', 'children'),
    [Input('year-option', 'value')]
)

def render_slider(year_option):

    if year_option == 'Single Year':

        return dcc.Dropdown(['2016', '2017', '2018', '2019', '2020', '2021'], '2016', id = 'year_selected', searchable = False, 
                            style = {'text-align': 'center',
                                    'fontSize': '20px',
                                    'padding': '20px'})
    
    
    elif year_option == 'Year Range':
        return dcc.RangeSlider(
            id = 'year_selected',
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
    





if __name__ == '__main__':
    app.run_server(debug = True)

