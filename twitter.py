#coding: utf-8
import oauth2 as oauth
import urllib
import json
import sys
import console

twitter_api = 'https://api.twitter.com/1/'
consumer_key = ''
consumer_key_secret = ''
access_token = ''
access_token_secret = ''

consumer = oauth.Consumer(key=consumer_key, secret=consumer_key_secret)
token = oauth.Token(key=access_token, secret=access_token_secret)
client = oauth.Client(consumer, token)
size = console.getTerminalSize()
width = size[0] - (15+1)

def home_timeline():
    url = twitter_api + "statuses/home_timeline.json?count=100"
    content = client.request(url, "GET")
    tweets = list(json.loads(content[1]))
    print_tweets(tweets)

def mentions():
    url = twitter_api + "statuses/mentions.json"
    content = client.request(url, "GET")
    tweets = list(json.loads(content[1]))
    print_tweets(tweets)

def search(query):
    query = unicode(query, 'utf-8')
    query = urllib.quote(query)
    url = twitter_api + "search.json?q=" + query
    content = client.request(url, "GET")
    response = json.loads(content[1])
    tweets = list(response['results'])
    print_tweets(tweets, True)

def update(status):
    status = unicode(status, 'utf-8')
    url = twitter_api + "statuses/update.json?status=" + status
    content = client.request(url, "POST")
    if int(content[0]['status']) == 200:
        dictionary = json.loads(content[1])
        print 'poseted: %s' % dictionary['text'] 
    else:
        print 'failed.'

def print_tweets(tweets, search_flag = False):
    tweets.reverse()
    for tweet in tweets:
        if search_flag:
            print "%15s" % tweet['from_user']
        else:
            user = tweet['user']
            print "%15s" % user['screen_name'],
        flag = False
        for string in console.splitByLength(tweet['text'], width):
            if flag:
                print "%15s" % "",
            print string
            flag = True

if __name__ == "__main__":
    arg = None
    if len(sys.argv) > 1:
        arg = sys.argv[1]
    if arg == "mentions":
        mentions()
    elif arg == "search":
        search(sys.argv[2])
    elif arg == "update":
        update(sys.argv[2])
    else:
        home_timeline()
