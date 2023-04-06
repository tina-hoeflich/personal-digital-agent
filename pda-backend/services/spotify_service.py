import spotipy
import os
import requests

def start_player(token):
    """Starts the music player with the given access token and resumes playback"""
    sp = spotipy.Spotify(auth=token)

    # Check if the user has an active device
    devices = sp.devices()
    if not devices['devices']:
        print("No active devices found.")
        return

    # Get the user's currently playing track
    track_info = sp.current_playback()
    if not track_info or 'is_playing' not in track_info:
        print("No track currently playing.")
        return

    # If the track is already playing, do nothing
    if track_info['is_playing']:
        print("Track already playing.")
        return

    # Resume playback
    sp.start_playback()
    print("Resuming playback.")
    # Call the resume_spotify function with the access token
 

        
def get_access_token():
    """Gets the access token for the Spotify API"""
    url = "https://accounts.spotify.com/api/token"

    payload='grant_type=refresh_token&refresh_token=AQBTfAcTnaNiH_PigcmXm7TFkGOGUjV9QKPD-xScvjYpbWpvROZRQZuTJ-VqXN7u5GrJ0Cc9Q3aSvQXFQffvMj0zTQwNQU8TMCpSIi9ww2606Ts3YnTjah_MkifbWxYLhZs'
    headers = {
    'Authorization': 'Basic ZGRhNGM4Nzc1ZjQ2NDZkMjgwNGU1ZWQ1YjRlZTVjYWY6MmNjYTk0NzEzN2E2NDRhNWFkZTI1ZmVjMGE4ZTkzZjQ=',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__Host-device_id=AQAq-DLjddfyGUTx3fFVtW_EkB07Ech06hnp1piSImqJsL1hVEecs4T8SM4WxdideVqW73oH2tLHVT_lLtj5XXWCSD4IIVL69fI; sp_tr=false'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    token = str(response.json()['access_token'])
    return token


def start_music():
    """Starts the music player"""
    start_player(get_access_token())