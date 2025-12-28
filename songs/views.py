from datetime import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from songs.services.music_brainz.services import MusicBrainz
from songs.services.acoustic_brainz.services import AcousticBrainz

@api_view(["GET"])
@permission_classes([AllowAny])
def search(request):
    track_name = request.GET["track_name"]
    songs = MusicBrainz().fetch_songs_by_track_name(track_name)
    song_ids = [s["id"] for s in songs]
    keys_with_scale = AcousticBrainz().fetch_keys_with_scale(song_ids)
    songs_data = []
    for song in songs:
        # AcousticBrainz will silently ignore songs that don't meet requested features
        # Only return movies that have tonal data
        song_id = song["id"]
        key_with_scale = keys_with_scale.get(song_id)
        if not key_with_scale:
            continue

        artist_credit = song["artist-credit"]
        artists = [x["artist"]["name"] for x in artist_credit]
        tags = song.get("tags", [])
        genres = [tag["name"].capitalize() for tag in tags]
        first_release_date = song.get("first-release-date", None)
        formatted_date = None
        if first_release_date:
            formats = [
                "%Y-%m-%d",
                "%Y-%m",
                "%Y",
            ]
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(first_release_date, fmt)
                    break
                except ValueError:
                    continue
            formatted_date = date_obj.strftime("%b %d, %Y")
        data = {
            "id": song_id,
            "title": song["title"],
            "artists": artists,
            "genres": genres,
            "release_date": formatted_date,
            "score": song["score"],
            "length": song.get("length", None),
            "key_with_scale": key_with_scale
        }
        songs_data.append(data)
    return Response(
        {
            "message": "Songs retrieved.",
            "songs": songs_data,
        }
    )
