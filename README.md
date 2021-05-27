# Reddit-User-Media-Downloader-Public

Download all the picture/video posts from a particular user on Reddit, for uh...reasons. Automatically removes duplicates :star:.

## QuickStart with Docker 

The simplest way to run this tool is from Docker due to the number of overlapping dependencies.

1. Install Docker from this link - https://docs.docker.com/engine/install/  (make sure virtualization is enabled in your BIOS)
2. Pull the image from Docker Hub with
```
docker pull monkeymaster64/reddit-media-downloader:latest
```
3. To run the tool, from the shell (CMD for Windows, bash for Linux/MAC) run the following commmand
```
docker run -v "[Path to folder to store output]:/usr/src/app/Reddit-User-Media-Downloader-Public/output" monkeymaster64/reddit-media-downloader --user [Reddit username] --limit [maximum number of posts to download from user]
```

An example is

```
docker run -v "C:\Users\User\Downloadsr:/usr/src/app/Reddit-User-Media-Downloader-Public/output" monkeymaster64/reddit-media-downloader --user monkeymaster64 --limit 10
```

## Usage from Command Prompt

If you choose to run the tool natively, here is how you'd run it from Python in your shell

```--limit``` tag is optional
```
python3 reddit-media-downloader.py --user [case-sensitive username] --limit [maximum number of posts to download from user]
```
## Requirements
- Python 3.8
- Microsoft Visual Studio Build Tools (C++ Build Tools) <--- **only required if you're on Windows**

### Python libraries
- youtube_dl 
- imagededup
- OpenCV2
- Cython
- Requests

### How to Install Python Requirements

```
pip install -r requirements.txt
```

### How to Install Visual C++ Build Tools

1. Download the executable from this link - https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Select the "C++ Build Tools" workload under "Desktop and Mobile"
3. When it's finished downloading and installing, restart your PC

![C++ Build Tools Instructions](https://user-images.githubusercontent.com/16315128/119354163-5cd54200-bc69-11eb-885c-4c3b9ab6cac0.png)

