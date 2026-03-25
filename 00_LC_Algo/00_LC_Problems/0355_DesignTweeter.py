import heqpq


class User:
    def __init__(self, userId: int):
        self.userId = userId
        self.followees = set()
        self.last_tweet_dummy = Tweet(-1, -1)

    def add_ tweet(self, tweetId: int, tweet_count: int):
        new_tweet = Tweet(tweetId, tweet_count,self.last_tweet_dummy.prev)
        prev =  new_tweet.prev
        new_tweet.prev =  prev
        self.last_tweet_dummy.prev = new_tweet

class Tweet:
    def __init__(self, tweetId: int, idx: int, prev: Tweet = None):
        self.tweetId = tweetId
        self.idx = idx 
        self.prev = prev 

class Twitter:

    def __init__(self):
        self.heap = []
        self.tweet_count = 0 
        

    def postTweet(self, userId: int, tweetId: int) -> None:
        

    def getNewsFeed(self, userId: int) -> List[int]:
        

    def follow(self, followerId: int, followeeId: int) -> None:
        

    def unfollow(self, followerId: int, followeeId: int) -> None: 
        

