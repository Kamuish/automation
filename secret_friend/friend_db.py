
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_

import logging 


Base = declarative_base()

conn = create_engine('sqlite:///friends.db', echo=False)

Session = sessionmaker(bind=conn)
session = Session()


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s -  %(levelname)s:%(name)s:%(message)s')
file_handler = logging.FileHandler('db.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)



class Users(Base):
    __tablename__ = 'user'
    id = Column( Integer, primary_key=True)
    name = Column(String(20), nullable = False)
    email = Column(String(120), unique = True, nullable = False)
    year = Column(Integer, nullable = False,default =datetime.now().year)
    #image_file = db.Column(db.String(20), nullable = False, default='default.jpg')


    def __repr__(self):
        return(f"User {self.name}, with email {self.email}")

class Gifts(Base):
    __tablename__ = 'gifts'
    id = Column( Integer, primary_key=True)
    year = Column(Integer, nullable = False,default =datetime.now().year)
    gifter = Column(Integer, nullable = False)
    receiver = Column(Integer, nullable = False)

    def __repr__(self):
        return(f"Gift from {self.gifter} to {self.receiver} on year {self.year}")


Base.metadata.create_all(conn)



def manual_insert_user(name,email):
    try:
        result_mail = session.query(Users).filter_by(email = email).all()
        result_user = session.query(Users).filter_by(name = name).all()

        if result_mail != []:
            print("Email  already exists")
            logger.warning(f"Repated Email {email}")
            return -1 
        if result_user != []:
            logger.warning(f"Repated name {name}")
            print("Name  already exists")
            return -1 

        user = Users(name = name,email = email)
        session.add(user)
        session.commit()
    except Exception as e:
        print(e)
        pass

def select_user(user_id):
    try:
        result = session.query(Users).filter_by(id = user_id).all()
        return result[0]
    except:
        return -1


def insert_gift(gifter_id,receiver_id,year = None):
    try:
        gifter = select_user(gifter_id)
        receiver = select_user(receiver_id)

        if has_match(gifter_id,receiver_id,datetime.now().year):
            print("Already one match in this year")
            return -1

        if gifter == -1 or receiver == -1 :

            return -1 

        if year is not None:
            gift = Gifts(year = year, gifter = gifter_id, receiver = receiver_id)

            session.add(gift)
            session.commit()
        else:
            gift = Gifts(gifter = gifter_id, receiver= receiver_id)

            session.add(gift)
            session.commit()
    except Exception as e:
        print(e)
        return -1



def has_match(gifter_id, receiver_id, start_year):
    """
    time_span: number of years allowed between repeated gifts
    """

    s = session.query(Gifts).filter(
                and_(
                Gifts.gifter.like(gifter_id),
                Gifts.receiver.like(receiver_id)
                )
            )

    
    result = list(session.execute(s))
    try:
        if result[-1] is not None:
            if  result[-1][1] >=  start_year:
                return True
            else:
                return False

    except Exception as e: 
        print(e)
        pass


if __name__ == '__main__':
    print(select_user(2))