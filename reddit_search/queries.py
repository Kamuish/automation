import praw
import yaml

def start_connection():
	with open('config.yaml', 'r') as stream:  # 'document.yaml' contains a single YAML document.
	        kwarg = yaml.load(stream)

	reddit = praw.Reddit(client_id= kwarg['client_id'],
	                     client_secret= kwarg['client_secret'],
	                     password= kwarg['password'],
	                     user_agent= kwarg['user_agent'],
	                     username= kwarg['username'])
	return reddit


def find_match(reddit,sub_name, chapter_number):
	subreddit = reddit.subreddit(sub_name)

	for submission in subreddit.hot():
		if f'Chapter {chapter_number}' in submission.title :
			print(submission.title)

reddit = start_connection()
find_match(reddit,'BokunoHeroAcademia',207)
print(reddit.user.me())




