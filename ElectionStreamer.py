#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "101639713-8HcKbxzh8KjwAdEH2r0FKcowaqzcXnJ7HwWUJPit"
access_token_secret = "g8Mm5UjniLEVb8uLbdfOAAjyTE1NjNTYKlvhqXkrjbtwW"
consumer_key = "vUyZ0XaxIIXYLQ8T9OhZxzYRp"
consumer_secret = "wmbzSkiozPuBvYrGppsQSpv5D3pcvcGlOQlbSNLM4q0voAJOMQ"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: "#debate","#debate2016","@hillaryclinton","@realdonaldtrump"
    stream.filter(track=["#election","#election2016","@hillaryclinton","@realdonaldtrump"])




