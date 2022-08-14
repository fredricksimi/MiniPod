from unittest import result
from django.test import TestCase
import requests
from dotenv import load_dotenv
import hashlib
import time
import os
load_dotenv()


api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')

epoch_time = int(time.time())
# our hash here is the api key + secret + time 
data_to_hash = api_key + api_secret + str(epoch_time)
sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()
headers = {
    'X-Auth-Date': str(epoch_time),
    'X-Auth-Key': api_key,
    'Authorization': sha_1,
    'User-Agent': 'postcasting-index-python-cli'
}


class YourTestClass(TestCase):
    def test_home_view(self):
        print("Method: test_parameter_search.")
        url="https://api.podcastindex.org/api/1.0/search/byterm?q=Podcrushed"
        response = requests.get(url=url, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_podcast_details(self):
        print("Method: test_podcast_details.")
        url="https://api.podcastindex.org/api/1.0/podcasts/byfeedid?id=5440392&pretty"
        response = requests.get(url=url, headers=headers)
        result = response.json()['feed']['title']
        self.assertEqual(result, 'Podcrushed')
