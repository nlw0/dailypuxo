import sys
import json
import datetime
from dateutil.tz import gettz


def generate_data_line(line):
    aa = line['timestamp']
    bb = datetime.datetime.strptime(aa, "%Y-%m-%d %H:%M:%S")
    cc = bb.replace(tzinfo=gettz('UTC')).astimezone(gettz('America/Sao Paulo'))
    localtime = cc.strftime("%Y-%m-%d %H:%M:%S")
    line['local_timestamp'] = localtime
    return line


def main():

    the_data = {
        x['local_timestamp'][:10]: x
        for line in open(sys.argv[1])
        for x in [generate_data_line(json.loads(line))]
    }

    print json.dumps(the_data, indent=4)
