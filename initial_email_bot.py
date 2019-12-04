#https://www.youtube.com/watch?v=QnDWIZuWYW0
from flask import Flask, request, redirect, url_for#be sure to include last 2 for token generator
from flask_mail import Mail, Message
#import smtplib#include
from itsdangerous import URLSafeSerializer#include for url generator
from threading import Thread


app = Flask(__name__) #This is for the app


#in program -- use app.config.from_pyfile('config.cfg')
app.config.update(#include
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'ec327emailb@gmail.com',
	MAIL_PASSWORD = ,
    SECRET_KEY = ,
    MAIL_MAX_EMAILS = 1000
	)

mail=Mail(app) #include
s = URLSafeSerializer(app.config['SECRET_KEY']) #include


emails = ['wileyhunt65@gmail.com', 'whunt@bu.edu']

def generate_token(email): #include
    token = s.dumps(email, salt= 'email-confirm')
    return token



@app.route('/')#don't inclide
@app.route('/home')
def home():
    return "<h1>Hello Ken<h1>"

@app.route('/about')#don't include
def about():
    return 'Hi Ken'
 

@app.route('/bulk/', methods = ['GET']) # actual email
def bulk():
    if request.method == 'GET':
        with mail.connect() as conn:
            try:
                for email in emails:
                    token = generate_token(email)
                    link = url_for('wishlist', token = token, _external = True)
                    msg = Message('Hello from Optimal Secret Santa!',#subject
                    sender = 'ec327emailb@gmail.com',
                    recipients= [email])
                    msg.body = f"Ho ho ho! \n You have been added to a new Secret Santa Group.\nHere's a link to enter your wishlist for YOUR Secret Santa: {link}"
                    conn.send(msg)
                    # mail.send(msg)
                return 'Emails Sent!'
            except Exception as e:
                return str(e)
    else:
        return "Invalid"




@app.route('/wishlist')#don't include - for testing
def wishlist():
    return 'Hi Ken'

if __name__== '__main__':
    app.run(debug=False)
