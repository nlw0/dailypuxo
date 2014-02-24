from pymongo import MongoClient

import urllib2
from bs4 import BeautifulSoup


def main():

    db = MongoClient()['mytweets']
    qq = db['tweets'].find(
        {"$and": [
            {"text": {"$regex": "#dailypuxo"}},
            {"text": {"$regex": "http:\/\/t.co\/.......... - "}}
        ]}
    )
    for x in qq:
        tco_url = x['text'][:22]
        soup = BeautifulSoup(urllib2.urlopen(tco_url))
        tag = soup.find('meta', attrs={"name": 'twitter:url'})
        tp_code = tag['value'][-6:]
        print tco_url, tp_code

        db['tweets'].update(
            {"_id": x["_id"]},
            {"$set": {'twitpic_code': tp_code}}
        )
