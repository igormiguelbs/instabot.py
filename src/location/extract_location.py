import json
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials


url = 'http://127.0.0.1:5000/photo'
path = 'unprocessed'
instagram_url = 'https://www.instagram.com/p/'


def add_location(shortcode, data):
    try:
        data = {
            'shortcode': shortcode,
            'location': data
        }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = json.dumps(data)
        r = requests.patch(url + '/' + shortcode, data=data, headers=headers)
    except:
        r = 0
    print(f"{shortcode} was updated! {r}")
    return r


def get_location(shortcode):
    insta_url = instagram_url + f'{shortcode}/?__a=1'
    insta_response = requests.get(insta_url, stream=False)
    insta_result = insta_response.json()
    id = insta_result['graphql']['shortcode_media']['location']['id']
    name = insta_result['graphql']['shortcode_media']['location']['name']
    return {'id': id, 'name': name}


def update_all_location():
    response = requests.get(url + '/' + path, stream=False)
    result = response.json()
    for small_big in result['result']:
        try:
            data = get_location(small_big['shortcode'])
            add_location(small_big['shortcode'], data)
        except:
            print(f"Warning: image: {small_big['shortcode']} can not updated.")


# Used by app.py
def get_locations_id(name):
    name = name.upper()
    scope = ['https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Locations and Hashtags').sheet1
    result = sheet.get_all_records()
    location_filtered = [l for l in result if name in l['runner']]
    format = list(map(lambda obj: {'location_id': f"l:{obj['id']}", 'name': obj['location']}, location_filtered))

    return format


#update_all_location()
