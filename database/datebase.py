import pymongo


class database:
    def __init__(self):
        try:
            mongo = pymongo.MongoClient(host='test_mongodb', port=27017, username='root', password='pass')
            mongo.server_info() # trigger exception if not connected to db
            self.db = mongo.Movie
        except:
            print("ERROR - Cannot connect to db")
