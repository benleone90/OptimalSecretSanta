# added by Wiley for link gen
from flask import Flask, render_template, request, url_for
from flask_mail import Mail, Message  # added by Wiley for flaskmail
from itsdangerous import URLSafeSerializer  # added by Wiley for url generator
from threading import Thread  # added by Wiley for asynch emailing
# from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import random
#added to create engine:
from sqlalchemy import create_engine


class Person:
    def __init__(self, member , email , partner_email, partner_wishlist):
        self.member = member #The persons name
        self.email = email #The person email
        self.partner_email = partner_email #Who the person is giffting
        self.partner_wishlist = partner_wishlist #The partner's wishlist


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config.update(  # added by Wiley
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='OptimalSecretSanta@gmail.com',
    MAIL_PASSWORD='MAIL_PASSWORD',
    SECRET_KEY='SECRET_KEY',
    MAIL_MAX_EMAILS=1000
)

mail = Mail(app)  # added by Wiley
s = URLSafeSerializer(app.config['SECRET_KEY'])  # added by Wiley


def generate_token(email):  # added by Wiley
    token = s.dumps(email, salt='email-confirm')
    return token


def send_thread_email(msg):  # added by Wiley
    with app.app_context():
        mail.send(msg)


ENV = 'STATE'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:g4qtyx7v@localhost/test_db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zyyzysejezblhz:17a351947912f2433f7d4ca45121650d224b002543e633d521e57d4c4bb6d874@ec2-174-129-253-63.compute-1.amazonaws.com:5432/ddui50dco58tad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class SecretSanta(db.Model):
    __tablename__ = 'secretsanta'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(200), unique=True)
    member = db.Column(db.String(200))
    email = db.Column(db.String(200), unique=True)
    wishlist = db.Column(db.Text())
    partner = db.Column(db.String(200))

    def __init__(self, member, email, partner):
        self.member = member
        self.email = email
        # self.uuid = uuid
        # self.wishlist = wishlist
        self.partner = partner


def generate_pairings(emails):
    f = {}  # dict containing name:group
    for i, line in enumerate(emails):
        group = line.strip().split(" ")
        f.update({p: i for p in group})
    names = list(f.keys())

    while True:
        random.shuffle(names)
        assignments = {a: b for a, b in zip(names, names[1:] + [names[0]])}
        if all([f[a] != f[b] for a, b in assignments.items()]):
            break
    pairs = [None]*len(names)
    for a, b in assignments.items():
        pairs[f[a]] = b
    return pairs

def send_thread_email(msg):#added by Wiley
    with app.app_context():
        mail.send(msg)

###########################################################################################################

 #each email(ie. key) is unique so nothing in dictionary will get overwritten


#####################################################################################################
#people dictionary is filled at this point, wich each email acting as a key for each person

#for key in people:
#    user_member = people[key].member #The user's name
#    user_email = people[key].email #The user's email (could just as easily use key instead of people[key].email)
#    user_partner_email = people[key].partner_email #The email of the user's recipient
#    user_partner_name = people[user_partner_email].member #The name of the user's recipient
#    user_partner_wishlist = people[user_partner_email].wishlist #The wishlist of the user's recipient

#    msg = Message('Hello from Optimal Secret Santa!',  # subject
#                  sender='OptimalSecretSanta@gmail.com',
#                  recipients=[user_email])
#    msg.body = F"Hi {user_member},\n\nGreetings from the North Pole!\n\nYour Secret Santa is {user_partner_name}.\n\nPlease use the below link to fill out the wishlist/message you would like to send your Secret Santa.\n\nLink:{link}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
#    thr = Thread(target=send_thread_email, args=[msg])
#    thr.start()

#####################################################################


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        member = request.form.getlist('member')
        email = request.form.getlist('email')
        pair = generate_pairings(email)
        print(member, email, pair)

        for ii in range(len(member)):
            if member[ii] == '' or email[ii] == '':
                return render_template('index.html', message='Please ensure all fields are entered')
            # elif: // Email validation goes here (Using email-validator pkg from pip)

            else:
                try:
                    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
                    records = engine.execute('SELECT * FROM "secretsanta"').fetchall()
                except:
                    print("FAILURE TO CONNECT TO DATABASE")
                    exit()

                for row in records['partner']:
                    if row == email:
                        who_to_email = records[row]['email'] #who we are emailing
                        break
                    else:
                        continue
                        
                for other_row in records['email']:
                    if other_row == email
                        name_of_secret_santa = records[other_row]['member'] #the name of the person who submitted the wishlist
                        break
                    else:
                        continue

                    msg = Message('Your Secret Santa Assignment is in!',  # subject
                                  sender='OptimalSecretSanta@gmail.com',
                                  recipients=[who_to_email])
                    msg.body = F"Hi {name_of_who_to_email},\n\n You have been assigned as the Secret Santa for {name_of_secret_santa}.Their wishlist is included below: \n\n{wishslist}\n\nHappy Holidays!\n\nSincerely,\nOptimalSecretSanta"
                    thr = Thread(target=send_thread_email, args=[msg])
                    thr.start()  # wiley add end
                else:
                    return render_template('index.html', message='A user with this email is already a part of Secret Santa')
        db.session.commit()
        return render_template('success.html')


@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist(user_id):
    return render_template('wishlist.html')


if __name__ == '__main__':
    app.run(debug=True)
