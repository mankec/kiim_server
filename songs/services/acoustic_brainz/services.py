from urllib.parse import quote

import requests

from project.settings import USER_AGENT
from core.url.utils import build_url_with_query


class AcousticBrainz():
    # Constants (https://acousticbrainz.readthedocs.io/api.html#constants)
    LOW_LEVEL_INDIVIDUAL_FEATURES = {
        "key": "tonal.key_key",
        "scale": "tonal.key_scale",
    }
    # TEST_SONG_IDS = [
    #     '9d4d455a-7bc6-44ef-82fa-f1091baf2c1a', '8b38312f-24b2-4c4f-bf06-c3c5dac26ee1', 'b9f53bed-1e32-4d1d-9f69-18ab84b74cec', '7b0c65cd-8bde-40e3-ab95-e3a4f0333f7f', 'e241cf7a-f2b1-4c87-b3ea-ad5dfe4b5e65', '6b88634c-804c-4366-b573-c13bd026cc10', 'e40e9663-6761-4787-99d8-e541aa36b221', 'b6411d6b-2dca-4004-8919-e8c27ff6b286', 'c2aed45f-02c4-4c2f-9aa6-43ef37b5440c', '835d20ad-df96-42fa-8ec4-d4f73e1fe015', 'bb92acf6-fb7a-48c8-a5bf-6d22962f761b', '4033d60f-7f2a-4863-a83d-bd7df81c4f98', '4e600523-4a37-41cd-8599-5fe7311968e5', 'a9f0d7a8-186d-4038-89bb-69248fc372c5', '280b5006-0e74-4584-8fa3-ac82494d1778', 'bca4b055-ef21-4aa0-aafb-1f5611044c08', '3d0e806c-304a-43cb-b073-3d166dda23e7', '3c4c9269-0b7b-4336-bb16-88051d16bf92', '9dbbac37-91ce-4a50-b56c-ff6c5c788f08', 'c70f808d-78b6-4e61-993c-dac7698d6bbc', '4ee82b14-fb23-42b2-9048-1073dee82360', '02d70574-8ea6-42bc-8094-42621e7ab8a8', '408822d2-1442-4d03-8f7f-b12c16697c9d', 'dd655bd2-f75b-4bb7-8443-4b1b715a6dc5', '9226a606-670b-4b8d-addd-ccba7e0be593'
    # ]

    def __init__(self):
        self.api_url = "https://acousticbrainz.org"
        self.headers = {
            'Content-Type': 'application/json',
            "User-Agent": USER_AGENT,
        }

    def fetch_keys_with_scale(self, song_ids):
        try:
            llif = self.__class__.LOW_LEVEL_INDIVIDUAL_FEATURES
            recording_ids = ";".join(song_ids)
            features =f"{llif["key"]};{llif["scale"]}"
            query = {
                "recording_ids": recording_ids,
                "features": features,
            }
            url = f"{self.api_url}/api/v1/low-level"
            url = build_url_with_query(url, query)
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            response_body = response.json()
            data = [{k: v} for k, v in response_body.items() if k != "mbid_mapping"]
            keys_with_scale = {}
            for d in data:
                for song_id, v in d.items():
                    tonal = v["0"]["tonal"]
                    keys_with_scale[song_id] = f"{tonal["key_key"]} {tonal["key_scale"]}"
            return keys_with_scale
        except requests.RequestException as error:
            print(f"Error while fetching keys with scale from AcousticBrainz: {error}")
