import facebook
import datetime as dt
from pandas.core.frame import DataFrame
import os
import requests
import json

APP_ID = 'xxxxxxxxxxxxxxxxxxxx'
APP_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxx'


def main():
    # colocar o id da página pretendida
    # procurar os ids das páginas aqui: https://lookup-id.com/
    search(query='1726708387545466')


def get_api():
    access_token = APP_ID + '|' + APP_SECRET
    return facebook.GraphAPI(access_token=access_token, version='2.7')


def search(query=None, raw_query=None, api=None, total=None, pagename=None):
    next_results = None

    try:
        if api is None:
            api = get_api()

        if pagename is None:
            name = api.get_object(query)['name']
        else:
            name = pagename

        if query is not None:
            print('Procurar posts da página {}({}) '.format(name, query))
            posts = api.get_connections(query, connection_name='posts',
                                        fields='caption,created_time,description,from,link,message,object_id,parent_id,permalink_url,picture,privacy,place,properties,shares,source,status_type,story,to,type,with_tags',
                                        limit='100')
        else:
            posts = requests.get(raw_query).json()

        if total is None:
            count = len(posts['data'])
        else:
            count = total + len(posts['data'])

        if 'next' in posts['paging']:
            next_results = posts['paging']['next']

        print('Posts encontrados:', count, end='\r')
        filename = makedir(name) + get_filename(name)
        write_posts(posts['data'], filename)
        write_posts(posts['data'], filename, 'json')
        if next_results is not None:
            search(raw_query=next_results, api=api, total=count, pagename=name)
        else:
            print('Total de posts encontrados:', count)

    except Exception as ex:
        print(ex)


def get_filename(name):
    d = dt.datetime.now()
    day = '{0}-{1:0>2}-{2:0>2}'.format(d.year, d.month, d.day)
    return '{}_{}'.format(name, day)


def write_posts(posts, filename, type='csv'):
    df = DataFrame(posts)
    filename = filename + '.' + type
    with open(filename, 'a') as f:
        if type == 'csv':
            df.to_csv(f, sep='\t', index=False, encoding='utf-8')
        else:
            for post in posts:
                json.dump(post, f)
                f.write('\n')


def makedir(name):
    dirname = 'facebook/{}/'.format(name)
    os.makedirs(os.path.dirname(dirname), exist_ok=True)
    return dirname


if __name__ == "__main__":
    main()
