#https://www.youtube.com/watch?v=QnDWIZuWYW0
from flask import Flask, render_template, request, redirect, url_for#include for url generator
from flask_mail import Mail, Message
#import smtplib#include
from itsdangerous import URLSafeSerializer#include for URL generator
from threading import Thread#include for asynch emailing


app = Flask(__name__) #This is for the app


#in program -- use app.config.from_pyfile('config.cfg')
app.config.update(#include
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'ec327emailb@gmail.com',
	MAIL_PASSWORD = #'#see me for this ,
    	SECRET_KEY = #see me for this,
    	MAIL_MAX_EMAILS = 1000
	)

mail=Mail(app) #include
s = URLSafeSerializer(app.config['SECRET_KEY']) #include


users = [{'GroupID': '1', 'UUID': '1', 'name': 'wiley', 'email': 'whunt@bu.edu'}, {'GroupID': '1', 'UUID': '2', 'name': 'wiley', 'email': 'wileyhunt65@gmail.com'}]

def generate_token(email): #This function generates our email token
    token = s.dumps(email, salt= 'email-confirm')
    return token

def send_async_email(msg):#This function sends asynchronous email
    with app.app_context():
        mail.send(msg)




@app.route('/')#don't inclide
@app.route('/home')
def home():
    return "<h1>Hello Ken<h1>"

@app.route('/about')#don't include
def about():
    return 'Hi Ken'
 

@app.route('/bulk/', methods = ['GET']) # The following is designed to send bulk emails. This holds the connection open (slow but reliable)
def bulk():
    if request.method == 'GET':
        with mail.connect() as conn:
            try:
                for user in users:
                    token = generate_token(user['email'])
                    link = url_for('wishlist', token = token, _external = True)
                    msg = Message('Hello from Optimal Secret Santa!',#subject
                    sender = 'ec327emailb@gmail.com',
                    recipients= [user['email']])
                    msg.body = F"Hi {user['name']}\nGreetings from the North Pole!\nYou have been added to a Secret Santa group created on OptimalSecretSanta.com.nPlease use the below link (along with your personal and group identifier) to fill out the wishlist/message you would like to send your Secret Santa\n\nLink:{link}\nGroupID: {user['GroupID']}\nUserID: {user['UUID']}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta."
                    #msg.html = render_template('/msg.html', name = user['name'], GroupId = user['GroupID'], UUID = user['UUID'], link=link)
                    conn.send(msg)
                return 'Emails Sent!'
            except Exception as e:
                return str(e)
    else:
        return "Invalid"

@app.route('/send/', methods = ['GET']) # asynchrnous sending -- fast but no immediate error messages
def send():
    if request.method == 'GET':
        try:
            for user in users:
                token = generate_token(user['email'])
                link = url_for('wishlist', token = token, _external = True)
                msg = Message('Hello from Optimal Secret Santa!',#subject
                sender = 'ec327emailb@gmail.com',
                recipients= [user['email']])
                msg.body = F"Hi {user['name']}\nGreetings from the North Pole!\nYou have been added to a Secret Santa group created on OptimalSecretSanta.com.nPlease use the below link (along with your personal and group identifier) to fill out the wishlist/message you would like to send your Secret Santa\n\nLink:{link}\nGroupID: {user['GroupID']}\nUserID: {user['UUID']}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
                thr = Thread(target=send_async_email, args=[msg])
                thr.start()
            return 'Emails Sent!'
        except Exception as e:
            return str(e)
    else:
        return "Invalid"



@app.route('/wishlist')#don't include - for testing
def wishlist():
    return 'Hi Ken'

if __name__== '__main__':
    app.run(debug=True)
