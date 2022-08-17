import os
import requests
import sys
from dotenv import load_dotenv
load_dotenv()

def get_access_token(url, client_id, client_secret):
  response = requests.post(url, data={"grant_type": "client_credentials"}, 
                          auth=(client_id, client_secret))
  
  print('response status_code: ' + str(response.status_code), file=sys.stdout)   
  print('ACcess Token Headers: ' + str(response.headers))              

  return response.json()["access_token"]                         


def get_track_info(url, access_token):
  auth = "Bearer " + access_token
  headers = {"Authorization" : auth}
  response = requests.get(url, headers=headers)

  print('\nresponse status_code: ' + str(response.status_code), file=sys.stdout)  
  print('GET response headers: ' + str(response.headers), file=sys.stdout)

  if(response.status_code == 429):
    sec_to_sleep = response.headers.get('retry-after')
    print('need to sleep for: ' + str(sec_to_sleep))

  return response.json()


def main():
  url = 'https://accounts.spotify.com/api/token'
  client_id = os.environ.get('CLIENT_ID')
  client_secret = os.environ.get('CLIENT_SECRET')

  access_token = get_access_token(url, client_id, client_secret)
  print('access token: ' + str(access_token), file=sys.stdout)                      

  artist_name = []

  for j in range(1000):
    for i in range(0, 1000, 50):
      url = "https://api.spotify.com/v1/search?q=year%3A1980-2019&type=track&limit=50&offset=" + str(i)
      tracks = get_track_info(url, access_token)
      for i, t in enumerate(tracks['tracks']['items']):
            artist_name.append(t['artists'][0]['name'])
    print("Number of downloaded tracks: " + str(len(artist_name)))


if __name__ == "__main__":
    main()  

