import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
import json
from mock_data import mock_search

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
production_mode = False

def main():
	youtube = generate_youtube_auth_request()
	request = generate_request(youtube, 'tesla', 25)
	
	response = None
	if production_mode:
		#print "production mode"
		response = request.execute()
	else:
		#print "test mode"
		response = mock_search()
		
	display_results(response)

def generate_request(client, keyword, results):
	request = client.search().list(
		part="snippet",
		order="viewCount",
		type="video",
		maxResults=results,
		q=keyword
	)
	return request
	
def generate_youtube_auth_request():
	os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

	api_service_name = "youtube"
	api_version = "v3"
	service_account_file = "credentials/service.json"

	if not os.path.exists(service_account_file):
		print('Service account file missing')
	
	credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=scopes)
	youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)
	return youtube
  
	
def display_results(response):
	for key, value in response.items():
		#print key
		if key == "items":
			item_collection = value
			for video_obj in item_collection:
				#id = video_obj['snippet']['']
				title = video_obj['snippet']['title']
				thumbnail = video_obj['snippet']['thumbnails']['default']
				
				print title
	
if __name__ == "__main__":
	main()
	
	