def query_spliter(querys):
    query_dict = {}
    query_list = querys.split('&')
    for query in query_list:
        temp = query.split('=')
        query_dict[temp[0]] = temp[1].split(',')
    return query_dict

