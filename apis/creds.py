import requests
import json


def get_credentials():
    credentials = dict()
    credentials['access_token'] = 'EAAnqNm9ZAVc8BALOHTKOTpypn22fZCX59NyPZCgmXYADH8S1ZBIOhygENLYsTukUcCvtGaDAZAUA2VmcyZCgzbGbBuNPj28C9eAZCRutIZAmqISVQFS6ILdO2vG1s6WgCCKcSjaZBJfBqyHJb1lRN8tXdd0M76JxnSetZChfjmkdKjXZAXVPzGDax7giu8Bwj8dHtZA7mbvt3YXx5AZDZD'
    credentials['client_id'] = '2790794307655119'
    credentials['client_secret'] = '96d6b480bae2ff4cdfe9ec15ef82a8ae'
    credentials['graph_domain'] = 'https://graph.facebook.com/'
    credentials['graph_version'] = 'v7.0'
    credentials['username'] = ''
    credentials['endpoint_base'] = credentials['graph_domain'] + credentials[
        'graph_version'] + '/'
    credentials['page_id'] = '926554251020729'
    credentials['ig_id'] = '17841407391222597'

    return credentials


def call_api(url, endpoint_params):

    data = requests.get(url, endpoint_params)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpoint_params
    response['formatted_endpoint_params'] = json.dumps(endpoint_params, indent=4, sort_keys=True)
    response['json_data'] = json.loads(data.content)
    response['formatted_json_data'] = json.dumps(response['json_data'], indent=4, sort_keys=True)

    return response


def print_data(response):
    print(response['json_data_pretty'])
    return

