"""
Code which provides a MongoDB connection.
"""

from pymongo import MongoClient
from frontend import settings

# MongoDB defaults for test and locak usage
DEFAULT_MONGO_HOST = "localhost"
DEFAULT_MONGO_PORT = 27017


class MongoConnection(object):
    """
    Base class for connecting to MongoDB.
    """

    def __init__(self, db='chatlogs', host=DEFAULT_MONGO_HOST, port=DEFAULT_MONGO_PORT, tz_aware=True, username=None,
                 password=None,
                 **kwargs):
        """
        Create & open the connection - and authenticate.
        """
        self.client = MongoClient(
            host=host,
            port=port,
            tz_aware=tz_aware,
            w=0,
            **kwargs
        )
        self.db = self.client[db]

    def get_collection(self, collection):
        return self.db[collection]

    def get_db(self):
        return self.db
