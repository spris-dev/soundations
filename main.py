import os
import pandas as pd
from SpotifyCrawler import SpotifyCrawler
from dotenv import load_dotenv

load_dotenv()


def main():
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    spotify_crawler = SpotifyCrawler(client_id, client_secret)

    artists = []
    columns = [
        "name",
        "id",
        "popularity",
        "release_date",
        "danceability",
        "energy",
        "key",
        "loudness",
        "mode",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
        "type",
        "id",
        "uri",
        "track_href",
        "analysis_url",
        "duration_ms",
        "time_signature",
    ]

    dataset = pd.DataFrame(columns=columns)
    dataset.to_csv("dataset.csv", index=False)

    for year in range(1960, 2023):
        search_config = {"type": "artist", "year": str(year), "limit": "50"}
        next_artists = spotify_crawler.search_for_artists(search_config)

        if next_artists is not None:
            artists = artists + next_artists

        for artist in next_artists:
            track_features = []
            tracks = spotify_crawler.get_artist_tracks(artist)

            if tracks is not None:
                for track in tracks:
                    features = spotify_crawler.get_track_features(track)

                    if features is not None:
                        analys = spotify_crawler.get_track_features(track)
                        track_features.append([*track, *analys.values()])

                sub_dataset = pd.DataFrame(track_features)
                sub_dataset.to_csv("dataset.csv", index=False, mode="a", header=False)


if __name__ == "__main__":
    main()
