import pymongo

mongo = pymongo.MongoClient('localhost:27017')


def get_references(db):
    database = mongo[db]
    refs = database['references'].find()
    return(refs)


def get_references(db,maxpriority):
    database = mongo[db]
    refs = database['references'].find({'priority':{'$lt':maxpriority}})
    return(refs)
