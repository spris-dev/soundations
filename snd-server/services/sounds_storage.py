import csv

from models.track import Track


class SoundsStorage:
    def __init__(self, tracks_file, artists_file):
        self.tracks_file = tracks_file
        self.artists_file = artists_file

    def write_headers(self):
        open(self.artists_file, "w").close()
        with open(self.tracks_file, "w") as f:
            w = csv.DictWriter(f, fieldnames=Track.__fields__)
            w.writeheader()

    def store_tracks(self, tracks):
        for track in tracks:
            with open(self.tracks_file, "a") as f:
                w = csv.DictWriter(f, fieldnames=Track.__fields__)
                w.writerow(track.dict())

    def store_artist(self, artist_id: str):
        with open(self.artists_file, "a") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    artist_id,
                ]
            )

    def get_stored_artists(self):
        artists_ids = set()
        with open(self.artists_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                artists_ids.add(row[0])

        return artists_ids
