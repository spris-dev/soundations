import joblib
import zipfile
import pandas as pd

from typing import List
from sklearn.metrics.pairwise import cosine_similarity

from models.soundations import SoundationsTrackWithFeatures, RecommendedTrack
from context import Context


class Recommender:
    def __init__(self, ctx: Context) -> None:
        self.config = ctx.config
        self.zf = zipfile.ZipFile(self.config.archive_storage_path, mode="r")
        self.scaler = joblib.load(self.zf.open(self.config.scaler_storage_path))
        self.dataset = pd.read_csv(
            self.zf.open(self.config.transformed_sounds_storage_path), index_col=0
        )

    def __prepare_track(self, track: SoundationsTrackWithFeatures):
        prepared_track = pd.Series(track.dict())
        prepared_track = prepared_track.drop(labels=["id", "artists"])

        prepared_track = self.scaler.transform(prepared_track.values.reshape(1, -1))

        return prepared_track[0]

    def get_top_n(
        self, track: SoundationsTrackWithFeatures, n: int
    ) -> List[RecommendedTrack]:
        prepared_track = self.__prepare_track(track)

        similarity = cosine_similarity(self.dataset, prepared_track.reshape(1, -1))[
            :, 0
        ]
        recommends = pd.DataFrame({"id": self.dataset.index, "similarity": similarity})
        recommends = recommends[recommends.id != track.id]
        recommends = recommends.sort_values("similarity", ascending=False).head(n)

        result = []
        for _, row in recommends.iterrows():
            result.append(RecommendedTrack(id=row["id"], similarity=row["similarity"]))

        return result
