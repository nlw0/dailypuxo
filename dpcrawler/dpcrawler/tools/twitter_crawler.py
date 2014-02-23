import oauth2 as oauth
import json

CONSUMER_KEY = 'wGmcUuiveRydaKiqrHjsUA'
CONSUMER_SECRET = 'XZBm2sQ5wIp67BE0eewA6S3yGYF4cpbQkEilPMBNwOI'
ACCESS_KEY = '13129082-cw9rV2cJD5CjMIA8nVvhGmxHPUgXazsDj7DdPKSxx'
ACCESS_SECRET = 'P7lombxv8bAcMvTsDOCMW61YxmwwO3QL61Y782Pvd0RnZ'

def oauth_req(url, key, secret, http_method="GET", body="",
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

timeline = oauth_req(
    'https://api.twitter.com/1.1/statuses/user_timeline.json?max_id=435159404271255555',
    ACCESS_KEY,
    ACCESS_SECRET,
    body=""
)

# print timeline
data = json.loads(timeline)

for tw in data:
    print tw['id'], tw['text']
