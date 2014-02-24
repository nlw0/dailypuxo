from pymongo import MongoClient
from dateutil import parser
import oauth2 as oauth
import json

CONSUMER_KEY = 'wGmcUuiveRydaKiqrHjsUA'
CONSUMER_SECRET = 'XZBm2sQ5wIp67BE0eewA6S3yGYF4cpbQkEilPMBNwOI'
ACCESS_KEY = '13129082-cw9rV2cJD5CjMIA8nVvhGmxHPUgXazsDj7DdPKSxx'
ACCESS_SECRET = 'P7lombxv8bAcMvTsDOCMW61YxmwwO3QL61Y782Pvd0RnZ'


class TwitterHandler(object):

    def __init__(self):
        pass

    def oauth_req(self, url, key, secret, http_method="GET", body="",
                  http_headers=None):
        consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
        token = oauth.Token(key=key, secret=secret)
        client = oauth.Client(consumer, token)

        resp, content = client.request(
            url,
            method=http_method,
            body=body,
            headers=http_headers
        )
        return content

    def get_timeline(self, max_id=""):
        if max_id:
            uri = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=100&max_id={}'\
                .format(max_id)
        else:
            uri = 'https://api.twitter.com/1.1/statuses/user_timeline.json?count=100'

        timeline = self.oauth_req(uri, ACCESS_KEY, ACCESS_SECRET)
        return json.loads(timeline)[1:]

    def timeline_generator(self, max_id="", until=None):
        if until is not None:
            until_date = parser.parse(until)

        while True:
            for tw in self.get_timeline(max_id):
                max_id = tw['id']
                if until is not None and\
                   until_date > parser.parse(tw['created_at']).replace(tzinfo=None):
                    return
                yield tw['id'], tw['text'], tw['created_at']


def main():
    th = TwitterHandler()
    db = MongoClient()['mytweets']
    max_id_query = db['tweets'].aggregate(
        {"$group": {"_id": 1, "max_id": {"$min": "$twitter_id"}}}
    )
    if max_id_query['result']:
        max_id = max_id_query['result'][0]['max_id'] - 1
    else:
        max_id = ""

    for twid, text, at in th.timeline_generator(max_id=max_id, until="2013-01-01"):
        #if text.find("dailypuxo") >= 0:
        db['tweets'].insert({"twitter_id": twid, "text": text, "time": at})
