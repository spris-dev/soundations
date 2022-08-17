import os
from SpotifyCrawler import SpotifyCrawler
from dotenv import load_dotenv
load_dotenv()


def main():
  client_id = os.environ.get('CLIENT_ID')
  client_secret = os.environ.get('CLIENT_SECRET')
  spotify_crawler = SpotifyCrawler(client_id, client_secret)                    

  search_config = {'type':'track', 'year':'2000-2020', 'limit':'50'}

  spotify_crawler.search(search_config)


if __name__ == "__main__":
  main()  

