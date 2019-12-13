#This file to use Twitter API and retreive tweets using keyword searches. The aim here is to get all the tweets
#from last week that records data breaches in the companies and the number of records exposed

#To get the Tweet's data breach numbers
#twitter_search()
#----------------------------------------------------------------------------------------------------------------------------------------------------------

#import for using tweepy library in python to retreive tweets
import tweepy as tw

class tweet_word_search():
    def __init__(self):
        
        #setting all the keys and tokens provided by the API
        self.consumer_key = 'QNyBCFphPNU0DpmuxS4mQ6aN6'
        self.consumer_secret = 'r7hyIj8hfJY7ZdgEMXfIhgK6yCjLtbr2D0P5kAvvkUAj0CY4ZA'
        self.access_token = '573706929-RhWm0TgQvJpK44wefqCXE8IHFCtou2ZRrxg6QdTN'
        self.access_token_secret = 'ywCeCngWVliWwZiKdIPlwZuAVvVfZNJ8TgsCE8OkvYvbt'
        
        #trying to connect to Twitter using tweepy's OAuthHandler and passing the tokens and keys
        try:
            self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
            self.auth.set_access_token(self.access_token, self.access_token_secret)
            self.api = tw.API(self.auth, wait_on_rate_limit=True)
        
        except Exception as e:
            print(f"Something went wrong! {e}")
        
    #function to get the Tweet's data breach numbers
    def twitter_search(self):
        #setting the query parameter, return tweets shouldn't containt retweets or replies
        self.q = '#databreach exposed million -filter:retweets -filter:replies (data OR account)' 
        self.date_since = "2019-01-01"
        
        #sending the query to twitter using api.search and parameters. Retreive extended version of the tweets and obtain 1000 items
        self.tweets = tw.Cursor(self.api.search, q=self.q, lang="en", since=self.date_since, tweet_mode="extended").items(1000)
        self.tweet_url = []
        self.tweet_breach_data = []
        self.tweet_data = []
        self.tweet_full_text_list = []
        
        for tweet in self.tweets:
            
            #splitting the tweet text to list items to obtain the data breach's number
            self.tweet_full_text_list = tweet.full_text.split()
            for i,j in enumerate(self.tweet_full_text_list[:-1]):
                try:
                    
                    #checking if the list item can be converted to float, indicates that the item is a number
                    if isinstance(float(self.tweet_full_text_list[i]), float):
                        
                        #checking if the next word is a number to check the number of million data exposed
                        if self.tweet_full_text_list[i+1].lower() == "million":
                            for url in tweet.entities['urls']:
                                
                                #checking if the tweet consists of URLS attached, then add the URL and breach number to list
                                if url['expanded_url'] != "":
                                    self.tweet_breach_data.append(float(self.tweet_full_text_list[i]))
                                    self.tweet_url.append(url['expanded_url'])
                                else:
                                    continue
                except:
                    pass
            
        #mapping the breach data and url into a list                
        self.tweet_data = list(zip(self.tweet_breach_data, self.tweet_url))
        return self.tweet_data