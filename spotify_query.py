import os
import requests
import json
from github import Github
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    id= os.environ.get("SPOTIFY_ID")
    secret = os.environ.get("SPOTIFY_SECRET")
    body = {
        "grant_type":"client_credentials",
        "client_id":id,
        "client_secret":secret
    }
    try:
        response = requests.post(url, headers=headers, data=body)
        print("Token Response: ",response.status_code)
        if response.status_code == 200:
            decoded_response = response.content.decode('utf-8')
            return json.loads(decoded_response)["access_token"]
    except Exception as e:
        pass

def get_tracks(token):
    url = "https://api.spotify.com/v1/playlists/77HCRyNiBLmGMdAcLnT5Tb/tracks"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers)
        print("Tracks Response: ", response.status_code)
        if response.status_code == 200:
            unsorted_tracks = json.loads(response.content.decode('utf-8'))["items"]
            sorted_tracks = []
            for track in unsorted_tracks:
                track_name = track["track"]["name"]
                track_artists = ' & '.join([artist["name"] for artist in track["track"]["artists"]])
                track_link = track["track"]["external_urls"]["spotify"]
                
                # Format the track as a markdown table row
                sorted_tracks.append(f"| **{track_name}** | {track_artists} | [Listen Here]({track_link}) |")
            
            # Return the last 5 tracks formatted as a markdown table
            return sorted_tracks[-5:]
    except Exception as e:
        print(f"Exception {e}")


def update_readme(tracks):
    g = Github(os.environ.get("GITHUB_TOKEN"))
    repo = g.get_repo('moses946/moses946')
    readme = repo.get_readme()
    content = readme.decoded_content.decode()
    # Update README
    start_marker = "<!-- start spotify -->"
    end_marker = "<!-- end spotify -->"
    new_content = "\n \n".join(tracks)
    print(new_content)
    updated_content = content.split(start_marker)[0] + start_marker + "\n" + new_content + "\n" + end_marker + content.split(end_marker)[1]
    commit_message = f"Spotify playlist as at {datetime.date(datetime.now())}"
    repo.update_file(readme.path, commit_message, updated_content, readme.sha)
    

if __name__ == "__main__":
    token = get_token()
    tracks = get_tracks(token=token)
    update_readme(tracks=tracks)
