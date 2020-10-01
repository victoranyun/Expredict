import os
import requests
import json
import numpy as np


def download():
    """
    Helper functions to download the images according to the display_url from the scraper
    :return: N/A
    """
    directory = "../img/"
    users_file = open('../data/usernames.txt', 'r')
    username = users_file.read()
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data[username]:
            r = requests.get(i.get('display_url'))
            with open(directory + i.get('shortcode') + '.jpeg', 'wb') as file:
                file.write(r.content)


def likes():
    """
    Uses scraped .json to create an array
    :return:
    """
    likes_arr = []
    users_file = open('../scraper/usernames.txt', 'r')
    username = users_file.read()
    with open('../data/data.json') as json_file:
        data = json.load(json_file)
        for i in data[username]:
            likes_count = i.get('likes_count')
            likes_arr.append(likes_count)
    return likes_arr


# download()
