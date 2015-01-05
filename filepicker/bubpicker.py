import base64
import cStringIO
import logging
import re
import urllib
from django.conf import settings
import requests

LOGGER = logging.getLogger(__name__)

IS_IMAGE = re.compile(r".*.(jpg|png|gif)$")

class FilePicker(object):
    def __init__(self):
        self.KEY = settings.FILEPICKER_API_KEY
        self.API = "https://www.filepicker.io/api/store/S3"


    def getSize(self, url):
        payload = {
            'key': self.KEY,
            'width':'true',
            'height':'true',
        }
        url = url + "/metadata"
        r = requests.get(url, params=payload)
        d = r.json()
        return d['width'], d['height']


    def createFilePickerFromURL(self, url):
        if url and IS_IMAGE.match(url):
            LOGGER.info("Uploading file to filepicker %s" % url)
            filename = url.split('/')[-1]
            headers = {
                'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.45 Safari/537.36"
            }
            payload = {
                'key': self.KEY,
                'filename': filename,
                'url': url
            }
            # file = cStringIO.StringIO(urllib.urlopen(url).read())
            r = requests.get(url)
            files = {'file': base64.b64encode(r.content)}
            r = requests.post(self.API, params=payload, headers=headers, files=files)
            # get size
            d = r.json()
            width, height = self.getSize(d['url'])
            d['width'] = width
            d['height'] = height
            return d


    def createFilePickerFromFile(self, path):
        LOGGER.info("Uploading file to filepicker %s" % path)
        filename = path.split('/')[-1]
        payload = {
            'key': self.KEY,
            'filename': filename,
            'mimetype':'image/png'
        }
        with open(path, "r") as file:
            files = {'fileUpload': file.read()}
            r = requests.post(self.API, params=payload, files=files)
            # get size
            d = r.json()
            width, height = self.getSize(d['url'])
            d['width'] = width
            d['height'] = height
            return d

