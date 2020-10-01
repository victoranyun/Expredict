import requests
import json


def get_credentials():
    """
    Holds basic credentials of Facebook's App that the user is logging into
    :return: dictionary with the required fields
    """
    credentials = dict()
    credentials['access_token'] = ''
    credentials['client_id'] = ''
    credentials['client_secret'] = ''
    credentials['graph_domain'] = 'https://graph.facebook.com/'
    credentials['graph_version'] = 'v7.0'
    credentials['username'] = ''
    credentials['endpoint_base'] = credentials['graph_domain'] + credentials[
        'graph_version'] + '/'
    credentials['page_id'] = '926554251020729'
    credentials['ig_id'] = '17841407391222597'

    return credentials


def call_api(url, endpoint_params):
    """
    Calls the API via a GET request
    :param url: the url of the endpoint
    :param endpoint_params: parameters for the endpoint
    :return: returns the response in json formatted
    """
    data = requests.get(url, endpoint_params)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpoint_params
    response['formatted_endpoint_params'] = json.dumps(endpoint_params, indent=4, sort_keys=True)
    response['json_data'] = json.loads(data.content)
    response['formatted_json_data'] = json.dumps(response['json_data'], indent=4, sort_keys=True)

    return response


def print_data(response):
    """
    A print function
    :param response: raw data
    :return: prints the pretty json version of the raw data
    """
    # print(response['json_data_pretty'])
    return

