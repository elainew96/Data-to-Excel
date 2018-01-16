import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, Event, State

import xlsxwriter
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy

import pandas as pd

import time

app = dash.Dash()

global clicks # for creating a new sheet button
global u_clicks #for update button
clicks = 0
u_clicks = 0

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
    # opens the sheet to read from
    s = rb.sheet_by_name('Spending')
    wb = copy(rb)
    sheet = wb.get_sheet('Spending')
    row = 0
    found = 0
    #trial
    while (found == 0):
        #sees if the row has an entry, if it fails then exit the loop and we know which row is empty
        try:
            exists = s.cell_value(row,0)
            row = row + 1
        except:
            found = 1
    # puts the data into the excel sheet
    for i in range(len(data)):
        sheet.write(row,i,data[i])
    # saves the new sheet
    wb.save(name+'.xlsx')
    return name
    '''
    #gets data from excel as pandas DataFrame
    dfs = pd.readexcel(name+'.xlsx',sheetname="Spending")
    return dfs

    '''

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
    #use global variables to find out which click it was
    global clicks
    global u_clicks
    timestamp = time.ctime()
    info = [date,purchase,price,timestamp]
    if (((sheet_value == 'update') | (sheet_value == 'edit')) & (new_clicks>clicks)):
        clicks = new_clicks #update clicks
        return html.Div('Are you sure you didn\'t mean to update or edit an existing sheet?')
    elif ((sheet_value == 'new') & (update_clicks>u_clicks)):
        u_clicks = update_clicks
        return html.Div('Are you sure you didn\'t want to create a new sheet?')
    elif ((sheet_value == 'new') & (new_clicks>clicks)):
        clicks = new_clicks
        #data is a pandas dataframe, and create new makes the excel and converts it into pandas
        data = create_new(name,info)
        data = pd.read_excel(name+'.xlsx',sheetname="Spending")
        # need to fix spacing/padding issues with table
        return html.Div([html.Table(
                    [html.Tr([html.Th(col) for col in data.columns])] +
                    [html.Tr([
                        html.Td(data.iloc[i][col]) for col in data.columns
                    ]) for i in range(len(data))]
                    ),
                ])
    elif ((sheet_value == 'update') & (update_clicks>u_clicks)):
        u_clicks = update_clicks
        data = update_sheet(name,info)
        return html.Div(data)

if __name__ == '__main__':
    app.run_server(debug=True)
