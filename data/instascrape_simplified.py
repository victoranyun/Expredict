import re
import json
import requests
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver

PATH = '~/Expredict/data/'

def where_json(file_name):
    return os.path.exists(file_name)

wd = webdriver.Chrome()
usersFile = open('usernames.txt', 'r')
usernames = usersFile.read().split('\n')

jsonObject = {}

# for i, ats in enumerate(usernames):

