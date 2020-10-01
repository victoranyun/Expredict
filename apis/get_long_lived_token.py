from creds import get_credentials, call_api


def get_access_token(cred):
    """
    Endpoint:
    "https://graph.facebook.com/{graph-api-version}/oauth/access_token?
        grant_type=fb_exchange_token&
        client_id={app-id}&
        client_secret={app-secret}&
        fb_exchange_token={your-access-token}"
    :param cred: Endpoint parameters
    :return: Response from endpoint (long lived token 30 days)
    """
    parameters = dict()
    parameters['grant_type'] = 'fb_exchange_token'
    parameters['client_id'] = cred['client_id']
    parameters['client_secret'] = cred['client_secret']
    parameters['fb_exchange_token'] = cred['access_token']
    url = cred['endpoint_base'] + 'oauth/access_token'
    return call_api(url, parameters)


