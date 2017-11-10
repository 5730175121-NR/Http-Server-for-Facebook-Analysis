import requests
import json
import operator

def getComments(token, since):
    ACCESS_TOKEN = token
    base_url = 'https://graph.facebook.com/v2.10/me'
    fields = 'posts.since(%s){comments{message,permalink_url,from}}' % (since)
    url = '%s?fields=%s&access_token=%s' % (base_url,fields,ACCESS_TOKEN)
    content = requests.get(url).json()
    try:
        list_of_posts = [post for post in content['posts']['data']]
    except:
        return json.dumps(content)
    list_of_comments = []
    count_friend_comments = {}

    while True:
        for post in list_of_posts:
            if 'comments' in post:
                list_of_comments += [(comment['from']['id'], comment['from']['name'])for comment in post['comments']['data']]
                next_page_of_comment_url = ''
                next_page_of_comment = {}
                if 'next' in post['comments']['paging']:
                    next_page_of_comment_url = post['comments']['paging']['next'] 
                while next_page_of_comment_url != '':
                    next_page_of_comment = requests.get(next_page_of_comment_url).json()
                    list_of_comments += [(comment['from']['id'], comment['from']['name']) for comment in post['data']['comments']]
                    if 'next' in next_page_of_comment['paging']:
                        next_page_of_comment_url = next_page_of_comment['paging']['next']
                    else:
                        next_page_of_comment_url = ''
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
        content = requests.get(url).json()
        list_of_posts = [post for post in content['data']]

    count_friend_comments = {}
    friend_comments_name = {}

    for friend_comments in list_of_comments:
        if friend_comments[0] not in count_friend_comments:
            count_friend_comments[friend_comments[0]] = 0
            friend_comments_name[friend_comments[0]] = friend_comments[1]
        else:
            count_friend_comments[friend_comments[0]] += 1

    count_friend_comments = sorted(count_friend_comments.items(), key=operator.itemgetter(1), reverse=True)

    jsonDict = {}

    list_of_friends = []

    pic_link = ''

    for element in count_friend_comments:
        pic_link = 'https://graph.facebook.com/v2.10/%s/picture' % (element[0])
        list_of_friends.append({'id' : element[0], 'name': friend_comments_name[element[0]], 'comments' : element[1], 'pic' : pic_link})
    
    jsonDict['friends'] = list_of_friends

    return json.dumps(jsonDict)
