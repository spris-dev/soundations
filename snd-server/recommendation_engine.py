import joblib
import zipfile
import pandas as pd

from typing import List
from sklearn.metrics.pairwise import cosine_similarity

from models.soundations import SoundationsTrackWithFeatures, RecommendedTrack
from models.users import UserInDB
from context import Context
from spotify_crawler import get_tracks_by_genre


def create_track_with_features_dict(track: SoundationsTrackWithFeatures):
    track_dict = {
        "danceability": track.danceability,
        "energy": track.energy,
        "key": track.key,
        "loudness": track.loudness,
        "mode": track.mode,
        "speechiness": track.speechiness,
        "acousticness": track.acousticness,
        "instrumentalness": track.instrumentalness,
        "liveness": track.liveness,
        "valence": track.valence,
        "tempo": track.tempo,
        "duration_ms": track.duration_ms,
        "time_signature": track.time_signature,
        "popularity": track.popularity,
    }
    return track_dict


class Recommender:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx
        self.config = ctx.config
        self.zf = zipfile.ZipFile(self.config.archive_storage_path, mode="r")
        self.scaler = joblib.load(self.zf.open(self.config.scaler_storage_path))
        self.dataset = pd.read_csv(
            self.zf.open(self.config.transformed_sounds_storage_path), index_col=0
        )
        self.columns = list(self.dataset.columns)

    def __prepare_track(self, track: SoundationsTrackWithFeatures):
        prepared_track = pd.Series(track.dict())
        prepared_track = prepared_track.drop(labels=["id", "artists"])

        prepared_track = self.scaler.transform(prepared_track.values.reshape(1, -1))

        return prepared_track[0]

    def __recommend(
        self, dataset: pd.DataFrame, track: SoundationsTrackWithFeatures, n: int
    ) -> List[RecommendedTrack]:
        prepared_track = self.__prepare_track(track)

        similarity = cosine_similarity(dataset, prepared_track.reshape(1, -1))[:, 0]
        recommends = pd.DataFrame({"id": dataset.index, "similarity": similarity})
        recommends = recommends[recommends.id != track.id]
        recommends = recommends.sort_values("similarity", ascending=False).head(n)

        result = []
        for _, row in recommends.iterrows():
            result.append(RecommendedTrack(id=row["id"], similarity=row["similarity"]))

        return result

    def get_top_n(
        self, track: SoundationsTrackWithFeatures, n: int
    ) -> List[RecommendedTrack]:
        return self.__recommend(dataset=self.dataset, track=track, n=n)

    async def get_top_n_for_user(
        self, track_description_prompt: str, user: UserInDB, n: int
    ) -> List[RecommendedTrack] | None:
        user_history = await self.ctx.search_history.get_search_history(user=user)
        if not user_history:
            return None

        tracks = []
        tracks_df = pd.DataFrame(columns=self.columns)

        genres = await self.ctx.genres_classificator.predict(track_description_prompt)
        for genre, prob in genres.items():
            tracks.extend(await get_tracks_by_genre(self.ctx, genre))
            if prob < self.config.genres_classification_threshold:
                break

        for track in tracks:
            track_dict = create_track_with_features_dict(track)
            tracks_df.loc[track.id] = pd.Series(track_dict)

        tracks_df[:] = self.scaler.transform(tracks_df.values)

        user_recommends = []
        for user_track_id in user_history:
            user_track = await self.ctx.track_service.create_track_model_by_id(
                user_track_id
            )
            recommends = self.__recommend(tracks_df, user_track.value, n)
            user_recommends.extend(recommends)

        return sorted(
            user_recommends, key=lambda track: track.similarity, reverse=True
        )[:n]
