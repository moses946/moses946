import os
import requests
import json
from github import Github

def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = {
        "grant_type":"client_credentials",
        "client_id":os.getenv("SPOTIFY_ID"),
        "client_secret":os.getenv("SPOTIFY_SECRET")
    }
    try:
        response = requests.post(url, headers=headers, data=body)
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
        if response.status_code == 200:
            unsorted_tracks = json.loads(response.content.decode('utf-8'))["items"]
            sorted_tracks = []
            # {
            #         "name": track["track"]["name"],
            #         "link": track["track"]["external_urls"]["spotify"],
            #         "Artist": track["track"]["artists"][0]["name"]
            #     }
            for track in unsorted_tracks:
                sorted_tracks.append(f"- **{track["track"]["name"]} by {' & '.join([artist["name"] for artist in track["track"]["artists"]])}")
            return sorted_tracks[-5: ]
    except Exception as e:
        print(f"Exception {e}")

def update_readme(tracks):
    g = Github(os.getenv("GITHUB_TOKEN"))
    repo = g.get_repo('moses946')
    readme = repo.get_readme()
    content = readme.decoded_content.decode()
    print(content)

if __name__ == "__main__":
    token = get_token()
    print("\n\n")
    print(get_tracks(token=token))
