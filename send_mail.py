import smtplib
from email.mime.text import MIMEText


def send_mail(member, email, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '3e16d738a72cf4'
    password = 'bbcd6703450f79'
    messsage = f"<h3>New Feedback Submission</h3><ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'email1@example.com'
    receiver_email = 'email2@example.com'
    msg = MIMEText(messsage, 'html')
    msg['Subject'] = 'Secret Santa Responses'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())