# Video-maker-with-Reddit
A vidéo maker that use the youtube and reddit api 

To use this you'll need:
- a intro named "Intro.mpeg"
- a outro named "Outro.mpeg"
- a video (any, will be deleted then replaced by the end video) named "ma_video.mp4"
- a json file with the informations here https://www.reddit.com/prefs/apps (you will need to create a app) on this format named "credentials.json"
    {
    "client_id": personal use script key,
    "api_key": secret key,
    "username": your reddit username,
    "password": your reddit password
    } 
- a json file named "code_secret_client.json" that you download from https://console.cloud.google.com/home/dashboard after crating a projet

- if you get confuse you can follow this tutorial : https://learndataanalysis.org/how-to-upload-a-video-to-youtube-using-youtube-data-api-in-python/
  a part of my code is taken from him
