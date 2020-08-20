import json
import time
from urllib.request import urlopen
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver

PATH = '~/Expredict/data/archived'


def scroll(driver, t):
    timeout = t
    previous_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(timeout)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == previous_height:
            break
        previous_height = new_height


def source_to_json(source_html):
    data = bs(source_html, 'html.parser')
    body = data.find('body')
    script = body.find('script', text=lambda t: t.startswith('window._sharedData'))
    page_json = script.string.split(' = ', 1)[1].rstrip(';')
    return page_json


wd = webdriver.Chrome()
users_file = open('../usernames.txt', 'r')
usernames = users_file.read().split('\n')

json_object = {}

for i, username in enumerate(usernames):
    print("Scraping Instagram profile:", username)
    insta_url = 'https://instagram.com'
    full_url = insta_url + '/' + username
    wd.get(full_url)

    scroll(wd, 3.5)

    media_links = []
    source = wd.page_source

    finalData = json.loads(source_to_json(source))

    print(json.dumps(finalData, sort_keys=True, indent=4))

    for link in finalData['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']:
        media_links.append('https://www.instagram.com' + '/p/' + link['node']['shortcode'] + '/')

    print(media_links)

    finalResults = pd.DataFrame()
    arr = []
    for j in range(len(media_links)):
        try:
            media_source = urlopen(media_links[j]).read()  # fetching page
            media_data = bs(media_source, 'html.parser')
            media_body = media_data.find('body')
            media_script = media_body.find('script')

            raw = media_script.text.strip().replace('window._sharedData =', '')
            raw2 = raw.replace(';', '')
            media_json = json.loads(raw2)
            posts = media_json['entry_data']['PostPage'][0]['graphql']
            posts = json.dumps(posts)
            posts = json.loads(posts)
            posts = posts.get('shortcode_media')
            actual_display_url = posts.get('display_url').replace('\u0026', '&')

            dict_posts = {}

            if not posts.get('is_video'):
                dict_posts = {'owner_username': posts.get('owner').get('username'), 'shortcode': posts.get('shortcode'),
                              'dimensions': posts.get('dimensions'), 'display_url': actual_display_url,
                              'likes_count': posts.get('edge_media_preview_like').get('count'),
                              'comments_count': posts.get('edge_media_preview_comment').get('count')}

                shortcode_display_url_and_likes = {'shortcode': posts.get('shortcode'),
                                                   'display_url': actual_display_url,
                                                   'likes_count': posts.get('edge_media_preview_like').get('count')}
                arr.append(shortcode_display_url_and_likes)
                json_posts = {posts.get('owner').get('username'): arr}
            p = pd.DataFrame.from_dict(pd.json_normalize(dict_posts), orient='columns')
            finalResults = finalResults.append(p)
        except TypeError:
            np.nan

    finalResults = finalResults.drop_duplicates(subset='shortcode')
    finalResults.index = range(len(finalResults.index))
    with open('data.csv', 'wb'):
        finalResults.to_csv(r'~/Expredict/data/data.csv')

    with open('data.json', 'w') as json_data:
        json_string = json.dumps(json_posts, sort_keys=True, indent=4)
        json_data.write(json_string)

    wd.close()
