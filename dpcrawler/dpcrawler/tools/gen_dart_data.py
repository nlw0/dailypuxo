import sys
import json
import datetime
from dateutil.tz import gettz

from pymongo import MongoClient
db = MongoClient()['mytweets']


def generate_data_line(line):
    aa = line['timestamp']
    bb = datetime.datetime.strptime(aa, "%Y-%m-%d %H:%M:%S")
    cc = bb.replace(tzinfo=gettz('UTC')).astimezone(gettz('America/Sao Paulo'))
    localtime = cc.strftime("%Y-%m-%d %H:%M:%S")
    line['local_timestamp'] = localtime

    qq = db.tweets.find_one({"twitpic_code": line['short_id']})
    line['twitter_id'] = qq['twitter_id'] if qq is not None else None
    return line


def main():

    the_data = {
        x['local_timestamp'][:10]: x
        for line in open(sys.argv[1])
        for x in [generate_data_line(json.loads(line))]
        if x['local_timestamp'][:10] != '2013-02-15'
    }

    ## Find out next and previous day from each picture
    dias = sorted(the_data.keys())
    pre = dias[-1:] + dias[:-1]
    nex = dias[1:] + dias[:1]
    for p, x, n in zip(pre, dias, nex):
        the_data[x]['previous_day'] = p
        the_data[x]['next_day'] = n

    print json.dumps(the_data, indent=4)
