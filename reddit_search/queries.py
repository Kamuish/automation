import praw
import yaml
from db import get_template
def start_connection():
	with open('config.yaml', 'r') as stream:  # 'document.yaml' contains a single YAML document.
	        kwarg = yaml.load(stream)

	reddit = praw.Reddit(client_id= kwarg['client_id'],
	                     client_secret= kwarg['client_secret'],
	                     password= kwarg['password'],
	                     user_agent= kwarg['user_agent'],
	                     username= kwarg['username'])
	return reddit


def find_match(reddit, sub_name, chapter_number):
	"""
		Checks for template matches in the hot section of the subreddit
	"""

	subreddit = reddit.subreddit(sub_name)

	found = False
	template = get_template(sub_name)
	desired_title = template.replace('$',str(chapter_number))
	for submission in subreddit.hot():
		if desired_title in submission.title :
			print(submission.title)

			found = True
			return 0

	if not found:
		return 1



if __name__ == '__main__':
	reddit = start_connection()
	find_match(reddit,'BokunoHeroAcademia',207)



