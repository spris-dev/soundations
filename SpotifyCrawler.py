import requests
import sys
import time
import pandas as pd
from operator import itemgetter
import os
from dotenv import load_dotenv

audio_features = [
    "name",
    "id",
    "popularity",
    "release_date",
    "acousticness",
    "danceability",
    "duration_ms",
    "energy",
    "instrumentalness",
    "key",
    "liveness",
    "loudness",
    "mode",
    "speechiness",
    "tempo",
    "time_signature",
    "valence",
]


class SpotifyCrawler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = "https://accounts.spotify.com/api/token"
        self.token = self.get_access_token()

    def get_access_token(self):
        response = requests.post(
            self.token_url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret),
        )

        print("[Response] status_code: " + str(response.status_code), file=sys.stdout)
        print("Access Token Headers: " + str(response.headers), file=sys.stdout)

        return response.json()["access_token"]

    def request(self, url):
        auth = "Bearer " + self.token
        headers = {"Authorization": auth}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(
                "[Response] status_code: " + str(response.status_code), file=sys.stdout
            )
            print("Response headers: " + str(response.headers), file=sys.stdout)

        if response.status_code == 401:
            self.token = self.get_access_token()
            print("Token refreshed")
            return None

        if response.status_code == 404:
            print("404")
            return None

        if response.status_code == 429:
            sec_to_sleep = response.headers.get("retry-after")
            print("Retry-after: " + str(sec_to_sleep))
            time.sleep(sec_to_sleep)
            self.request(url)

        if response.status_code == 503:
            self.request(url)

        return response.json()

    def search_for_artists(self, search_config):
        type = search_config["type"]
        year = search_config["year"]
        limit = search_config["limit"]

        url = (
            "https://api.spotify.com/v1/search?q=year%3A"
            + year
            + "&type="
            + type
            + "&limit="
            + limit
            + "&offset="
        )

        artist_names = []
        for i in range(0, 1000, int(limit)):
            curr_url = url + str(i)
            tracks = self.request(curr_url)

            if tracks is not None:
                for i, t in enumerate(tracks["artists"]["items"]):
                    artist_names.append((t["name"], t["id"]))

        return artist_names

    def search_for_genre(self, search_config):
        genre = search_config["genre"]
        limit = search_config["limit"]

        url = (
            "https://api.spotify.com/v1/search?q=genre%3A"
            + genre
            + "&type="
            + "track"
            + "&limit="
            + limit
            + "&offset="
        )

        songs = []
        for i in range(0, 1000, int(limit)):
            curr_url = url + str(i)
            tracks = self.request(curr_url)

            if tracks is not None:
                for i, t in enumerate(tracks["tracks"]["items"]):
                    songs.append(
                        (
                            t["name"],
                            t["id"],
                            t["popularity"],
                            t["album"]["release_date"],
                        )
                    )

        print(songs)

        return songs

    def get_artist_tracks(self, artist_name):
        url = (
            "https://api.spotify.com/v1/artists/"
            + str(artist_name[1])
            + "/top-tracks?market=ES"
        )

        response = self.request(url)
        if response is not None:
            tracks = []
            for i, t in enumerate(response["tracks"]):
                tracks.append(
                    [t["name"], t["id"], t["popularity"], t["album"]["release_date"]]
                )

            return tracks

    def get_track_features(self, track_name):
        url = "https://api.spotify.com/v1/audio-features/" + str(track_name[1])

        response = self.request(url)
        if response is not None:
            return response

    def get_genres_list(self):
        url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"

        response = self.request(url)
        if response is not None:
            return response

    def create_dataset(self, columns, file):
        dataset = pd.DataFrame(columns=columns)
        dataset.to_csv(file, index=False)

        return dataset

    def dataset_by_year(self, from_year, to_year, file):
        artists = []
        for year in range(from_year, to_year):
            search_config = {"type": "artist", "year": str(year), "limit": "50"}
            next_artists = self.search_for_artists(search_config)

            if next_artists is not None:
                artists = artists + next_artists

            for artist in next_artists:
                track_features = []
                tracks = self.get_artist_tracks(artist)

                if tracks is not None:
                    for track in tracks:
                        features = self.get_track_features(track)

                        if features is not None:
                            analys = self.get_track_features(track)
                            track_features.append(
                                [*track, *itemgetter(*audio_features[4:])(analys)]
                            )

                    sub_dataset = pd.DataFrame(track_features)
                    sub_dataset.to_csv(file, index=False, mode="a", header=False)

    def dataset_by_genres(self, genres, file):
        for genre in genres:
            search_config = {"genre": genre, "limit": str(50)}
            tracks = self.search_for_genre(search_config)

            if tracks is not None:
                track_features = []
                for track in tracks:
                    features = self.get_track_features(track)

                    if features is not None:
                        track_features.append(
                            [*track, *itemgetter(*audio_features[4:])(features)]
                        )

                sub_dataset = pd.DataFrame(track_features)
                sub_dataset.to_csv(file, index=False, mode="a", header=False)


def main():
    load_dotenv()
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")
    spotify_crawler = SpotifyCrawler(client_id, client_secret)

    dataset = spotify_crawler.create_dataset(audio_features, "dataset.csv")

    genres_list = spotify_crawler.get_genres_list()
    print(genres_list)

    your_metal = [
        "alt-rock",
        "alternative",
        "black-metal",
        "death-metal",
        "emo",
        "grunge",
        "hard-rock",
        "hardcore",
        "heavy-metal",
        "j-rock",
        "metal",
        "metal-misc",
        "metalcore",
        "psych-rock",
        "punk",
        "punk-rock",
        "rock",
        "rock-n-roll",
        "rockabilly",
    ]

    spotify_crawler.dataset_by_genres(your_metal, "dataset.csv")


if __name__ == "__main__":
    main()
