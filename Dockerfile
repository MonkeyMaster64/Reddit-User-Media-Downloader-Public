FROM python:3.8

RUN apt-get update && apt-get install -y git libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx
RUN git --version

WORKDIR /usr/src/app

RUN git clone https://github.com/MonkeyMaster64/Reddit-User-Media-Downloader-Public

WORKDIR /usr/src/app/Reddit-User-Media-Downloader-Public

RUN pip install imagededup==0.2.2 --no-dependencies
RUN pip install matplotlib==3.4.2
RUN pip install scikit-learn==0.24.2
RUN pip install PyWavelets~=1.1.1
RUN pip install youtube_dl==2021.5.16
RUN pip install cython==0.29.23
RUN pip install opencv-python==4.5.2.52 
RUN pip install Pillow==6.2.2
RUN pip install tqdm==4.60.0
RUN pip install tensorflow==2.5.0

ENTRYPOINT ["python3", "reddit-media-downloader.py"]