#!/usr/bin/env python
import os
import requests
import magic
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
from bs4 import BeautifulSoup


def get_latest_song():
    base_url = 'http://timtimebomb.com'

    r = requests.get(base_url, headers=get_headers())
    soup = BeautifulSoup(r.content)
    latest_url = soup.h2.a['href']

    if latest_url:
        get_song_info(latest_url)
    else:
        print_msg('Dang, couldn\'t find the latest.')


def get_song_info(url):
    print_msg('Requesting the page at %s' % url)

    r = requests.get(url, headers=get_headers())
    soup = BeautifulSoup(r.content)

    song_info = {
        'title': soup.article.h2.a.string,
        'image_url': soup.article.img['src'],
        'date_published': soup.select("span.date")[0].string
    }

    src = soup.iframe['src'].split('?')[0]
    video_id = src.split('/')[-1]
    mp3_name = '%s.mp3' % song_info['title']

    download_mp3(src, video_id, mp3_name)
    tag_mp3(mp3_name, song_info)


def download_mp3(src, video_id, mp3_name):
    """
        Using youtube-dl, download an mp3 of the given src and rename it from
        the video id to the given mp3_name.
    """
    os.system("youtube-dl --id -x --audio-format mp3 %s" % src)
    os.rename('%s.mp3' % video_id, mp3_name)


def tag_mp3(mp3, song_info):
    """
        Using the Mutagen module, set the title, artist, year, and cover image
        the give mp3.
    """
    artist = 'Tim Timebomb and Friends'
    cover_img = get_cover_img(song_info['image_url'])
    title = song_info['title']

    easyid3_audio = EasyID3(mp3)
    easyid3_audio['title'] = u'%s' % title
    easyid3_audio['artist'] = u'%s' % artist

    if song_info['date_published']:
        year = song_info['date_published'].split(',')[1].strip()
    else:
        print_msg('The Parser couldn\'t find date_published, defaulting to 2013')
        year = '2013'

    easyid3_audio['date'] = year

    easyid3_audio.save()

    # EasyID3 does not allow you to set the APIC tag
    id3_audio = ID3(mp3)
    id3_audio.add(
        APIC(encoding=3,
            mime=cover_img['mime'],
            type=3,
            desc=u'Cover',
            data=open(cover_img['img']).read()
        )
    )

    id3_audio.save()

    # Clean up
    os.remove(cover_img['img'])
    print_msg('"%s" is ready to roll.' % title)
    os.system('open %s ' % os.getcwd())


def get_headers():
    """
        The site blocks bots so I was getting a 403 trying to request the image
        Send a User-Agent to get around that busch league shit
    """
    headers = {}
    headers['User-Agent'] = "Ticking Timebomb 1.0"
    return headers


def get_cover_img(img_url):
    """
        Download the image from the site and create a new image on the fs from it.
        Return the name of the image file and the image mime type
    """
    orig_img = requests.get(img_url, headers=get_headers())
    img_name = img_url.split('/')[-1]

    img = open(img_name, 'wb')
    img.write(orig_img.content)
    img.close()

    return {
        'img': img_name,
        'mime': magic.from_file(img_name, mime=True)
    }


def print_msg(msg):
    print '[timebomb] %s' % msg


def main():
    parser = argparse.ArgumentParser(description='Download and tag a fucking awesome Tim Timebomb and Friends Song')
    parser.add_argument('-u', '--url', help='The url of the song')
    args = parser.parse_args()

    if args.url:
        # At this spot I was surprise that I had to define functions top-down
        # for only methods that are called via args or CLI or whatever is happening
        get_song_info(args.url)
    else:
        get_latest_song()


if __name__ == '__main__':
    main()
