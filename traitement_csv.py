# version static a ameliorer

import csv



#vj1 = "C:/Program Files/PostgreSQL/9.5/CSV/vj1.csv"
#cr = csv.reader(open(vj1,"rb"))
#for row in cr:
   # print row
fname = "C:/Program Files/PostgreSQL/9.5/CSV/sdc_2_16_bis.csv"
fname1 = "C:/Program Files/PostgreSQL/9.5/CSV/sdc_2_16.csv"
file1 = open(fname1, "wb")
file = open(fname, "rb")

try:
    reader = csv.reader(file)
    writer = csv.writer(file1)

    i = 0
    for row in reader:
        if i == 0:
            print "Suppression de la premiere ligne :"
            print row
        else :
            #row = row.insert(0, str(i))
            writer.writerow(row)
        i = i + 1

finally:
    file.close()


