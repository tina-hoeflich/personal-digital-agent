import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# authenticate with Spotify API
client_id = "dda4c8775f4646d2804e5ed5b4ee5caf"
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# search for a song
song_name = "Despacito"
results = sp.search(q=song_name, type='track')
if len(results['tracks']['items']) > 0:
    # get the first song
    print(results['tracks']['items'][0]['name'])
    song_uri = results['tracks']['items'][0]['uri']
else:
    print(f"No results found for '{song_name}'")