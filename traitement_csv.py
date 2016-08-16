# version static a ameliorer

import csv

fname = "C:/Program Files/PostgreSQL/9.5/CSV/SDD/SDD_0716.csv"
fname1 = "C:/Program Files/PostgreSQL/9.5/CSV/SDD/SDD_0716_clean.csv"
file1 = open(fname1, "wb")
file = open(fname, "rb")

try:
    reader = csv.reader(file)
    writer = csv.writer(file1)

    i = 0
    for row in reader:
        if i == 0:
            print "Suppression de :"
            print row
        else :
            writer.writerow(row)
        i = i + 1

finally:
    file.close()


