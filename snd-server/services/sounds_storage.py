import csv
from models.track import Track


class SoundsStorage:
    def __init__(self, file):
        self.file = file
        with open(self.file, "w") as f:
            w = csv.DictWriter(f, fieldnames=Track.__fields__)
            w.writeheader()

    def store_tracks(self, tracks):
        for track in tracks:
            with open(self.file, "a") as f:
                w = csv.DictWriter(f, fieldnames=Track.__fields__)
                w.writerow(track.dict())
