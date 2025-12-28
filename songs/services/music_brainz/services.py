from urllib.parse import quote

import requests

from project.settings import USER_AGENT
from core.url.utils import build_url_with_query


class MusicBrainz():
    def __init__(self):
        self.api_url = "http://musicbrainz.org/ws/2"
        self.headers = {
            'Accept': 'application/json',
            "User-Agent": USER_AGENT,
        }

    def fetch_songs_by_track_name(self, track_name):
        try:
            query = {
                "query": track_name,
            }
            url = f"{self.api_url}/recording"
            url = build_url_with_query(url, query)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response_body = response.json()
            return response_body["recordings"]
        except requests.RequestException as error:
            print(f"Error while fetching songs from MusicBrainz: {error}")
