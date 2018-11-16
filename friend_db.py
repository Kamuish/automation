
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy import Table, Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.sql import select
Base = declarative_base()

conn = create_engine('sqlite:///friends.db', echo=False)

Session = sessionmaker(bind=conn)
session = Session()


association_table = Table('association', Base.metadata,
    Column('gift_id', Integer,ForeignKey('gifts.id')),
    Column('members', Integer, ForeignKey('user.id')),
)


class Users(Base):
    __tablename__ = 'user'
    id = Column( Integer, primary_key=True)
    name = Column(String(20), nullable = False)
    email = Column(String(120), unique = True, nullable = False)
    year = Column(Integer, nullable = False,default =datetime.now().year)
    #image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    
    exchanges = relationship("Gifts",
                    secondary=association_table,
                    backref="members")

    def __repr__(self):
        print(f"User {self.name}, with email {self.email}")

class Gifts(Base):
    __tablename__ = 'gifts'
    id = Column( Integer, primary_key=True)
    year = Column(Integer, nullable = False,default =datetime.now().year)
    #image_file = db.Column(db.String(20), nullable = False, default='default.jpg')


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
    print(result)
    return result[0]



def insert_gift(gifter_id,receiver_id,year = None):
    try:
        gifter = select_user(gifter_id)
        receiver = select_user(receiver_id)

        if year is not None:
            gift = Gifts(year = year)
            gifter.exchanges.append(gift)
            receiver.exchanges.append(gift)

            session.add(gift)
            session.commit()
        else:
            conn.execute(gift.insert().values(name = name,email = email))
    except Exception as e:
        print(e)
        pass
#manual_insert_user('a','adas')

def check_pair(gifter_id, receiver_id, time_span):
    s = select([association_table.c.members == gifter_id])
    result = session.execute(s).first()
    [print(a) for a in result]


check_pair(1,2,1)

user = select_user(1)