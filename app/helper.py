import requests
import json
import numpy as np


def download():
    directory = "../img/"
    users_file = open('../scraper/usernames.txt', 'r')
    username = users_file.read()
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data[username]:
            r = requests.get(i.get('display_url'))
            with open(directory + i.get('shortcode') + '.jpeg', 'wb') as file:
                file.write(r.content)


def likes():
    likes_arr = []
    users_file = open('../scraper/usernames.txt', 'r')
    username = users_file.read()
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data[username]:
            likes_count = i.get('likes_count')
            likes_arr.append(likes_count)
    return np.array(likes_arr)


download()
