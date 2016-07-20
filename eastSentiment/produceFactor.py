import datetime
from pymongo import  *
from snownlp import  SnowNLP
import pymongo

# connecting database 601001eastmoney
def getSentimentFactor(stockcode,date):
    client = MongoClient()

    # now_time = datetime.datetime.now()
    # yes_time = now_time + datetime.timedelta(days=-1)
    # grab_time = yes_time.strftime('%m-%d')

    db = client[stockcode+'eastmoney']

    # sort the collection GuYouHui and point to it
    coll = db[date+'GuYouHui']

    documents = coll.find().sort([
        ("created_at", pymongo.DESCENDING)
    ])

    for document in documents:

        create_date = document['create'][:10]
        last = document['last'][:5]

        if (document['text'] != ''):
            s = SnowNLP(document['text'])
            sentiment = s.sentiments
            sentiment_factor = (sentiment) * int(document['read'])
        else:
            sentiment,sentiment_factor = 0,0
        document['sentiment'] = sentiment
        document['sentiment_factor'] = sentiment_factor



        # # print sentiment_factor
        # coll2 = db[date+'SentimentFactor']
        #
        # result = coll2.insert_one(
        #     {
        #         "create_date": create_date,
        #         "sentiment_factor": sentiment_factor,
        #         "last_date": last
        #     })
        # print result.inserted_id
