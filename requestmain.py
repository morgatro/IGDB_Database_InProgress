import config
import requests

client_id = config.client_id
client_secret = config.client_secret
base_url = 'https://api.igdb.com/v4/'

body = {
    'client_id': client_id,
    'client_secret': client_secret,
    "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token?', body)

keys = r.json();

# print(keys)

headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer ' + keys['access_token']
}