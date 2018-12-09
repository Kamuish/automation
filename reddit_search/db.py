
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.sql import select


engine = create_engine('sqlite:///red_search.db', echo=False)
metadata = MetaData()


chapters = Table('chapters', metadata,
     Column('id', Integer, primary_key=True),
     Column('subreddit', String),
     Column('chapter_number', Integer),
	 )


metadata.create_all(engine)
conn = engine.connect()



def insert_subreddit(name, last_chapter):
	"""
	Inserts a subreddit in the db, as well as the number of the last read chapter
	"""
	if conn.execute(select([chapters]).where(chapters.c.subreddit == name)).fetchall() != []:
		return    # Avoids repetitions
	command = chapters.insert().values(subreddit = name, chapter_number = last_chapter)
	conn.execute(command)

def get_all_subs():
	"""
	returns all the existing subreddits in the db
	"""

	result = conn.execute(select([chapters])).fetchall()
	return result

def update_subreddit(name):
	"""
	Updates the chapter number to +1. I.e. the user has read a chapter and it updates the value
	"""
	result = conn.execute(select([chapters]).where(chapters.c.subreddit == name)).fetchall()
	
	stmt = chapters.update().where(chapters.c.subreddit == name).values(chapter_number = result[0][2] + 1)
	conn.execute(stmt)
	return result

