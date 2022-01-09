import pandas as pd  # (version 1.0.0)
import plotly  # (version 4.5.0)
import plotly.express as px

import dash  # (version 1.8.0)
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


file_name = 'data/DOHMH_New_York_City_Restaurant_Inspection_Results_sub.csv'
df = pd.read_csv(file_name)
df['INSPECTION DATE'] = pd.to_datetime(df['INSPECTION DATE'])
cusine_types = list(df['CUISINE DESCRIPTION'].unique())
newdf = df.groupby(['CAMIS', 'INSPECTION DATE',
                   'CUISINE DESCRIPTION'], as_index=False)['SCORE'].sum()
newdf = newdf.groupby(
    ['CUISINE DESCRIPTION', 'INSPECTION DATE'], as_index=False)['SCORE'].mean()
# newdf['INSPECTION DATE'] = newdf['INSPECTION DATE'].dt.to_period('M')
newdf = newdf.sort_values('INSPECTION DATE')

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Restaurant Inspection in NYC'),

    html.Div(children='''
        choose cuisine type to compare
    '''),
    dcc.Dropdown(
        id='dropdown1',
        options=[{'label': x, 'value': str(x)} for x in cusine_types],
    ),
    dcc.Dropdown(
        id='dropdown2',
        options=[{'label': x, 'value': x} for x in cusine_types],
    ),
    dcc.Dropdown(
        id='dropdown3',
        options=[{'label': x, 'value': x} for x in cusine_types],
    ),

    dcc.Graph(
        id='example-graph',
    )
])


@app.callback(Output('example-graph', 'figure'),
              Input('dropdown1', 'value'),
              Input('dropdown2', 'value'),
              Input('dropdown3', 'value'),)
def update_fig(val1, val2, val3):
    plot_df = newdf[newdf['CUISINE DESCRIPTION']==val1]
    fig0 = px.line(plot_df, x='INSPECTION DATE', y = 'SCORE', color='CUISINE DESCRIPTION', title=f'Score for {val1} cusine')
    print(plot_df.head())
    return fig0


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
