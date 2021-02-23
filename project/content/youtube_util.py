# Get YoutubeData API key
from credentials import youtube_data_api_token

# from pytube import YouTube
import requests

def get_video_metadata(video_id):
    metadata = {}
    try:
        # Call YouTube Data API
        video_api_endpoint = "https://www.googleapis.com/youtube/v3/videos"
        video_api_params = {
            "key":youtube_data_api_token,
            "id": video_id,
            "part": "snippet"
        }
        response = requests.get(video_api_endpoint, params=video_api_params)

        if response.status_code == 200:
            video_data = response.json()
            snippet = video_data['items'][0]['snippet']
            thumbnail_res = 'standard'
            if 'maxres' in snippet['thumbnails']:
                thumbnail_res = 'maxres'
            metadata = {
                "title": snippet['title'],
                "author": snippet['channelTitle'],
                "thumbnail_url": snippet['thumbnails'][thumbnail_res]['url']
            }
    except Exception as e:
        print(e)
    return metadata
    
