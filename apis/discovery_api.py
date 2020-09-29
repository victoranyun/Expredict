from creds import get_credentials, call_api


def get_instagram_metadata(cred):
    """
    {facebook-graph-api-url}/me/accounts
    :param cred: Endpoint parameters
    :return: Object data
    """
    parameters = dict()
    parameters['access_token'] = cred['access_token']
    url = cred['endpoint_base'] + cred['ig_id'] + '?fields=business_discovery.username(' + cred['username'] + \
                            '){username,name,profile_picture_url,biography,follows_count,followers_count,media_count}'

    return call_api(url, cred)


cred = get_credentials()
res = get_instagram_metadata(cred)
print(res)
