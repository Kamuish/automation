
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def import_from_file(filename):
    """
    Extracts the names and emails from filename

    :param: filename: path to file
    :return: dict pairing names and emails and list of names
    """
    info = {}
    names =[]
    with open(filename,'r') as file:
        for line in file:
            name,mail = line.split(';')
            name = name.split()
            mail = mail.split()
            if name[0] in info or mail[0] in info.values():
                print(f"User {name[0]}, with mail {mail[0]} already exists")
            else:
                info[name[0]] = mail[0]
                names.append(name[0])
    return info,names

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

def main(filename, main_email, main_pw):
    """
    Randomly matches two persons for secret friend gifting. Each element will receive
    an email with one name.

    :param: filename: path to file with names and emails separated by a ";"
    :param: main_email: email from which the notices will be sent. COnfigured for gmail
    :param: main_pw: password for the email. Must be gmail's app password
    :return:
    """

    info,names = import_from_file(filename)


    senders = names.copy()
    receivers = names.copy()
    pairs ={}

    for j in range(len(names)):
        a,b = 0,0
        while a ==b:
            a = random.choice(senders)
            b = random.choice(receivers)

        pairs[a] = b

        senders.remove(a)
        receivers.remove(b)

    
    checks = {}
    for j in names:
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

        send_email(server,main_email,subject,key,info[key],value)
        
    server.close()

        


if __name__ == '__main__':
    main('emails.txt','placeholder@pla.com','pw')