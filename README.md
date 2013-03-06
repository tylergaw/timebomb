# Timebomb

A little script to download and tag mp3s versions of songs from
http://timtimebomb.com.

**This is the first Python script I've ever written so it's probabably a hot mess.**

## Options
    -u, --url    The url of the song

## Dependencies
- youtube-dl https://github.com/rg3/youtube-dl/
  - ffmpeg - brew install ffmpeg

## Python Reqs

`pip install -r requirements.txt`

    beautifulsoup4==4.1.3
    distribute==0.6.31
    mutagen==1.21
    python-magic==0.4.3
    requests==1.1.0
    wsgiref==0.1.2