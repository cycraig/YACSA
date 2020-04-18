from flask_restx import Namespace, Resource, fields
from .sentiment import predict_reddit_sentiment
from datetime import datetime, timedelta, timezone
import dateutil.parser as dt

api = Namespace('sentiment', description='Cryptocurrency social media sentiment')

# TODO: return aggregate sentiment _and_ volume, or split endpoints?
sentiment_request = api.model('SentimentRequest', {
    'datetime': fields.DateTime(required=True, dt_format='iso8601', description='The datetime to analyse in UTC ISO 8601 format (will be truncated to the hour).'),
});

sentiment_response = api.model('SentimentResponse', {
    'sentiment': fields.Fixed(decimals=4, description='Cryptocurrency sentiment [-1,1] for the requested time period.'),
});

@api.route('/')
class Sentiment(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @api.doc('post_sentiment')
    @api.expect(sentiment_request)
    @api.marshal_with(sentiment_response)
    def post(self):
        '''Request sentiment for a particular hour'''
        # TODO: production logging
        
        # truncate to the hour
        start_epoch = dt.parse(api.payload['datetime'])
        start_epoch = start_epoch.replace(minute=0, second=0, microsecond=0)
        end_epoch = start_epoch + timedelta(hours=1)
        
        # reject any time more than 24 hours in the past for now...
        now = datetime.now(timezone.utc)
        diff = now - start_epoch
        if diff.total_seconds() / 3600 >= 24:
            api.abort(400, "{} is more than 24 hours in the past".format(start_epoch))
            
        print(start_epoch)
        print(end_epoch)
        print(now)
        # TODO: store results in a database, use a put/post to update it (secured endpoint)
        # TODO: psaw isn't returning the most recent posts (posted 31 minutes ago etc.)
        #       Either the UTC is wrong or it's delayed, so maybe make the time range more coarse like per day?
        sentiment = predict_reddit_sentiment(start_epoch, end_epoch)
        return {'sentiment': sentiment}
