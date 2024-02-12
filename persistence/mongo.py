from pymongo import MongoClient

class Mongo:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['housing_scrapper']
        self.collection = self.db['properties']

    def insert(self, data):
        return self.collection.insert_one(data)

    def find_one(self, query):
        return self.collection.find_one(query)

    def update(self, query, data):
        return self.collection.update_one(query, data)

    def delete(self, query):
        self.collection.delete_one(query)

    def close(self):
        self.client.close()