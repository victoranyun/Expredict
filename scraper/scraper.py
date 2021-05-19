import json
import numpy as np
import requests


def get_media_urls():
    """
    Gets all media URLs on a specified username in username.txt
    :return:
    """
    users_file = open('usernames.txt', 'r')
    usernames = users_file.read().split('\n')
    arr = []
    for i, username in enumerate(usernames):
        try:
            print("Scraping:", username)
            insta_url = 'https://instagram.com/' + username + '/?__a=1'  # print(insta_url)
            response = requests.get(insta_url)
            raw = response.content
            json_object = json.loads(raw)
            user_id = json_object['graphql']['user']['id']
            end_cursor = ''
            json_posts = {}
            while True:
                query_url = 'https://instagram.com/graphql/query/' \
                            '?query_id=17888483320059182&id=' + user_id + '&first=12&after=' + end_cursor
                query_response = requests.get(query_url)
                query_raw = query_response.content
                query_json_object = json.loads(query_raw)
                media_edges = query_json_object['data']['user']['edge_owner_to_timeline_media']['edges']
                for media_edge in media_edges:
                    if not media_edge['node']['is_video']:
                        actual_display_url = media_edge['node']['display_url'].replace('\u0026', '&')
                        shortcode_display_url_and_likes = {'shortcode': media_edge['node']['shortcode'],
                                                           'display_url': actual_display_url,
                                                           'likes_count':
                                                               media_edge['node']['edge_media_preview_like'].get('count')}
                        arr.append(shortcode_display_url_and_likes)

                    json_posts = {username: arr}
                page_info = query_json_object['data']['user']['edge_owner_to_timeline_media']['page_info']
                has_next_page = page_info['has_next_page']
                if not has_next_page:
                    break
                else:
                    end_cursor = page_info['end_cursor']
        except TypeError:
            np.nan

    with open('../data/data.json', 'w') as json_data:
        json_string = json.dumps(json_posts, sort_keys=True, indent=4)
        json_data.write(json_string)


def download():
    """
    Helper functions to download the images according to the display_url from the scraper
    :return: N/A
    """
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        users_file = open('usernames.txt', 'r')
        usernames = users_file.read().split('\n')
        for i in usernames:
            r = requests[i['display_url']]
            with open('../data/img/' + i['shortcode'] + '.jpg', 'wb') as file:
                file.write(r.content)


get_media_urls()
