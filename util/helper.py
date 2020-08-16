import os
import requests
import json
import numpy as np

directory = "../img/"


def download(username):
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data['wittytumblrs']:
            r = requests.get(i.get('display_url'))
            with open(directory + i.get('shortcode') + '.jpeg', 'wb') as file:
                file.write(r.content)


def likes(username):
    likes_arr = []
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data['wittytumblrs']:
            likes_count = i.get('likes_count')
            likes_arr.append(likes_count)
    return np.array(likes_arr)


# likes('wittytumblrs')
