
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.sql import select


engine = create_engine('sqlite:///red_search.db', echo=False)
metadata = MetaData()


chapters = Table('chapters', metadata,
     Column('id', Integer, primary_key=True),
     Column('subreddit', String),
     Column('chapter_number', Integer),
     Column('title_style', String),
	 )


metadata.create_all(engine)
conn = engine.connect()



def insert_subreddit(name, last_chapter, title_style):
	"""
	Inserts a subreddit in the db, as well as the number of the last read chapter

	Title style will be a fixed template, with $ in the place of the chapter number.

		IF we wish to enter the template for bokunoheroacademia chapters, we do:
			Chapter $ - Links and Discussion
	"""
	find_equal = conn.execute(select([chapters]).where(chapters.c.subreddit == name)).fetchall()
	allow = False
	if find_equal != []:
		for sub in find_equal: # avoids repetitions of equal title styles but allows tracking more than one instance from each sub
			if sub[-1] == title_style:
				return -1
	command = chapters.insert().values(subreddit = name, chapter_number = last_chapter, title_style = title_style)
	conn.execute(command)
	return 0

def get_all_subs():
	"""
	returns all the existing subreddits in the db
	"""

	result = conn.execute(select([chapters])).fetchall()
	return result

def get_template(name):
	"""
		Returns the template for the subreddit "name"
	"""
	result = conn.execute(select([chapters]).where(chapters.c.subreddit == name)).fetchall()

	return result[-1][-1]

def update_subreddit(name):
	"""
	Updates the chapter number to +1. I.e. the user has read a chapter and it updates the value
	"""
	result = conn.execute(select([chapters]).where(chapters.c.subreddit == name)).fetchall()
	
	stmt = chapters.update().where(chapters.c.subreddit == name).values(chapter_number = result[0][2] + 1)
	conn.execute(stmt)
	return result



if __name__ == '__main__':
	print(insert_subreddit('OnePiece',928,'One Piece: Chapter $'))
