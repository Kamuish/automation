
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
from friend_db import manual_insert_user, insert_gift, has_match, select_user
# https://stackoverflow.com/questions/18156485/receive-replies-from-gmail-with-smtplib-python
from datetime import datetime
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -  %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def import_from_file(filename):
    """
    Extracts the names and emails from filename and stores new users on the database
    IN the file name we expect to have the name and email of the people participating on
    secret friend
    
    :param: filename: path to file

    each line of the file should have the format:

    username ; email
    """
 
    with open(filename,'r') as file:
        for line in file:
            name,mail = line.split(';')
            name = name.strip()
            mail = mail.strip()

            manual_insert_user(name,mail)


def import_gifts_from_file(filename):
    """
    Creates gifts on the database between the users with emails specified on
    the database, on the specified year

    :param: filename: path to file

    each line of the file should have the format:

        sender email ; receiver email; year
    """
 
    with open(filename,'r') as file:
        for line in file:
            try:
                sender_mail,receiver_mail,year = line.split(';')
                sender_mail = sender_mail.strip()
                receiver_mail = receiver_mail.strip()
                year = int(year.strip())

                gifter = select_user(sender_mail, method = 2)
                receiver = select_user(receiver_mail, method = 2)

                insert_gift(gifter.id,receiver.id, year)
            except:
                logger.error("Couldn't extract gifts",exc_info=True)
                return -1
        return 0



def send_email(server,main_email,subject,gifter_name,gifter_email,receiver_name):
    """
    Sends an email notifying the receiver of the person he has to give a gift.

    :param: server - email server
    :param: main_email - email from which the emails will be sent
    :param: subject - subject of the email
    :param: gifter_name - name of the person sendin the gift
    :param: gifter_email - email of the gifter
    :param: receiver_name - name of the receiver

    """

    msg = MIMEMultipart()
    msg['From'] = main_email
    msg['To'] = gifter_email
    msg['Subject'] = subject
     
    body = f'{gifter_name}, your secret friend is {receiver_name}'
    msg.attach(MIMEText(body, 'plain'))

    server.sendmail(main_email, gifter_email, msg.as_string())



def create_pairs(user_ids,year_thresh, main_email, main_pw):
    """
    Randomly matches two persons for secret friend gifting. Each element will receive
    an email with one name.

    :param: filename: path to file with names and emails separated by a ";"
    :param: main_email: email from which the notices will be sent. COnfigured for gmail
    :param: main_pw: password for the email. Must be gmail's app password
    :return:
    """

    senders = user_ids.copy()
    receivers = user_ids.copy()

    pairs ={}

    for j in range(len(user_ids)):

        a = random.choice(senders)
        b = random.choice(receivers)
        count = 0

        while has_match(a,b,year_thresh) or a == b:
            a = random.choice(senders)
            b = random.choice(receivers)
            count += 1

            if count > 1000:
                print("Could not find match")
                logger.fatal('Could not find reliable matches')
                return -1
        pairs[a] = b

        senders.remove(a)
        receivers.remove(b)

    checks = {}
    for j in user_ids:
        x = [0,0]
        if j in pairs:
            x[0]= 1
        if j in pairs.values():
            x[1] = 1
        checks[j] = x
    


    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(main_email,main_pw)
    subject = 'Secret friend!!'

    for key,value in pairs.items():
        if key ==value:
            print('OH GOD NO')
            return
        sender = select_user(key)
        receiver = select_user(value)
        send_email(server,main_email,subject,sender.name, sender.email,receiver.name)
        insert_gift(key,value,datetime.now().year)
    server.close()

        


if __name__ == '__main__':
    main('emails.txt','placeholder@pla.com','pw')

