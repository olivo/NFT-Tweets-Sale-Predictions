from operator import neg
import requests
from requests.structures import CaseInsensitiveDict
import json
import time

bearerToken = "BEARER_TOKEN"

#url = "https://api.twitter.com/2/tweets/20"
#url = "https://api.twitter.com/2/tweets/search/recent?query=%23bayc&max_results=10&tweet.fields=created_at"
#url = "https://api.twitter.com/2/tweets/search/all?query=%23bayc&max_results=10"

def fetch_tweets():
    #url = "https://api.twitter.com/2/tweets/search/recent?query=%23bayc&max_results=10&tweet.fields=created_at"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + bearerToken
    
    next_token = ""
    #next_token = "b26v89c19zqg8o3fpyql915yy5ybswfhcze73gcu8sepp"

    current_request = 0
    #current_request = 5637 

    while True:
        #print(headers["Authorization"])

        print("Current 'next_token': " + next_token )

        if next_token == "":
            #url = "https://api.twitter.com/2/tweets/search/recent?query=coolcats&max_results=100&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/recent?query=cryptopunks&max_results=100&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/recent?query=doodlesnft&max_results=100&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/recent?query=bayc&max_results=100&tweet.fields=created_at,author_id"

            #url = "https://api.twitter.com/2/tweets/search/all?query=coolcats&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T00:01:01Z&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/all?query=cryptopunks&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T05:01:01Z&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/all?query=doodlesnft&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T05:01:01Z&tweet.fields=created_at,author_id"
            #url = "https://api.twitter.com/2/tweets/search/all?query=bayc&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T18:21:29Z&tweet.fields=created_at,author_id"

            url = "https://api.twitter.com/2/tweets/search/all?query=coolcats&max_results=500&start_time=2021-07-01T00:00:01Z&end_time=2021-10-31T00:00:01Z&tweet.fields=created_at,author_id"
        else:
            #url = "https://api.twitter.com/2/tweets/search/recent?query=coolcats&max_results=100&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/recent?query=cryptopunks&max_results=100&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/recent?query=doodlesnft&max_results=100&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/recent?query=bayc&max_results=100&tweet.fields=created_at,author_id&next_token="+next_token
            
            #url = "https://api.twitter.com/2/tweets/search/all?query=coolcats&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T00:01:01Z&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/all?query=cryptopunks&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T05:01:01Z&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/all?query=doodlesnft&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T05:01:01Z&tweet.fields=created_at,author_id&next_token="+next_token
            #url = "https://api.twitter.com/2/tweets/search/all?query=bayc&max_results=500&start_time=2022-03-01T00:00:01Z&end_time=2022-03-18T18:21:29Z&tweet.fields=created_at,author_id&next_token="+next_token
            
            url = "https://api.twitter.com/2/tweets/search/all?query=coolcats&max_results=500&start_time=2021-07-01T00:00:01Z&end_time=2021-10-31T00:00:01Z&tweet.fields=created_at,author_id&next_token="+next_token

        # Sleep for one second to avoid rate limiting.
        time.sleep(1)

        resp = requests.get(url, headers=headers)

        #print(resp.content)

        twitter_json_response = json.loads(resp.content)
        #print("Data:")
        #print(twitter_json_response['data'])

        if 'data' not in twitter_json_response:
            print(resp.content)
            break

        twitter_data = twitter_json_response['data']
        #f1 = open("data/"+"coolcats/"+"coolcats_"+str(current_request)+".txt", "w", encoding='utf-8')
        #f1 = open("data/"+"cryptopunks/"+"cryptopunks_"+str(current_request)+".txt", "w", encoding='utf-8')
        #f1 = open("data/"+"doodlesnft/"+"doodlesnft_"+str(current_request)+".txt", "w", encoding='utf-8')
        #f1 = open("data/"+"bayc/"+"bayc_"+str(current_request)+".txt", "w", encoding='utf-8')

        f1 = open("data/raw/"+"coolcats/07-10_2021/"+"coolcats_"+str(current_request)+".txt", "w", encoding='utf-8')
        
        f1.write(str(twitter_data))

        if 'next_token' not in twitter_json_response['meta']:
            break

        next_token = twitter_json_response["meta"]['next_token']

        current_request += 1

        #print("next_token")
        #print(twitter_json_response["meta"]['next_token'])

        #f1 = open("opensea_assets_response.txt", "w")
        #f1.write(html.decode())
        #f1.close()

        #print(resp.status_code)
        #print(resp.content)

fetch_tweets()