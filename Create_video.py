import glob
import os
import praw
import requests
import shutil
import json
import moviepy.editor as mp
import moviepy.video as mpv
import moviepy.video.fx.all as vfx
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode
from os.path import isfile, join


def delete_all_folder():
    directory = 'reddit'
    os.chdir(directory)
    files = glob.glob('*')
    for file_name in files:
        os.unlink(file_name)
    os.chdir('..')


def deemojify(input_str):
    return_output = ''

    for car in input_str:
        try:
            car.encode('ascii')
            return_output += car
        except UnicodeEncodeError:
            replaced = unidecode(str(car))
            if replaced != '':
                return_output += replaced

    return " ".join(return_output.split())


def get_images():
    directory = 'reddit'
    # https://www.reddit.com/r/mildlyinteresting/top/?t=week
    with open('credentials.json') as c:
        params = json.load(c)

    reddit = praw.Reddit(
        client_id=params['client_id'],
        client_secret=params['api_key'],
        password=params['password'],
        user_agent='<reddit_top> accessAPI:v0.0.1 (by/u/Megapixel_YTB)',
        username=params['username']
    )

    subreddit = reddit.subreddit('mildlyinteresting')

    name = 0

    for submitions in subreddit.top("week", limit=50):
        name += 1
        url = submitions.url
        file_name = str(name)
        if url.endswith('.jpg'):
            file_name += '.jpg'
            found = True
        else:
            found = False

        if found:
            r = requests.get(url)
            with open(file_name, 'wb') as f:
                f.write(r.content)

            shutil.move(file_name, directory)

            caption = submitions.title
            title = str(name)
            title += '.txt'

            with open(title, 'wt') as c:
                c.write(deemojify(caption))
                c.close()

            shutil.move(title, directory)


def resize(im, fill_color=(0, 0, 0, 0)):
    img = Image.open(im)
    x, y = img.size
    sizex = int(y / 1080 * 1920)
    sizey = y
    new_im = Image.new('RGB', (sizex, sizey), fill_color)
    new_im.paste(img, (int((sizex - x) / 2), int((sizey - y) / 2)))

    new_im = new_im.resize((1920, 1080), Image.LANCZOS)

    f = open(im[:-4] + '.txt', 'r')
    content = f.read()
    draw = ImageDraw.Draw(new_im)
    draw.rectangle(((0, 0), (1920, 25)), fill=(0, 0, 0))

    font = ImageFont.truetype('arialbd.ttf', size=18)
    txt_size = draw.textsize(content, font=font)[0]
    draw.text((int((1920 - txt_size) / 2), 0), content, fill=(255, 255, 255), font=font)
    f.close()

    os.remove(im)
    new_im.save(im)


def create_tts():
    for file in [f for f in os.listdir('reddit/') if isfile(join('reddit/', f)) and f.endswith('.txt')]:
        f = open('reddit/' + file, 'r')
        my_txt = f.read()
        f.close()
        out = gTTS(text=my_txt, lang='en', slow=False)
        out.save('reddit/' + file[:-4] + '.mp3')


def finish_video():
    all_clips = []
    for file in [f for f in os.listdir('reddit/') if isfile(join('reddit/', f)) and f.endswith('.mp3')]:
        sound = mp.AudioFileClip('reddit/' + file)
        sound = mp.concatenate_audioclips([sound, mp.AudioClip(lambda t: 0, duration=3)])
        all_clips.append(sound)
    all_video_clips = []
    x = 0
    for file in [f for f in os.listdir('reddit/') if isfile(join('reddit/', f)) and f.endswith('.jpg')]:
        resize('reddit/' + file)
        vid = mp.ImageClip('reddit/' + file, duration=all_clips[x].duration)
        all_video_clips.append(vid)
        x += 1

    sound = mp.concatenate_audioclips(all_clips)
    video = mp.concatenate_videoclips(all_video_clips)
    video.audio = sound
    video.fps = 60

    background = mp.VideoFileClip('space.mpeg')
    masked_clip = mpv.fx.all.mask_color(video, color=[0, 0, 0], thr=0, s=0)
    midle_video = mp.CompositeVideoClip([background, masked_clip]).set_duration(video.duration)

    intro = mp.VideoFileClip('Intro.mpeg')
    outro = mp.VideoFileClip('Outro.mpeg')

    final_video = mp.concatenate_videoclips([intro, midle_video, outro])

    os.remove('ma_video.mp4')
    final_video.write_videofile('ma_video.mp4')


def create():
    print()
    delete_all_folder()
    print('Importing the images .....', end='')
    get_images()
    print(' done !')
    print('creating tts .............', end='')
    create_tts()
    print(' done !')
    print('Making the video .........')
    print('===============================================================================================')
    finish_video()
    print('===============================================================================================')
