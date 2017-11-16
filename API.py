import requests
import json
import operator
import time

def navigator(path, querys):
    query_dict = query_spliter(querys)
    since = ''
    top = ''
    if 'since' in query_dict:
        since = query_dict['since']
    if 'top' in query_dict:
        top = query_dict['top']

    if path == '/comments':
        return top_comments(query_dict['access_token'], since=since, top=top)
    elif path == '/likes':
        return top_likes(query_dict['access_token'], since=since, top=top)
    elif path == '/reactions':
        return top_reactions(query_dict['access_token'], since=since, top=top)
    else:
        return ['none']

def query_spliter(querys):
    query_dict = {}
    query_list = querys.split('&')
    for query in query_list:
        temp = query.split('=')
        query_dict[temp[0]] = temp[1]
    return query_dict

def getData(access_token, fields):
    start = time.time()
    base_url = 'https://graph.facebook.com/v2.10/me'
    url = '%s?fields=%s&access_token=%s' % (base_url,fields,access_token)
    content = requests.get(url).json()
    list_of_data = []
    try:
        list_of_data = [data for data in content['posts']['data']]
    except:
        print('error : please check ur access token!')
        return content

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
    end = time.time()
    print('fetching data finished in : %s secs' % str('%.3f' % (end - start)))
    return list_of_data

def top_comments(access_token,since = '', top = ''):
    dict_of_friends = {}
    dict_of_comments = {}
    fields = 'posts{comments{from}}'
    if since != '':
        fields = 'posts.since(%s){comments{from}}' % (since)
    list_of_posts = getData(access_token, fields)
    if 'error' in list_of_posts:
        return list_of_posts
    start = time.time()
    for post in list_of_posts:
        if 'comments' in post:
            for comment in post['comments']['data']:
                if comment['from']['id'] not in dict_of_friends:
                    dict_of_friends[comment['from']['id']] = comment['from']['name']
                    dict_of_comments[comment['from']['id']] = 1
                else:
                    dict_of_comments[comment['from']['id']] += 1
            next_page_of_comment = {}
            next_page_of_comment_url = ''
            if 'next' in post['comments']['paging']:
                next_page_of_comment_url = post['comments']['paging']['next'] 
            while next_page_of_comment_url != '':
                next_page_of_comment = requests.get(next_page_of_comment_url).json()
                for comment in next_page_of_comment['data']:
                    if comment['from']['id'] not in dict_of_friends:
                        dict_of_friends[comment['from']['id']] = comment['from']['name']
                        dict_of_comments[comment['from']['id']] = 1
                    else:
                        dict_of_comments[comment['from']['id']] += 1
                if 'paging' not in next_page_of_comment:
                    next_page_of_comment_url = ''
                if 'next' in next_page_of_comment['paging']:
                    next_page_of_comment_url = next_page_of_comment['paging']['next']
                else:
                    next_page_of_comment_url = ''
    dict_of_comments = sorted(dict_of_comments.items(), key=operator.itemgetter(1), reverse=True)

    list_of_friends = []
    pic_link = ''
    top_count = 0
    if top != '':
        top = int(top)
    else:
        top = -1

    for friend in dict_of_comments:
        pic_link = 'https://graph.facebook.com/v2.10/%s/picture' % (friend[0])
        list_of_friends.append({'id' : friend[0], 'name': dict_of_friends[friend[0]], 'comments' : friend[1], 'pic' : pic_link})
        top_count += 1
        if top_count == top:
            break
    end = time.time()
    print('top comments finished in : %s secs' % str('%.3f' % (end - start)))
    return list_of_friends
    
def top_likes(access_token,since = '', top = ''):
    dict_of_friends = {}
    dict_of_likes = {}
    fields = 'posts{likes{id,name,pic}}'
    if since != '':
        fields = 'posts.since(%s){likes{id,name,pic}}' % since
    list_of_posts = getData(access_token, fields)
    if 'error' in list_of_posts:
        return list_of_posts
    start = time.time()
    for post in list_of_posts:
        if 'likes' in post:
            for like in post['likes']['data']:
                if like['id'] not in dict_of_friends:
                    dict_of_friends[like['id']] = [like['name'], like['pic']]
                    dict_of_likes[like['id']] = 1
                else:
                    dict_of_likes[like['id']] += 1
            next_page_of_like = {}
            next_page_of_like_url = ''
            if 'next' in post['likes']['paging']:
                next_page_of_like_url = post['likes']['paging']['next']
            while (next_page_of_like_url != ''):
                next_page_of_like = requests.get(next_page_of_like_url).json()
                for like in next_page_of_like['data']:
                    if like['id'] not in dict_of_friends:
                        dict_of_friends[like['id']] = [like['name'], like['pic']]
                        dict_of_likes[like['id']] = 1
                    else:
                        dict_of_likes[like['id']] += 1
                if 'paging' not in next_page_of_like:
                    next_page_of_like_url = ''
                if 'next' in next_page_of_like['paging']:
                    next_page_of_like_url = next_page_of_like['paging']['next']
                else:
                    next_page_of_like_url = ''
    
    dict_of_likes = sorted(dict_of_likes.items(), key=operator.itemgetter(1), reverse=True)

    list_of_friends = []
    top_count = 0
    if top != '':
        top = int(top)
    else:
        top = -1
    for friend in dict_of_likes:
        list_of_friends.append({'id' : friend[0], 'name': dict_of_friends[friend[0]][0], 'likes' : friend[1], 'pic' : dict_of_friends[friend[0]][1]})
        top_count += 1
        if top_count == top:
            break
    end = time.time()
    print('top likes finished in : %s secs' % str('%.3f' % (end - start)))
    return list_of_friends

