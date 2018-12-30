import praw
from queries import start_connection, find_match
from db import get_all_subs

from win10toast import ToastNotifier




def main():
	reddit_instance = start_connection()

	subs = get_all_subs()
	matches = []

	for subreddit in subs:
		result = find_match(reddit_instance,subreddit[1], subreddit[2])
		result = 0
		if 0 == result:
			matches.append(subreddit[1])

	toaster = ToastNotifier()
	toaster.show_toast("Things to read/see:",
	                   "\n".join(matches),
	                   duration=10)

main()