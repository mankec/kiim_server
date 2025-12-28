from urllib.parse import quote

import requests
from environs import Env

from core.url.utils import build_url_with_query

env = Env()

class Spotify():
  def __init__(self):
    self.api_url = "https://api.spotify.com/v1"
    self.headers = {
      "x-api-key": env.str("SPOONACULAR_API_KEY", default="")
    }

  def search_songs(self, track_name):
    songs = self._fetch_songs_by_track_name(track_name)
    song_ids = [song["id"] for song in songs]


  def _fetch_songs_by_track_name(self, track_name):
    limit = 10
    q = f"track:{track_name}"
    encoded = quote(q, safe='')
    double_encoded = quote(encoded, safe='')
    query = {
      "q": double_encoded,
      "limit": limit
    }
    url = f"{self.api_url}/search"
    url = build_url_with_query(url, query)
    response = requests.get(url, headers=self.headers)
    response_body = response.json()
    return response_body["tracks"]

  def _fetch_several_songs(self, song_ids):
    ...
