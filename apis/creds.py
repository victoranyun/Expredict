import requests
import json


def get_credentials():
    credentials = dict()
    credentials['access_token'] = ''
    credentials['client_id'] = ''
    credentials['client_secret'] = ''
    credentials['graph_domain'] = 'https://graph.facebook.com/'
    credentials['graph_version'] = 'v7.0'
    credentials['username'] = ''
    credentials['endpoint_base'] = credentials['graph_domain'] + credentials[
        'graph_version'] + '/'
    credentials['account_id'] = ''

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

