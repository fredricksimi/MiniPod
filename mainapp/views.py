from textwrap import indent
from django.shortcuts import render
import requests
from datetime import date
import hashlib
import os
import time
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('api_key')
api_secret = os.environ.get('api_secret')

epoch_time = int(time.time())
# our hash here is the api key + secret + time 
data_to_hash = api_key + api_secret + str(epoch_time)
# which is then sha-1'd
sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

# now we build our request headers
headers = {
    'X-Auth-Date': str(epoch_time),
    'X-Auth-Key': api_key,
    'Authorization': sha_1,
    'User-Agent': 'postcasting-index-python-cli'
}

# r = requests.get(url="https://api.podcastindex.org/api/1.0/search/byterm?q=call+her+daddy", headers=headers)

# entries = r.json()['feeds']
# for entry in entries:
#     print(entry)

def home_view(request):
    url_parameter = request.GET.get("q")
    if url_parameter:
        url = f"https://api.podcastindex.org/api/1.0/search/byterm?q={url_parameter}"
        response = requests.get(url=url, headers=headers)
        entries = response.json()['feeds']
    else:
        url = "https://api.podcastindex.org/api/1.0/podcasts/trending?pretty"
        response = requests.get(url=url, headers=headers)
        entries = response.json()['feeds']

    context = {'results':entries}
    return render(request, 'mainapp/index.html', context)

def podcast_details(request, id):
    the_id = str(id)
    url = f"https://api.podcastindex.org/api/1.0/podcasts/byfeedid?id={the_id}&pretty"
    response = requests.get(url=url, headers=headers)
    entries = response.json()['feed']
    context = {'results':entries}
    return render(request, 'mainapp/podcast-details.html', context)