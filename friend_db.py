
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.sql import select
from sqlalchemy.sql.expression import and_

Base = declarative_base()

conn = create_engine('sqlite:///friends.db', echo=False)

Session = sessionmaker(bind=conn)
session = Session()





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
        user = Users(name = name,email = email)
        session.add(user)
        session.commit()
    except Exception as e:
        pass

def select_user(user_id):
    result = session.query(Users).filter_by(id = user_id).all()
    return result[0]



def insert_gift(gifter_id,receiver_id,year = None):
    try:
        gifter = select_user(gifter_id)
        receiver = select_user(receiver_id)

        if year is not None:
            gift = Gifts(year = year, gifter = gifter_id, receiver = receiver_id)

            session.add(gift)
            session.commit()
        else:
            gift = Gifts(gifter = gifter_id, receiver= receiver_id)

            session.add(gift)
            session.commit()
    except Exception as e:
        raise(e)
        pass
#manual_insert_user('a','adas')

def check_pair(gifter_id, receiver_id, time_span):
    s = session.query(Gifts).filter(
                and_(
                Gifts.gifter.like(gifter_id),
                Gifts.receiver.like(receiver_id)
                )
            )

    result = session.execute(s).first()
    print(result)


#manual_insert_user('aa','ba')
insert_gift(1,2)
check_pair(2,1,1)

user = select_user(1)

