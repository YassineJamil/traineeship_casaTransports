import xlrd
import csv


def csv_from_excel():
    wb = xlrd.open_workbook('SDD010616.xls')
    sh = wb.sheet_by_index()
    your_csv_file = open('SDD010616.csv', 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
    print 'ok'
    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))
        print 'lol'
    print 'finish'

    your_csv_file.close()

csv_from_excel()