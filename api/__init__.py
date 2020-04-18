from flask_restx import Api

from .sentiment_api import api as ns1

api = Api(
    title='YACSA',
    version='1.0',
    description='Yet Another Crypocurrency Sentiment API',
    # All API metadatas
)

api.add_namespace(ns1)