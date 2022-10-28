import pandas as pd


class SoundsStorage:
    def __init__(self, file):
        self.file = file

    def store_tracks(self, track_features):
        track_features.rename(columns={"song": "song_name", "key": "song_key"})
        track_features.to_csv(self.file, index=False, mode="a", header=False)
