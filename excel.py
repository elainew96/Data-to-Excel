import dash
import dash_html_components as html
import dash_core_components as dcc
import time
from dash.dependencies import Input, Output, Event, State

import xlsxwriter
from xlrd import open_workbook
from xlutils.copy import copy

app = dash.Dash()

global clicks
clicks = 0

def create_new(name,data):
    workbook = xlsxwriter.Workbook(name+'.xlsx')
    worksheet = workbook.add_worksheet('Spending')
    #initialize new headers
    row = 0
    worksheet.write(row,0,'date:')
    worksheet.write(row,1,'purchase item:')
    worksheet.write(row,2,'price:')
    worksheet.write(row,3,'timestamp:')
    workbook.close()
    return update_sheet(name,data)

def update_sheet(name,data):
    #opens existing sheet and makes a copy to edit
    rb = open_workbook(name+'.xlsx')
    wb = copy(rb)
    sheet = wb.get_sheet('Spending')
    #trial
    return name
    #find the next empty line
    #try something, if fails then put in data


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
              [Input('create-new','n_clicks'),
               Input('update-existing','n_clicks')],
              [State('sheet','value'),
               State('name','value'),
               State('purchase','value'),
               State('date','value'),
               State('price','value')])
def display_choice(new_clicks,update_clicks,sheet_value,name,purchase,date,price):
    #use global variable to find out which click it was
    global clicks
    timestamp = time.time
    info = [date,purchase,price,timestamp]
    if (((sheet_value == 'update') | (sheet_value == 'edit')) & (new_clicks>clicks)):
        clicks = new_clicks #update clicks
        return html.Div('Are you sure you didn\'t mean to update or edit an existing sheet?')
    elif ((sheet_value == 'new') & (update_clicks>1)):
        return html.Div('Are you sure you didn\'t want to create a new sheet?')
    elif ((sheet_value == 'new') & (new_clicks>clicks)):
        #data is a pandas dataframe, and create new makes the excel and converts it into pandas
        data = create_new(name,info)
        return html.Div(name)

if __name__ == '__main__':
    app.run_server(debug=True)
