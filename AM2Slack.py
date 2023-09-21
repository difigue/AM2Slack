#AM2Slack v1.0.4
import requests
import time
import random
import subprocess

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

track = get_current_track().decode('utf-8')[0:len(get_current_track().decode('utf-8'))-1].split('_.:')

emojis = [":dancin-pug:",":aliendance:",":bananadance:",":catjam:",":pepejam:"]
expiration = int(time.time()) + 60*5
url_get = "https://slack.com/api/users.profile.get"
url_post = "https://slack.com/api/users.profile.set"
headers = {
        "Authorization": "Bearer xoxp-1277547768662-5441863361751-5793549125492-227a21c4ec1419cd7a4d46a9bb2101be", "Content-Type": "application/json; charset=utf-8"
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
        "status_emoji": emojis[random.randint(0,len(emojis)-1)]
    }
}
no_data = {
    "profile": {
        "status_text": "",
        "status_expiration": 0,
        "status_emoji": ""
    }
}

get_status = make_get_request(url_get,headers).json()["profile"]["status_text"].replace('&amp;',"&")
if get_status != 'Almorzando':
    if player_state != 'playing':
        make_post_request(url_post, headers=headers, json=no_data)
        print('No music playing, clearing status.')
    else:
        print('Music is playing.')
        print('Slack API user status:',get_status)
        if get_status != new_status:
            post_response = make_post_request(url_post, headers=headers, json=data)
            print('New song playing,',new_status)
            print('Updating status.')
        else:
            print('Still playing the same song, no action performed.')
else:
    print('Custom user status, no action performed')