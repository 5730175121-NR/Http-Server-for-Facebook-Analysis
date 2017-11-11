import requests
import json

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
    

fields = 'posts.since(-2 year){comments{message,permalink_url,from}}'
access = 'EAACEdEose0cBAPWWgPXvtsvZAOg7W3hM7E7vB0zGue5sXRbZAZAc9hJrWANkXR3aYb4QfSoPZC5S2cJdj3QIzCUZAN4LipgqdFIZBUVRZCIuiFPfGQIoTTCtP6AWx69RZB2rx3cEuaLht8u42ltHsFR9QMAWQdiGaiME6QMLZAZCbuZCYJm7QjWIPKXlA6UOH6ZAysoZD'
print(getDataFacebook(access, fields))
# getDataFacebook(access, fields)
