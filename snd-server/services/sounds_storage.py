import csv
import pandas as pd

from context import Context
from models.soundations import SoundationsTrackWithFeatures


class SoundsStorage:
    def __init__(self, ctx: Context) -> None:
        self.tracks_file = ctx.config.sounds_storage_path
        self.artists_file = ctx.config.artists_storage_path

    def write_headers(self) -> None:
        open(self.artists_file, "w").close()
        with open(self.tracks_file, "w") as f:
            w = csv.DictWriter(f, fieldnames=SoundationsTrackWithFeatures.__fields__)
            w.writeheader()

    def store_tracks(self, tracks) -> None:
        for track in tracks:
            with open(self.tracks_file, "a") as f:
                w = csv.DictWriter(
                    f, fieldnames=SoundationsTrackWithFeatures.__fields__
                )
                w.writerow(track.dict())

    def get_tracks(self) -> pd.DataFrame:
        dataset = pd.read_csv(self.tracks_file)
        return dataset

    def store_artist(self, artist_id: str) -> None:
        with open(self.artists_file, "a") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    artist_id,
                ]
            )

    def get_artists(self) -> set:
        artists_ids = set()
        with open(self.artists_file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                artists_ids.add(row[0])

        return artists_ids
