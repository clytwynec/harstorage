import pymongo

from pylons import config, tmpl_context as c


class MongoDB():

    """
    Interface for MongoDB database
    """

    def __init__(self, collection="results"):
        """Initilize connection and check indeces"""

        try:
            # MongoDB URI
            uri = config["app_conf"].get("mongo_uri")

            # Database
            database = uri.split('/')[-1]

            # Collection
            # Updated the mongo client connection for the collection
            # We could also use MongoReplicaSetClient for dealing with
            # replica sets.
            replicate = config["app_conf"]["mongo_replicate"]

            if replicate == "true":
                self.collection = pymongo.MongoReplicaSetClient(
                    hosts_or_uri=uri,
                    replicaSet=(config["app_conf"]["mongo_replset"])
                )[database][collection]
            else:
                self.collection = pymongo.mongo_client.MongoClient(
                    host=uri,
                )[database][collection]

            # Indecies
            self.ensure_index()
        except Exception as error:
            # Exception type: Exception message
            c.message = ": ".join([type(error).__name__, error.message])

    def ensure_index(self):
        self.collection.ensure_index([("label", 1), ("timestamp", -1)])
        self.collection.ensure_index([("label", 1), ("timestamp", 1)])
        self.collection.ensure_index([("url", 1), ("timestamp", -1)])
        self.collection.ensure_index([("url", 1), ("timestamp", 1)])
