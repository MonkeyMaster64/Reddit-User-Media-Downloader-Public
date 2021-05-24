#!/usr/bin/env python3

## simple reddit media downloader
## downloads reddit media quick & easy
## not the best but it works


from locale import Error
import requests, datetime
import youtube_dl
import argparse, sys
import json
import os, sys
import time
import logging
import cv2
from imagededup.methods import PHash

'''
Duplication removal algorithm using imagededup

- Extract and save first frame from each video downloaded as a file and in a dict
- Use imagededup lib to get dictionary of all duplicates and originals in working folder
- Iterate through the dictionary
- If the value is in the dict of frames, delete the videos associated with the duplicate images as well as the duplicate images
- Then, delete the original frame
- If the value is not in the dict of frames, delete all the duplicates

'''

args = {}
url_list = []

# pushshift helper function
def get_posts(post_type,params, cb, limit=-1):
    if limit != -1:
        if limit >= 100:
            size = 100
        else:
            size = limit
    else:
        size = 100
    last = int(datetime.datetime.now().timestamp())
    got = 0
    while True:
        logging.info(f"Fetching posts made before {last}")
        req_params = {
                **params,
                'size':size,
                'before':last
                }
        req_headers = {
                'User-Agent':'Python requests - Redditstat.py'
                }
        res = requests.get(f'https://api.pushshift.io/reddit/{post_type}/search', params=req_params, headers=req_headers)
        res.raise_for_status()
        data = res.json()["data"]
        cb(data)
        if len(data) < 100 or (limit != -1 and got >= limit):
            got += len(data)
            logging.info(f"Total of {got} posts fetched from u/{params['author']}")
            return
        else:
            last = data[-1]["created_utc"]
            got += 100

def submission_callback(data):
    print (len(data))
    for post in data:
        process_submission(post)

def process_submission(post):
    global url_list
    try:
        if not post['is_self'] and post['url'] not in url_list:
            if not post['is_video'] and "gif" not in post['url']:
                try:
                    res = requests.get(post['url'])
                    if(res):
                        print("Downloading file")
                        print (post['url'])
                        target_file = os.path.join(post['author'], f"{datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')}-{post['url'].split('/')[-1]}")
                        with open(target_file, "wb+") as f:
                            f.write(res.content)
                            logging.info(f"Photo downloaded from {post['url']} and saved to {f.name}")
                except Exception:
                    logging.error(f"Exception downloading {post['url']}.  Skipping.")
                
            else:
                print("Downloading video")
                target_file = os.path.join(post['author'], f"{datetime.datetime.now().strftime('%Y-%m-%dT%H%M%S')}-%(id)s.%(ext)s")
                with youtube_dl.YoutubeDL({'outtmpl':target_file, 'max_downloads': 1}) as ydl:
                    try:
                        info_dict = ydl.extract_info(post['url'], download=False)
                        fn = os.path.basename(ydl.prepare_filename(info_dict))
                        ydl.download([post['url']])
                        logging.info(f"Video downloaded from {post['url']} and saved to {fn}")
                    except (youtube_dl.utils.DownloadError, youtube_dl.utils.MaxDownloadsReached):
                        print("Unable to download")
    except KeyError:
        print("What?")
    url_list.append(post['url'])

def extractFirstFrame(cwd):
    logging.info("Beginning extraction of first frame from videos in the folder")
    videos = []
    for file in os.listdir(cwd):
        if file.endswith(".mp4"):
            videos.append(file)
    print (videos)
    video_images = {}
    for video in videos:
        vidcap = cv2.VideoCapture(os.path.join(cwd, video))
        success, image = vidcap.read()
        if success:
           cv2.imwrite(os.path.join(cwd, video+".jpg"), image)
           video_images[os.path.basename(video)+".jpg"] = os.path.basename(video)
        else:
            logging.error(f"Unable to extract first frame from {video}")
    return video_images
    
       
def removeDuplicates(duplicates, video_frames, images_dir): 
    for image in duplicates:
        if image in video_frames:
            #delete the duplicate image videos then the images 
            if duplicates[image]:
                for img in duplicates[image]:
                    try:
                        os.remove(os.path.join(images_dir, video_frames[img]))
                        os.remove(os.path.join(images_dir, img))
                        logging.info(f"Duplicate video found. Deleting {video_frames[img]}")
                    except FileNotFoundError as e:
                        print(e)
                    duplicates[img] = []
            try:
                os.remove(os.path.join(images_dir, image))
            except FileNotFoundError as e:
                print (e)
        else:
            if duplicates[image]:
                for dup in duplicates[image]:
                    try:
                        os.remove(os.path.join(images_dir, dup))
                        logging.info(f"Duplicate picture found. Deleting {dup}")
                    except FileNotFoundError:
                        print(images_dir + dup + " not found")
                    duplicates[dup] = []
            
        

def main():
    global args
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level='INFO', filename='execution.log')
    #logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level='DEBUG', stream=sys.stdout)
    parser = argparse.ArgumentParser(description="Download reddit media")
    parser.add_argument('-u', '--user', help="USER to download from")
    parser.add_argument('-s', '--subreddit', help="SUBREDDIT to download from")
    parser.add_argument('--ydl-args', help="JSON-format youtube-dl options", default='{}')
    parser.add_argument('-l','--limit',help="Maximum number of posts to be downloaded")
    parser.add_argument('--pushshift-params', help="JSON-formatted pushshift parameters", default='{}')
    args = parser.parse_args()
    logging.info(f"\n\n{'-'*30}\nBeginning download of media from user u/{args.user}")
    try:
       os.makedirs(args.user)
       logging.info(f"Created folder for reddit user {args.user}")
    except OSError as e:
       logging.info(f"Folder already exists for reddit user {args.user}")
       print (e)
    if args.limit:
        get_posts('submission', {**json.loads(args.pushshift_params), 'subreddit':args.subreddit, 'author':args.user}, submission_callback, int(args.limit))
    else:
        get_posts('submission', {**json.loads(args.pushshift_params), 'subreddit':args.subreddit, 'author':args.user}, submission_callback)
    #get working directory
    cwd = os.getcwd()
    images_dir = os.path.join(cwd, args.user)
    #get dict of video first frames
    video_frames = extractFirstFrame(images_dir)
    #get dict of all duplicates in directory
    logging.info("Beginning hashing function to create dict of duplicates")
    phasher = PHash()
    encodings = phasher.encode_images(image_dir=images_dir)
    duplicates = phasher.find_duplicates(encoding_map=encodings)
    print (video_frames)
    print("\n\n")
    print(duplicates)
    removeDuplicates(duplicates, video_frames, images_dir)
    logging.info("Execution complete. Exiting...")
    sys.exit()


if __name__ == "__main__":
    main()