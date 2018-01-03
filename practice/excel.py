import dash
import dash_html_components as html
import dash_core_components as dcc
import time

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1('Creating a Spending Excel Sheet'),
    html.Br(),
    html.P('Create new sheet or update existing sheet?'),
    dcc.RadioItems(
        id = 'sheet',
        options=[
            {'label': 'New', 'value': 'new'},
            {'label': 'Update', 'value': 'update'}
        ]
    ),
    html.Br(),
    html.P('Purchase Item:'),
    dcc.Input(type='text')
])

if __name__ == '__main__':
    app.run_server(debug=True)
