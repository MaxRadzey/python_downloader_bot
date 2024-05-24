import requests
from bs4 import BeautifulSoup


url = 'https://www.tiktok.com/@_il9_/video/7043465037918326018'

response = requests.get(url, stream=True)
page = BeautifulSoup(response.content, 'html.parser')


def get_video(url):

    cookies = {
        '_ga': 'GA1.1.1724469622.1716577356',
        '_ga_ZSF3D6YSLC': 'GS1.1.1716577356.1.1.1716577404.0.0.0',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'ru,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.1.1724469622.1716577356; _ga_ZSF3D6YSLC=GS1.1.1716577356.1.1.1716577404.0.0.0',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': url,
        'locale': 'en',
        'tt': 'enZHdncy',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    soupe = BeautifulSoup(response. text, 'html.parser')
    download_link = soupe.a['href']
    response = requests.get(download_link, stream=True)
    with open('test.mp4', 'wb') as f:
        for chunk in response.iter_content(1024):
            if chunk:
                f.write(chunk)


get_video(url)
