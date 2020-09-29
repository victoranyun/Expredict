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
    res = call_api(url, cred)
    page_id = res['json_data']['data'][0]['id']
    cred['page_id'] = page_id
    url2 = cred['endpoint_base'] + cred['page_id'] + '?fields=instagram_business_account&access_token=' + \
           parameters['access_token']
    return call_api(url2, cred)


# cred = get_credentials()
# res = get_facebook_pages(cred)
#
# print(res['json_data']['data'][0]['id'])

