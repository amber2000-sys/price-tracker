import smtplib, ssl

port = 465 
SENDER_EMAIL = 'triplem656@gmail.com'
PASSWORD = 'lqcytandnnumtydt'
context = ssl.create_default_context()

def sendMail(reciever, message):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, reciever, message)