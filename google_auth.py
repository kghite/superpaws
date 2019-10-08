"""
Set up google photos credentials
Create an Oauth2 client_secret.json in Google Cloud Console, then generate credentials.json with this script
Replace the ALBUM_KEY below to test with your own album, get the key from the test interface in the photos api docs
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Photo v1 API
SCOPES = 'https://www.googleapis.com/auth/photoslibrary.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('photoslibrary', 'v1', http=creds.authorize(Http()))

# Call the Photo v1 API
ALBUM_KEY = 'AKYbdu2O-wzXjma4pK1mp-XZ2YA2jRB683KeMCgCF6vZIIrm6VV30_NM4L5YEikVZGhYHVi3qTc5'
results = service.mediaItems().search(body={'albumId': ALBUM_KEY}).execute()
items = results.get('mediaItems', [])
if not items:
    print('No photos found.')
else:
    print('Photos:')
    for item in items:
        print('{0}'.format(item['baseUrl']))