import requests
import sys


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


    def request(self, url):
        auth = "Bearer " + self.token
        headers = {"Authorization" : auth}
        response = requests.get(url, headers=headers)

        print('[Response] status_code: ' + str(response.status_code), file=sys.stdout)
        print('Response headers: ' + str(response.headers), file=sys.stdout)

        if(response.status_code == 429):
            sec_to_sleep = response.headers.get('retry-after')
            print('Retry-after: ' + str(sec_to_sleep))

        return response.json()    


    def search(self, search_config):
        type = search_config['type']
        year = search_config['year']
        limit = search_config['limit']

        url = "https://api.spotify.com/v1/search?q=year%3A" + year + "&type=" + type + "&limit=" + limit + "&offset="
   
        for i in range(0, 1000, int(limit)):
            artist_name = []
            curr_url = url + str(i)
            print('Curr URL: ' + curr_url)
            tracks = self.request(curr_url)
            for i, t in enumerate(tracks['tracks']['items']):
                artist_name.append(t['artists'][0]['name'])
        
            print(artist_name)




