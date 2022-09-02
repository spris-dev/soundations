import requests
import sys
import time


class SpotifyCrawler:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.token = self.get_access_token()


    def get_access_token(self):
        response = requests.post(self.token_url, data={"grant_type": "client_credentials"}, 
                          auth=(self.client_id, self.client_secret))
  
        print('[Response] status_code: ' + str(response.status_code), file=sys.stdout)   
        print('Access Token Headers: ' + str(response.headers), file=sys.stdout)              

        return response.json()["access_token"]


    # def refresh_access_token(self):
    #     response = requests.post(self.token_url, data={"grant_type": "refresh_token"}, 
    #                       auth=(self.client_id, self.client_secret))

    #     return response.json()["access_token"]                  


    def request(self, url):
        auth = "Bearer " + self.token
        headers = {"Authorization" : auth}
        response = requests.get(url, headers=headers)

        if(response.status_code != 200):
            print('[Response] status_code: ' + str(response.status_code), file=sys.stdout)
            print('Response headers: ' + str(response.headers), file=sys.stdout)

        if(response.status_code == 401):
            self.token = self.get_access_token()
            print('Token refreshed')

        if(response.status_code == 429):
            sec_to_sleep = response.headers.get('retry-after')
            print('Retry-after: ' + str(sec_to_sleep))
            time.sleep(sec_to_sleep)

        return response    


    def search_for_artists(self, search_config):
        type = search_config['type']
        year = search_config['year']
        limit = search_config['limit']

        url = "https://api.spotify.com/v1/search?q=year%3A" + year + "&type=" + type + "&limit=" + limit + "&offset="

        artist_names = []
        for i in range(0, 1000, int(limit)):
            curr_url = url + str(i)
            tracks = self.request(curr_url).json()
            for i, t in enumerate(tracks['artists']['items']):
                artist_names.append((t['name'], t['id']))

        return artist_names


    def get_artist_tracks(self, artist_name):
        url = "https://api.spotify.com/v1/artists/" + str(artist_name[1]) + "/top-tracks?market=ES"
        #url = "https://api.spotify.com/v1/artists/" + str(artist_name[1]) + "/top-tracks"
        response = self.request(url).json()
        tracks = []
        for i, t in enumerate(response['tracks']):
            tracks.append((t['name'], t['id']))
    
        return tracks


    def get_track_features(self, track_name):
        url = "https://api.spotify.com/v1/audio-features/" + str(track_name[1])
        response = self.request(url).json()

        return response
        