import csv

with open('contact012.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    names = []
    emails = []
    wishlist = []
    for row in readCSV:
        firstname = row[1]
        lastname = row[2]
        email = row[3]
        wishlist = row[5]

      

    print(firstname)
    print(lastname)
    print(email)
    print(wishlist)
    