def top_reactions(access_token,since = '', top = ''):
    dict_of_friends = {}
    dict_of_total = {}
    dict_of_reactions = {}
    fields = 'posts{reactions{id,name,pic,type}}'
    if since != '':
        fields = 'posts.since(%s){reactions{id,name,pic,type}}' % since
    list_of_posts = getData(access_token, fields)
    if 'error' in list_of_posts:
        return list_of_posts
    start = time.time()
    for post in list_of_posts:
        if 'reactions' in post:
            for reaction in post['reactions']['data']:
                if reaction['id'] not in dict_of_friends:
                    dict_of_friends[reaction['id']] = [reaction['name'], reaction['pic']]
                    dict_of_reactions[reaction['id']] = { 'LIKE' :  0,'LOVE' :  0,'WOW' :  0,'HAHA' :  0,'SAD' :  0,'ANGRY' :  0,'THANKFUL' :  0}
                    dict_of_total[reaction['id']] = 0
                dict_of_reactions[reaction['id']][reaction['type']] += 1
                dict_of_total[reaction['id']] += 1
            next_page_of_reaction = {}
            next_page_of_reaction_url = ''
            if 'next' in post['reactions']['paging']:
                next_page_of_reaction_url = post['reactions']['paging']['next']
            while (next_page_of_reaction_url != ''):
                next_page_of_reaction = requests.get(next_page_of_reaction_url).json()
                for reaction in next_page_of_reaction['data']:
                    if reaction['id'] not in dict_of_friends:
                        dict_of_friends[reaction['id']] = [reaction['name'], reaction['pic']]
                        dict_of_reactions[reaction['id']] = { 'LIKE' :  0,'LOVE' :  0,'WOW' :  0,'HAHA' :  0,'SAD' :  0,'ANGRY' :  0,'THANKFUL' :  0}
                        dict_of_total[reaction['id']] = 0
                    dict_of_reactions[reaction['id']][reaction['type']] += 1
                    dict_of_total[reaction['id']] += 1
                if 'paging' not in next_page_of_reaction:
                    next_page_of_reaction_url = ''
                if 'next' in next_page_of_reaction['paging']:
                    next_page_of_reaction_url = next_page_of_reaction['paging']['next']
                else:
                    next_page_of_reaction_url = ''
    
    dict_of_total = sorted(dict_of_total.items(), key=operator.itemgetter(1), reverse=True)

    list_of_friends = []
    top_count = 0
    if top != '':
        top = int(top)
    else:
        top = -1
    for friend in dict_of_total:
        user_id = friend[0]
        user_name = dict_of_friends[user_id][0]
        user_pic = dict_of_friends[user_id][1]
        user_total = friend[1]
        dict_reactions = dict_of_reactions[user_id]
        LIKE = dict_reactions['LIKE']
        LOVE = dict_reactions['LOVE'] 
        WOW = dict_reactions['WOW'] 
        HAHA = dict_reactions['HAHA'] 
        SAD = dict_reactions['SAD'] 
        ANGRY = dict_reactions['ANGRY'] 
        THANKFUL = dict_reactions['THANKFUL'] 
        list_of_friends.append({'id' : user_id, 'name': user_name, 'pic' : user_pic, 'LIKE' : LIKE, 'LOVE' : LOVE, 'WOW' : WOW, 'HAHA' : HAHA, 'SAD' : SAD, 'ANGRY' : ANGRY, 'THANKFUL' : THANKFUL, 'TOTAL' : user_total})
        top_count += 1
        if top_count == top:
            break
    end = time.time()
    print('top likes finished in : %s secs' % str('%.3f' % (end - start)))
    return list_of_friends

                
