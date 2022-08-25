import os
import pandas as pd
from SpotifyCrawler import SpotifyCrawler
from dotenv import load_dotenv
load_dotenv()


def main():
  client_id = os.environ.get('CLIENT_ID')
  client_secret = os.environ.get('CLIENT_SECRET')
  spotify_crawler = SpotifyCrawler(client_id, client_secret)                    

  artists = []
  for year in range(1920, 2023):
    search_config = {'type':'artist', 'year':str(year), 'limit':'50'}
    artists = artists + spotify_crawler.search_for_artists(search_config)

  print("NUMBER OF ARTISTS: " + str(len(artists)))

  tracks = []
  for artist in artists:
    tracks = tracks + spotify_crawler.get_artist_tracks(artist)

  print("NUMBER OF TRACKS: " + str(len(tracks)))

  track_features = spotify_crawler.get_track_features(tracks[0])
  columns = track_features.keys()

  dataset = pd.DataFrame(columns=columns)

  track_features = []
  for track in tracks:
    track_features.append(spotify_crawler.get_track_features(track))

  track_features = pd.DataFrame(track_features)
  dataset = pd.concat([dataset, track_features], ignore_index=True)
  print(dataset)  
  dataset.to_csv('dataset.csv', index=False)


if __name__ == "__main__":
  main()  
  