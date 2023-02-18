from models.soundations import SoundationsTrack
from models.spotify import SpotifyApiTrack


def create_track_from_spotify(track: SpotifyApiTrack) -> SoundationsTrack:
    return SoundationsTrack(
        id=track.id,
        name=track.name,
        popularity=track.popularity,
        album=track.album,
        artists=track.artists,
        duration_ms=track.duration_ms,
        href=track.href,
        preview_url=track.preview_url,
    )
