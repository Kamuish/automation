
import random


def main(filename):
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

    print(pairs)

    for key,value in pairs.items():
        if key ==value:
            print('fuck')
        print(f"send mail from {info[key]} to {info[value]}")



if __name__ == '__main__':
    main('emails.txt')