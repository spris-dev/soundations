import joblib
import pandas as pd

from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

from models.track import Track, Album, Artist, RecommendedTrack
from services.config import Config
from services.sounds_storage import SoundsStorage


class Recommender:
    def __init__(self) -> None:
        self.config = Config()
        self.storage = SoundsStorage()
        self.dataset = pd.DataFrame()

    def scale(self) -> None:
        scaler = MinMaxScaler()
        self.dataset[:] = scaler.fit_transform(self.dataset.values)
        joblib.dump(scaler, "sc.joblib")

    def prepare_dataset(self) -> None:
        self.dataset = self.storage.get_tracks()
        self.dataset = self.dataset.drop(["name", "album", "artists"], axis=1)
        self.dataset.set_index("id", inplace=True)
        self.scale()

    def prepare_track(self, track: Track):
        prepared_track = pd.Series(track.dict())
        prepared_track = prepared_track.drop(labels=["id", "name", "album", "artists"])

        scaler = joblib.load("sc.joblib")
        prepared_track = scaler.transform(prepared_track.values.reshape(1, -1))

        return prepared_track[0]

    def add_track_to_dataset(self, track: Track):
        if track.id not in self.dataset.index:
            prepared_track = self.prepare_track(track)
            self.dataset.loc[track.id] = prepared_track

    def get_top_n(self, track: Track, n: int) -> List[RecommendedTrack]:
        self.add_track_to_dataset(track)
        prepared_track = self.prepare_track(track)

        similarity = cosine_similarity(self.dataset, prepared_track.reshape(1, -1))[
            :, 0
        ]
        recommends = pd.DataFrame({"id": self.dataset.index, "similarity": similarity})
        recommends = recommends[recommends.id != track.id]
        recommends = recommends.sort_values("similarity", ascending=False).head(n)

        # TO DO: get rid of iterating over DataFrame rows(considered to be an anti-pattern)
        result = []
        for _, row in recommends.iterrows():
            result.append(RecommendedTrack(id=row["id"], similarity=row["similarity"]))

        return result


def main():
    album = Album(
        id="652N05EcNH1a4bIlUixQE2",
        name="Enema Of The State",
        release_date="1999-06-01",
        images=[
            {
                "height": 640,
                "url": "https://i.scdn.co/image/ab67616d0000b2736da502e35a7a3e48de2b0f74",
                "width": 640,
            },
            {
                "height": 300,
                "url": "https://i.scdn.co/image/ab67616d00001e026da502e35a7a3e48de2b0f74",
                "width": 300,
            },
            {
                "height": 64,
                "url": "https://i.scdn.co/image/ab67616d000048516da502e35a7a3e48de2b0f74",
                "width": 64,
            },
        ],
    )
    artist = Artist(id="6FBDaR13swtiWwGhX1WQsP", name="blink-182")
    track = Track(
        danceability=0.434,
        energy=0.897,
        key=0,
        loudness=-4.918,
        mode=1,
        speechiness=0.0488,
        acousticness=0.0103,
        instrumentalness=0,
        liveness=0.612,
        valence=0.684,
        tempo=148.726,
        duration_ms=167067,
        time_signature=4,
        id="2m1hi0nfMR9vdGC8UcrnwU",
        name="All The Small Things",
        popularity=81,
        album=album,
        artists=[artist],
    )

    recommender = Recommender()
    recommender.prepare_dataset()
    print(recommender.get_top_n(track, 10))


if __name__ == "__main__":
    main()
