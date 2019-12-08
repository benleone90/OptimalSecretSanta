import psycopg2

try:
    conn = psycopg2.connect("dbname='template1' user='dbuser' host='localhost' password='dbpass'") #might only need dbname and user?
except:
    print("FAILURE TO CONNECT TO DATABASE")
    exit()

curr = conn.cursor() #open cursor for operations
curr.execute("""SELECT * from template1""") # select all data from db

records = curr.fetchall() #set records to pull all data from database

#EXAMPLE:
#first column: group_name
#second column: first_name
#third column: email
#fourth columnm recipients' email

people = {} #empty dictionary. The keys will be the emails of people

class Person:
    def _init_(self, group_name , person_name , email , recipient):
        self.group_name = group_name #The group name this person belongs to
        self.person_name = person_name #The persons name
        self.email = email #The person email
        self.recipient_email = recipient_email #Who the person is giffting (MUST BE OF PERSON DATA TYPE)

for row in records:
    temp_person = Person(row[0] , row[1] , row[2] , row[3])
    people[temp_person.email] = temp_person #each email is unique so nothing in dictionary will get overwritten

#In order to send emails out, loop through the dictionary:

for key in people:
    person_var = people[key]
    person_var_recipients_email = person_var.recipient_email
    person_var_recipient_name = people[person_var_recipients_email].email

    #run email code in this loop
