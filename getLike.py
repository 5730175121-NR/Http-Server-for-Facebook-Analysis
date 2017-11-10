import requests
import json
import operator

since = input()

ACCESS_TOKEN = "EAACEdEose0cBAALDWCOdcp046zzhmXHd6KZClQi2BmJSfuCZBAOSL137MyIelISGenyrhVHMKbFcx2GfZAEiRWZA10aiSnoZAZAtwrnMI93sIB2Srqw8U6XqyHlzC8fbO7l99UFyOoxzhbSB9ZCs65N1GPBbOzZChTh0ta8kcmUml5b3tRE6oXE5mz5Q3lYZCMdgZD"
base_url = 'https://graph.facebook.com/v2.10/me'
fields = 'posts.since(%s){created_time,likes{name}}' % (since)
url = '%s?fields=%s&access_token=%s' % (base_url,fields,ACCESS_TOKEN)
content = requests.get(url).json()
list_of_like = []
list_of_feed = [f for f in content['posts']['data']]

while True:
    for f in list_of_feed:
        if 'likes' in f:
            list_of_like += [(ll['name'],f['id']) for ll in f['likes']['data']]
            f_content = {}
            if 'next' in f['likes']['paging']:
                url = f['likes']['paging']['next']
            else:
                url = ''
            while url != '':
                print('Getting next likes of '+f['id'])
                f_content = requests.get(url).json()
                list_of_like += [(ll['name'],f['id']) for ll in f_content['data']]
                if 'next' not in f_content['paging']:
                    url = ''
                else:
                    url = f_content['paging']['next']
                print(url)
    if 'posts' in content:
        if 'paging' not in content['posts'] or 'next' not in content['posts']['paging']:
            break
        url = content['posts']['paging']['next']
    elif 'data' in content:
        if 'paging' not in content:
            break
        if 'next' not in content['paging']:
            break
        url = content['paging']['next']
    print('Getting next feed')
    content = requests.get(url).json()
    list_of_feed = [f for f in content['data']]

count_of_like = {}

for l in list_of_like:
    if l[0] not in count_of_like:
        count_of_like[l[0]] = 1
    else:
        count_of_like[l[0]] += 1

count_of_like = sorted(count_of_like.items(), key=operator.itemgetter(1), reverse=True)

f=open(since,'w')

for x in count_of_like:
    f.write(x[0] + ": " + str(x[1]) + '\n')
f.close()