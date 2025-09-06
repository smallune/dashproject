from dash import html, dcc, Input, Output, callback, register_page
import pandas as pd
import plotly.express as px
from pathlib import Path
from pytrends.request import TrendReq

register_page(__name__, path = '/page3', name = 'Demographics')

pytrends = TrendReq(hl='en-US', tz=360)
# Get US region mapping data
## Downloaded from https://gist.github.com/rogerallen/1583593
# need to modify
DataPath = Path(__file__).resolve().parent.parent / 'data' / 'us_region_mapping.csv'
df_us_region_mapping = pd.read_csv(DataPath)

layout = html.Div(
    style = {'backgroundColor': '#f9f9f9', 'padding': '10px'},
    children = [
    html.H1('How do people search for energy drink by State', style = {'color': '#CDD6D3', 'textAlighn': 'center'}),
    html.H2("Demographic Data", className = "centered-header"),
    dcc.Tabs(id="tab_product", value='Red Bull', children=[
        dcc.Tab(label = 'Red Bull', value = 'Red Bull'),
        dcc.Tab(label = 'Monster', value = 'Monster'),
        dcc.Tab(label = 'Rockstar', value = 'Rockstar'),
        dcc.Tab(label = '5-hour Energy', value = '5-hour Energy'),
        dcc.Tab(label = 'Bang', value = 'Bang'),
        dcc.Tab(label = 'Celsius', value = 'Celsius')
    ]),
    dcc.Slider(
        id = 'year-slider',
        min = 2015,
        max = 2025,
        value = 2025,
        marks = {
            str(y): str(y) for y in range(2015, 2026)
        },
        step = None,
        tooltip = {'placement': 'bottom', 'always_visible': True}
    ),
    html.Br(),
    html.Div(id='choropleth-map') 
])

@callback (
    Output('choropleth-map', 'children'),
    Input('tab_product','value'),
    Input('year-slider', 'value'),
)

def update_map_trends(kw_list, selected_year):
    # get data from Google Trends
    # Specify the timeframe from the selected year with slider
    time_range = f'{selected_year}-01-01 {selected_year}-12-31'
    try:
        pytrends.build_payload([kw_list], cat=0, timeframe= time_range, geo='US', gprop='')
        df = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True, inc_geo_code=False)
    
        # Clean dataframe
        df = df.reset_index()
        df['year'] = selected_year
        df.columns = ['region', 'Interest over time', 'year']
        df = pd.merge(df, df_us_region_mapping, left_on='region', right_on = 'region_name', how='left')
        df = df[['region_code', 'Interest over time', 'year']]
        
        fig = px.choropleth(
            df,
            locations = 'region_code',
            locationmode = 'USA-states',
            color = 'Interest over time',
            scope = 'usa',
            color_continuous_scale = 'Reds',
            labels = {'price': 'Price (cents/kWh)'},
            title = f'Interest in {kw_list} over {selected_year} - from Google Trends'
        )
        fig.update_layout(
            geo = dict(bgcolor = '#336b64'), ## background color around map
            paper_bgcolor = '#113631',
            font_color = '#ffffff',
            margin = dict(l = 10, r = 10, t = 50, b = 20)   
        )
        return dcc.Graph(figure=fig)
    except Exception as e:
        # Catch any other unexpected errors
        error_message = f"An unexpected error occurred: {e}"
        return html.P(error_message, style={'color': 'red'})
    
