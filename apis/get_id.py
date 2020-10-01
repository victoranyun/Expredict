from creds import call_api


def get_facebook_pages(cred):
    """
    {facebook-graph-api-url}/me/accounts
    :param cred: Endpoint parameters
    :return: Array of username + instagram_id, e.g. [username, ig_id]
    """
    parameters = dict()
    parameters['access_token'] = cred['access_token']
    url = cred['endpoint_base'] + 'me/accounts'
    res = call_api(url, cred)
    page_id = res['json_data']['data'][0]['id']
    username = res['json_data']['data'][0]['name']
    cred['page_id'] = page_id
    url2 = cred['endpoint_base'] + cred['page_id'] + '?fields=instagram_business_account&access_token=' + \
           parameters['access_token']
    url2_res = call_api(url2, cred)
    user_info = [username, url2_res]
    return user_info
