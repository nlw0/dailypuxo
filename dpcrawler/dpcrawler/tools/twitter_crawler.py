import oauth2 as oauth
import json

CONSUMER_KEY = 'qrXCcf1ScgbJrXJeUn1xYg'
CONSUMER_SECRET = 'odpHntZmyaoI5VkGlAcYpn8fN6PuxDIAUETlrtxG4'
ACCESS_KEY = '13129082-cw9rV2cJD5CjMIA8nVvhGmxHPUgXazsDj7DdPKSxx'
ACCESS_SECRET = 'P7lombxv8bAcMvTsDOCMW61YxmwwO3QL61Y782Pvd0RnZ'

def oauth_req(url, key, secret, http_method="GET", post_body=None,
              http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)

    resp, content = client.request(
        url,
        method=http_method,
        body=post_body,
        headers=http_headers
    )
    return content


home_timeline = oauth_req(
    'https://api.twitter.com/1.1/statuses/home_timeline.json',
    ACCESS_KEY,
    ACCESS_SECRET
)

for tw in json.loads(home_timeline):
    print tw
