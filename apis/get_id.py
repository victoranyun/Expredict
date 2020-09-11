from creds import get_credentials, call_api


def get_facebook_pages(cred):
    """
    {facebook-graph-api-url}/me/accounts
    :param cred: Endpoint parameters
    :return: Object data
    """
    parameters = dict()
    parameters['access_token'] = cred['access_token']
    url = cred['endpoint_base'] + 'me/accounts'

    return call_api(url, cred)


cred = get_credentials()
res = get_facebook_pages(cred)

print(res['json_data']['data'][0]['id'])

