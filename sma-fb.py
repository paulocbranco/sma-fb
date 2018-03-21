import facebook
import datetime as dt
import os
import requests
import json

APP_ID = '385325071930437'
APP_SECRET = '58debbbffb6c621e6c5924eed8baab5a'

POST_FIELDS = 'created_time,caption,description,from,link,message,message_tags,object_id,parent_id,permalink_url,picture,' \
              'place,properties,shares,source,status_type,story,to,type,with_tags'

COMM_FIELDS = 'created_time,caption,description,from,link,message,message_tags,object_id,parent_id,permalink_url,' \
              'place,properties,shares,source,status_type,story,to,type,with_tags'


def main():
    # https://www.facebook.com/russiaFIFA2018/
    get_page_info('1726708387545466')
    # https://www.facebook.com/fifaworldcup/
    get_page_info('606721589343692')


def get_token():
    response = requests.get(
        'https://graph.facebook.com/oauth/access_token?client_id=385325071930437&client_secret=58debbbffb6c621e6c5924eed8baab5a&grant_type=client_credentials')
    if response.status_code == 200:
        json_data = json.loads(response.text)
        return json_data['access_token']
    else:
        return ""


def get_api():
    access_token = APP_ID + '|' + APP_SECRET
    # access_token = get_token()
    return facebook.GraphAPI(access_token=access_token, version='2.7')


def get_page_info(page_id):
    api = get_api()
    info = api.get_object(page_id)

    print('Procurar dados da página:', info['name'])

    likes = get_page_objects('likes', object_id=page_id, api=api)
    feeds = get_page_objects('feed', object_id=page_id, api=api, fields=POST_FIELDS)
    posts = get_page_objects('posts', object_id=page_id, api=api, fields=POST_FIELDS)

    page = {
        "page": info,
        "likes": {
            "count": len(likes),
            "data": likes
        },
        "feed": {
            "count": len(feeds),
            "data": feeds
        },
        "posts": {
            "count": len(posts),
            "data": posts
        }
    }

    write_nodes(page, get_filename(info['name']), 'json')


def get_page_objects(node_type='posts', object_id=None, api=None, next=None, nodes=None,
                     fields='created_time, caption, from, message, name, shares, story', counter=0):
    counter += 1
    if counter == 1: print('>' + node_type + '<', flush=True)
    print('iteração nº>', counter, sep='', end='\r', flush=True)

    if api is None:
        api = get_api()

    if next is None:
        result = api.get_connections(object_id, connection_name=node_type, fields=fields, limit=100)
    else:
        result = requests.get(next).json()

    if nodes is None:
        data = []
    else:
        data = nodes

    if len(result['data']) > 0:
        if node_type == 'posts' or node_type == 'feed' or node_type == 'comments':
            # procura comments
            for obj in result['data']:
                id = obj['id']
                comments = get_page_objects('comments', object_id=id, api=api, nodes=None, fields=COMM_FIELDS,
                                            counter=counter)
                comments = {
                    "count": len(comments),
                    "data": comments
                }
                obj['comments'] = comments
                data.append(obj)
                counter += 1
            # fim de procurar comments
        else:
            data.extend(result['data'])

        if 'next' in result['paging']:
            next = result['paging']['next']
            data.extend(get_page_objects(node_type, api=api, next=next, nodes=data, counter=counter))

    return data


def get_filename(name):
    d = dt.datetime.now()
    day = '{0}-{1:0>2}-{2:0>2}'.format(d.year, d.month, d.day)
    return '{}_{}'.format(name, day)


def write_nodes(nodes, filename, type='csv'):
    filename = filename + '.' + type
    with open(filename, 'w') as f:
        json.dump(nodes, f)


def makedir(name):
    dirname = 'facebook/{}/'.format(name)
    os.makedirs(os.path.dirname(dirname), exist_ok=True)
    return dirname


if __name__ == "__main__":
    main()
