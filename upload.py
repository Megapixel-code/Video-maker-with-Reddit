def send(date):
    from Google import Create_Service
    from googleapiclient.http import MediaFileUpload

    CLIENT_SECRET_FILE = 'code_secret_client.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    date = date.replace(hour=10, minute=0, second=0, microsecond=0)
    upload_date_time = date.isoformat() + '.000Z'

    f = open('Video_Number.txt', 'r')
    video_number = int(f.read())
    video_number += 1
    f.close()

    request_body = {
        'snippet': {
            'categoryId': 23,
            'title': 'WEEKLY REDDIT [r/mildlyinteresting] #'+str(video_number),
            'description': 'Thanks for watching the video! \n\n►If you liked the video you can subscibe I would realy apreciate! \n►And if you have any videos sugestions tell me in the comments! \n\n\n\n\n#Reddit #mildlyinteresting',
            'tags': ['reddit', 'mildlyinteresting', 'r/mildlyinteresting', 'reddittts', 'redditstories', 'read']
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False,
        },
        'notifySubscribers': True
    }

    mediaFile = MediaFileUpload('ma_video.mp4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()

    f = open('Video_Number.txt', 'w')
    f.write(str(video_number))
    f.close()

