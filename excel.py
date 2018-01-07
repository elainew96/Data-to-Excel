import dash
import dash_html_components as html
import dash_core_components as dcc
import time
from dash.dependencies import Input, Output, Event, State

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Spending Excel Sheet'),
    html.P('Create new sheet or update existing sheet?'),
    #choose new or update existing
    dcc.RadioItems(
        id = 'sheet',
        options=[
            {'label': 'New', 'value': 'new'},
            {'label': 'Update', 'value': 'update'},
            {'label': 'Edit', 'value': 'edit'}
        ]
    ),
    html.Br(),
    html.Div([
        html.P('Excel Sheet Name:'),
        dcc.Input(type='text',id='name'),
        html.P('Purchase Item:'),
        dcc.Input(type='text',id='purchase'),
        html.P('Date Purchased:'),
        dcc.Input(id='date'),
        html.P('Purchase Price:'),
        dcc.Input(id='price'),
    ], style={'columnCount':2}),
    html.Br(),
    html.Br(),
    html.Button('Create New Sheet',id='create-new'),
    html.Button('Update Existing Sheet',id='update-existing'),
    html.Br(),
    html.Br(),
    #output will be a pandas table with the information
    html.Div(id='output'),
    #graph displays spending habits
    html.Div(id='time-graph')
])

@app.callback(Output('output','children'),
              [Input('create-new','n_clicks')],
              [State('sheet','value')])
def create_new(n_clicks,sheet_value):
    if (sheet_value != 'new' & n_clicks<1):
        return html.Div('Are you sure you didnt mean to update or edit an existing sheet?')


if __name__ == '__main__':
    app.run_server(debug=True)
