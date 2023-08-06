from __future__ import unicode_literals
from datetime import datetime
import yt_dlp
import requests
import re
import tempfile
from PIL import Image
from io import BytesIO
from pathlib import Path
import json

class BasketCase:
    def __init__(self, session_id=None):
        self._session = requests.Session()

        if session_id:
            self._session.cookies.set('sessionid', session_id)

        self._output_base = f'{Path.cwd()!s}/basketcase_{datetime.now()!s}'
        self._output_images = self._output_base + '/images'
        self._output_videos = self._output_base + '/videos'

    def fetch(self, target_urls):
        urls = self._scan(target_urls)

        if urls['images'] or urls['videos']:
            self._prepare_output()

            for url in urls['images']:
                self._get_image(url)
            
            self._get_videos(urls['videos'])
        else:
            print('Nothing to download.')

    def _prepare_output(self):
        Path(self._output_images).mkdir(parents=True, exist_ok=True)
        Path(self._output_videos).mkdir(parents=True, exist_ok=True)

    def _scan(self, target_urls):
        sets = {
            'images': set(),
            'videos': set()
        }

        print('Scanning the targets. This can take a while.')

        for target_url in target_urls:
            json_string = None

            with self._session.get(target_url, timeout=10) as request:
                json_string = re.search(r'window\.__additionalDataLoaded\s*\(\s*[^,]+,\s*({.+?})\s*\);', request.text)

                if not json_string:
                    raise RuntimeError(f'JSON string not found at {target_url}')

            json_data = json.loads(json_string.group(1))

            if 'carousel_media' in json_data['items'][0]:
                for media in json_data['items'][0]['carousel_media']:
                    sets['images'].add(media['image_versions2']['candidates'][0]['url'])

                    if 'video_versions' in media:
                        sets['videos'].add(media['video_versions'][0]['url'])
            else:
                if 'image_versions2' not in json_data['items'][0]:
                    raise RuntimeError(f'Unrecognized JSON structure at {target_url}')
                
                sets['images'].add(json_data['items'][0]['image_versions2']['candidates'][0]['url'])

                if 'video_versions' in json_data['items'][0]:
                    sets['videos'].add(json_data['items'][0]['video_versions'][0]['url'])

        return sets

    def _get_image(self, url):
        print(f'Downloading image: {url}')

        request = self._session.get(url, timeout=10)

        # Build image from binary response data
        image = Image.open(BytesIO(request.content))
        fp = tempfile.NamedTemporaryFile(prefix='basketcase_', suffix='.jpg', dir=self._output_images, delete=False)
        image.save(fp, format='JPEG')

    def _get_videos(self, urls):
        if self._session.cookies.get('sessionid'):
            # Add the session cookie
            yt_dlp.utils.std_headers.update({'Cookie': 'sessionid=' + self._session.cookies.get('sessionid')})

        ydl_opts = {
            'outtmpl': self._output_videos + '/%(title)s.%(ext)s' # Set output directory
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

