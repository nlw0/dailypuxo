'''This crawler queries twitpic for every image containing a certain
tag, then picks the code from each image for multiple pages. For each
of these images it loads its data and dumps it to stdout, and the
image itself is saved into an 'images' directory.

'''

from bs4 import BeautifulSoup
import json
import os.path
import re
from retrying import retry
import urllib2

TAG_URL = 'http://twitpic.com/tag/{tag:}?page={page:}'
API_URL = 'http://api.twitpic.com/2/media/show.json?id={code:}'
IMG_URL = 'http://twitpic.com/show/full/{code:}'


def main():
    data_file = open('dailypuxo.dat', 'a')

    codes = get_codes_from_tag('dailypuxo', 8)

    for c in codes:
        image_filename = 'images/' + c + '.jpeg'
        if os.path.exists(image_filename):
            continue

        tp_data = fetch_twitpic_data(c)
        data_file.write(json.dumps(tp_data) + '\n')
        data_file.flush()

        with open(image_filename, 'w') as fp:
            fp.write(fetch_twitpic_image(c))

    data_file.close()


def get_codes_from_tag(tag, pages):
    for p in range(1, 1 + pages):
        for img in get_page(tag, p).find_all('div', 'user-photo-wrap'):
            link = img.find('a')['href']
            assert link[0] == '/'
            code = link[1:]
            test_code(code)
            yield code


def test_code(code):
    assert len(code) == 6 and re.match(r'[a-z0-9]{6}', code) is not None


def get_page(tag, page):
    myurl = TAG_URL.format(**{'tag': tag, 'page': page})
    response = urllib2.urlopen(myurl)
    html_doc = response.read()
    return BeautifulSoup(html_doc)


@retry
def fetch_twitpic_data(code):
    myurl = API_URL.format(code=code)
    response = urllib2.urlopen(myurl)
    html_doc = response.read()
    return json.loads(html_doc)


@retry
def fetch_twitpic_image(code):
    myurl = IMG_URL.format(code=code)
    response = urllib2.urlopen(myurl)
    html_doc = response.read()
    return html_doc
