#AM2Slack v1.0.4
import requests
import time
import random
import subprocess
from dotenv import load_dotenv
import os

def get_current_track():
    cmd = """
        tell application "Music"
            set songTitle to name of current track
            set artistTitle to artist of current track
            set trackGenre to genre of current track
            set songAlbum to album of current track
            set state to player state
            return songTitle &"_.:"& artistTitle &"_.:"& trackGenre &"_.:"& songAlbum &"_.:"& state
        end tell
    """
    result = subprocess.run(['osascript', '-e', cmd], capture_output=True)
    return result.stdout
def make_get_request(url, headers=None):
    response = requests.get(url, headers=headers)
    return response
def make_post_request(url, headers=None, json=None):
    response = requests.post(url, headers=headers, json=json)
    return response

load_dotenv()

track = get_current_track().decode('utf-8')[0:len(get_current_track().decode('utf-8'))-1].split('_.:')
api_key = os.getenv("API_KEY")

try:
    emojis = os.getenv("EMOJIS").split(",")
    emoji = emojis[random.randint(0,len(emojis)-1)]
except AttributeError:
    emoji = ""

try:
    expiration = int(time.time()) + 60*int(os.getenv("STAUTS_EXPIRATION_MINUTES"))
except (AttributeError, TypeError):
    expiration = int(time.time()) + 300

try:
    white_list = os.getenv("SLACK_STATUS_WHITELIST").split(",")
except AttributeError:
    white_list = []

url_get = "https://slack.com/api/users.profile.get"
url_post = "https://slack.com/api/users.profile.set"
headers = {
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json; charset=utf-8"
}
if track != ['']:
    title = track[0]
    artist = track[1]
    genre = track[2]
    album = track[3]
    player_state = track[4]
    if album == "":
        new_status = title+" - "+artist
    else:
        new_status = title+" - "+artist+" ("+album+")"
else:
    new_status = ''
    player_state = ''
if len(new_status)>100:
    new_status = new_status[0:97]+'...'

data = {
    "profile": {
        "status_text": new_status,
        "status_expiration": expiration,
        "status_emoji": emoji
    }
}

no_data = {
    "profile": {
        "status_text": "",
        "status_expiration": 0,
        "status_emoji": ""
    }
}

get_status = make_get_request(url_get,headers)

if not get_status.json()["ok"]:
    print(f'Slack API error: {get_status.json()["error"]}')
else:
    status = get_status.json()["profile"]["status_text"].replace('&amp;',"&")

    if status not in white_list:
        if player_state != 'playing':
            make_post_request(url_post, headers=headers, json=no_data)
            print('No music playing, clearing status.')
        else:
            print('Music is playing.')
            print('Slack API user status:',status)
            if status != new_status:
                post_response = make_post_request(url_post, headers=headers, json=data)
                if post_response.json()["ok"] == True:
                    print('New song playing,',new_status)
                    print('Status updated successfully.')
                else:
                    print(f'Status update failed: {post_response.json()["error"]}')
            else:
                print('Still playing the same track, no action performed.')
    else:
        print('Custom user status, no action performed')