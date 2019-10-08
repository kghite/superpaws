"""
Slackbot serving cute animal pics
"""

import requests
import random
import yaml
from flask import Flask, abort, jsonify, request
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file
import urllib.request

app = Flask(__name__)

# Configuration and app setup
with open("config.yaml", 'r') as f:
    config = yaml.load(f)
slack_tokens = config['slack_tokens']
google_albums = config['album_ids']
api_map = {'cat': ('http://aws.random.cat/meow', 'file'),  # Cats
            'fox': ('https://randomfox.ca/floof/', 'image')}  # Foxes
help_message = '*superpaws commands:* \n \n' \
               '*cat* -> random cute cat pic \n ' \
               '*legatte* -> gatto Italiano \n ' \
               '*fox* -> foxes are basically cats \n ' \
               '*milo* -> random pic of the cutest cat \n ' \
               '*kitten* -> big cats \n ' \
               '*pillopet* -> Pillo submitted pet pics (Add to this folder: https://photos.app.goo.gl/eysJiartZbnnYPxr7)'


"""
Serve index status page to confirm the app is running
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    return "The Superpaws Slackbot is alive."


"""
Serve specified image type or help instructions when slash command is used in Slack
"""


@app.route('/superpaws', methods=['GET', 'POST'])
def receive_message():
    # Authenticate the Slack request
    if not is_request_valid(request):
        abort(400)

    # Respond based on command type
    arg = request.form.get('text', None)
    if arg == 'help':
        msg_text = help_message
    elif arg in api_map.keys():
        msg_text = get_api_image(arg)
    elif arg in google_albums.keys():
        msg_text = get_google_image(arg)
    else:
        msg_text = get_api_image('cat')

    return jsonify(response_type='in_channel', text=msg_text)


"""
Return a link to an image from the specified google photos album
"""


def get_google_image(key):
    # Authenticate Google photos access
    store = file.Storage('credentials.json')
    creds = store.get()
    service = build('photoslibrary', 'v1', http=creds.authorize(Http()))

    # Get the photo
    albumId = google_albums[key]
    results = service.mediaItems().search(body={'albumId': albumId}).execute()
    photo_urls = [photo['baseUrl'] for photo in results.get('mediaItems', [])]
    image_url = random.choice(photo_urls)
    short_link = shorten_link(image_url)

    # Clean up
    del(service)

    return short_link


"""
Return a link to an image from the specified api
"""


def get_api_image(key):
    response = requests.get(api_map[key][0]).json()
    image_url = response[api_map[key][1]]
    short_link = shorten_link(image_url)

    return short_link


"""
Generate shortened versions of photo urls
"""
def shorten_link(image_url):
    apiurl = "http://tinyurl.com/api-create.php?url="
    tinyurl = urllib.request.urlopen(apiurl + image_url).read()
    short_url = tinyurl.decode("utf-8")

    return short_url


"""
Authenticate Slack requests
"""


def is_request_valid(request):
    is_token_valid = request.form['token'] in slack_tokens.keys()
    if is_token_valid:
        is_team_id_valid = request.form['team_id'] == slack_tokens[request.form['token']]

    return is_token_valid and is_team_id_valid


if __name__ == '__main__':
    app.run(debug=True)
