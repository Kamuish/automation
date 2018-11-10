
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main(filename, main_email, main_pw):


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
    fromaddr = main_email
    subject = 'Secret friend!!'

    for key,value in pairs.items():
        if key ==value:
            print('fuck')
        receiver = info[value]

        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = receiver
        msg['Subject'] = subject
        
         
        body = f'{key}, your secret friend is {value}'
        msg.attach(MIMEText(body, 'plain'))


        server.sendmail(fromaddr, receiver, msg.as_string())
    server.close()

        


if __name__ == '__main__':
    main('emails.txt','placeholder@pla.com','pw')