import spotipy
import json
import csv


# To print and save a json format of response recieved from the website
def formatted_output(obj):
    output = json.dumps(obj, sort_keys=False, indent=4)
    with open("spotify\output.json", "w") as f :
        f.write(output)
    print(output)

client_id = "Spotify_Client_Id"
client_secret = "Spotify_Client_Secret"
redirect_uri = "https://www.google.com/"

scope = "playlist-read-private"     

oauth_object = spotipy.SpotifyOAuth(client_id=client_id,
                                    client_secret=client_secret,
                                    redirect_uri=redirect_uri,
                                    scope=scope)
token_dict = oauth_object.get_cached_token()
token = token_dict["access_token"]

# Object on which all the functions will work and requests are made
spotify_object = spotipy.Spotify(auth=token, requests_timeout=10, retries= 10)

def getting_playlists(spotify_object):
    playlists = spotify_object.current_user_playlists()         # Method to access all the playlists user have in their library
    with open(".\playlists_info.csv", 'w', encoding='utf-8', newline="") as playlist_file:
        writer = csv.writer(playlist_file)
        fields = ["Id", "Name", "Songs"]
        writer.writerow(fields)
        for playlist in playlists['items']:
            playlist_id = (playlist['uri']).split(':')[-1]      # Id of the playlist assigned by spotify, to access its song later
            playlist_name = playlist['name']
            playlist_total_songs = playlist['tracks']['total']
            row = [playlist_id, playlist_name, playlist_total_songs]
            writer.writerow(row)
            
def getting_tracks(spotify_object, playlist_id):
    tracks = spotify_object.playlist_tracks(playlist_id=playlist_id)        # Method to get all the tracks of the specified playlist
    # formatted_output(tracks['items'])
    track_names = []
    try:
        # print(playlist_name)
        for track in tracks['items']:
            track_names.append(track['track']['name'])
        while tracks['next']:                                   # The results from the api come in the batch of 100 results at a time so to check if their are more tracks then it.
            tracks = spotify_object.next(tracks)                # Accesssing the next batch of tracks
            for track in tracks['items']:
                track_names.append(track['track']['name'])
    except Exception as e:
        print(e)
    print(len(track_names))
    return track_names

if __name__ == "__main__":
    # getting_playlists(spotify_object)
    with open("spotify/playlists_info.csv", "r", encoding='utf-8') as playlist:
        rdr = csv.reader(playlist)
        next(rdr)
        for playlist_info in rdr:
            tracks = getting_tracks(spotify_object, playlist_info[0])
            with open(f"spotify\songs\{playlist_info[1]}.txt", 'w',encoding='utf-8') as playlist:
                for track in tracks:
                    playlist.write(track+"\n")