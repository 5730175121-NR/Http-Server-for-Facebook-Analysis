import requests
import json

def query_spliter(querys):
    query_dict = {}
    query_list = querys.split('&')
    for query in query_list:
        temp = query.split('=')
        query_dict[temp[0]] = temp[1].split(',')
    return query_dict

def getData(access_token, fields):
    base_url = 'https://graph.facebook.com/v2.10/me'
    url = '%s?fields=%s&access_token=%s' % (base_url,fields,access_token)
    content = requests.get(url).json()
    list_of_data = []
    try:
        list_of_data = [data for data in content['posts']['data']]
    except:
        print('error : please check ur access token!')
        return json.dumps(content)

    next_page_url = ''
    if 'paging' in content['posts']:
        if 'next' in content['posts']['paging']:
            next_page_url = content['posts']['paging']['next']
    
    while next_page_url != '':
        content = requests.get(next_page_url).json()
        list_of_data += [data for data in content['data']]
        if 'paging' in content:
            if 'next' in content['paging']:
                next_page_url = content['paging']['next']
        else:
            next_page_url = ''
    
    return list_of_data

def top_comments(access_token,since = '', top = ''):
    fields = 'posts{comments{from}}'
    if since != '':
        fields = 'posts.since(%s){comments{from}}' % (since)
    data = getData(access_token, fields)
    

