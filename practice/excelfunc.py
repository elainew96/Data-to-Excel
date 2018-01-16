import xlsxwriter
import xlrd
from xlrd import open_workbook
from xlutils.copy import copy

import time

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
    print 'done'
    return update_sheet(name,data)

def update_sheet(name,data):
    #opens existing sheet and makes a copy to edit
    rb = open_workbook(name+'.xlsx')
    s = rb.sheet_by_name('Spending')
    wb = copy(rb)
    sheet = wb.get_sheet('Spending')
    row = 0
    found = 0
    while (found == 0):
        print 'trying to find'
        #sees if the row has an entry, if it fails then exit the loop and we know which row is empty
        try:
            print 'hellooooo'
            exists = s.cell_value(row,0)
            row = row + 1
            print 'prev: ' + exists
        except:
            print 'not found'
            found = 1
    # puts the data into the excel sheet
    for i in range(len(data)):
        print data[i]
    for i in range(len(data)):
        sheet.write(row,i,data[i])
    # saves the new sheet
    wb.save(name+'.xlsx')
    return name

print 'hello'
name = 'stuff'
data = []
data.append('1/13/18')
data.append('blankets')
data.append('$4.20')
data.append(time.ctime())

create_new(name,data)
