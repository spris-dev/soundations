import joblib
import zipfile
import pandas as pd

from typing import List
from sklearn.metrics.pairwise import cosine_similarity

from models.track import Track, Album, Artist, RecommendedTrack
from context import Context
from app import create_ctx


class Recommender:
    def __init__(self, ctx: Context) -> None:
        self.config = ctx.config
        self.zf = zipfile.ZipFile(self.config.archive_storage_path, mode="r")
        self.scaler = joblib.load(self.zf.open(self.config.scaler_storage_path))
        self.dataset = pd.read_csv(
            self.zf.open(self.config.transformed_sounds_storage_path), index_col=0
        )

    def __prepare_track(self, track: Track):
        prepared_track = pd.Series(track.dict())
        prepared_track = prepared_track.drop(labels=["id", "name", "album", "artists"])

        prepared_track = self.scaler.transform(prepared_track.values.reshape(1, -1))

        return prepared_track[0]

    def get_top_n(self, track: Track, n: int) -> List[RecommendedTrack]:
        prepared_track = self.__prepare_track(track)

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
    ctx = create_ctx()
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

    recommender = Recommender(ctx)
    print(recommender.get_top_n(track, 10))


if __name__ == "__main__":
    main()
