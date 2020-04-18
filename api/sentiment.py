from typing import List
from psaw.PushshiftAPI import PushshiftAPI
from datetime import datetime

import flair
#from textblob import TextBlob
#from nltk.sentiment.vader import SentimentIntensityAnalyzer

psaw = PushshiftAPI()
sentiment_model = flair.models.TextClassifier.load('en-sentiment')

def classify(text: str):
    sent = flair.data.Sentence(text)
    return sentiment_model.predict(sent)

def predict_reddit_sentiment(start_datetime: datetime, end_datetime: datetime) -> float:
    posts = get_reddit_posts(start_datetime, end_datetime)
    for p in posts:
        text = p.title
        if hasattr(p, 'selftext'):
            text += " " + p.selftext
        print(text,":",classify(text)[0].labels)#, TextBlob(text).sentiment)
    return 0
        
def get_reddit_posts(start_datetime: datetime, end_datetime: datetime) -> List:
    start_epoch = int(start_datetime.timestamp())
    end_epoch = int(end_datetime.timestamp())
    
    posts = list(psaw.search_submissions(
                            after=start_epoch,
                            before=end_epoch,
                            subreddit='cryptocurrency',
                            filter=['title','selftext'],
                            limit=1000))
    return posts
