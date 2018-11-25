
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine


engine = create_engine('sqlite:///red_search.db', echo=True)
metadata = MetaData()


chapters = Table('chapters', metadata,
     Column('id', Integer, primary_key=True),
     Column('subreddit', String),
     Column('chapter_number', Integer),
	 )


metadata.create_all(engine)
conn = engine.connect()



def insert_subreddit(name, last_chapter):
	command = chapters.insert().values(subreddit = name, chapter_number = last_chapter)
	conn.execute(command)

insert_subreddit('BokuNoHeroAcademia',207)