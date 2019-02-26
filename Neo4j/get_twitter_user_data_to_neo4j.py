import os
import requests
import time
import json
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session
from sqlalchemy import create_engine
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client

# .envのロード
dotenv_path = ('.env')
load_dotenv(dotenv_path)

# Neo4j
neo4j_url = 'http://{}:{}@localhost:7474/db/data/'.format(os.environ['NEO4J_USER'], os.environ['NEO4J_PASSWORD'])
gdb = GraphDatabase(neo4j_url)

# MySQL接続
mysql_info = 'mysql+pymysql://' + os.environ['MYSQL_USER'] + ':' + os.environ['MYSQL_PASSWORD'] + '@' + os.environ['MYSQL_HOST'] + '/' + os.environ['MYSQL_DATABASE'] + '?charset=utf8mb4'
engine = create_engine(mysql_info, echo=False)

# Define
twitter_user_search_url = 'https://api.twitter.com/1.1/users/search.json'
twitter_user_friend_url = 'https://api.twitter.com/1.1/friends/list.json'
twitter_user_show_url = 'https://api.twitter.com/1.1/users/show.json'
slack_incoming_webhook = os.environ['SLACK_INCOMING_WEBHOOK_URL']
my_twitter_user_id = os.environ['MY_TWITTER_ID']


# Twitter認証
def get_twitter_access():
    twitter_client = OAuth1Session(
        os.environ['API_KEY'],
        os.environ['API_SECRET'],
        os.environ['ACCESS_TOKEN'],
        os.environ['ACCESS_SECRET']
    )
    return twitter_client


twitter = get_twitter_access()


# Slack Message
def post_message_slack(message):
    payload_dic = {
        "text": message,
        "channel": "#bot_room",
    }

    r = requests.post(slack_incoming_webhook, data=json.dumps(payload_dic))
    return r


# Human Label作成
human = gdb.labels.create('Human')


def insert_user_data_neo4j(user):
    u = gdb.nodes.create(user_id=user['id'], name=user['name'], followers=user['followers_count'],
                         friends=user['friends_count'])
    human.add(u)


def insert_friendship_data_neo4j(user_id, friend_id):
    x = gdb.query('match (p:Human {user_id: ' + str(user_id) + '}) return p', returns=client.Node)
    y = gdb.query('match (p:Human {user_id: ' + str(friend_id) + '}) return p', returns=client.Node)
    x[0][0].relationships.create('Follow', y[0][0])


def insert_user_data(user_info):
    ins = 'INSERT INTO user (user_id, name, screen_name, location, description, followers_count, friends_count, favourites_count, profile_background_image_url_https, profile_image_url_https) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    try:
        engine.execute(ins, user_info['id'], user_info['name'], user_info['screen_name'], user_info['location'],
                       user_info['description'], user_info['followers_count'], user_info['friends_count'],
                       user_info['favourites_count'], user_info['profile_background_image_url_https'],
                       user_info['profile_image_url_https'])
        # Neo4jにデータ挿入
        insert_user_data_neo4j(user_info)
    except Exception as e:
        print(user_info['name'])
        print(e.args)


def insert_friendship_data(user_id, friend_id):
    ins = 'INSERT INTO friendship(user_id, friend_id) VALUES (%s, %s)'
    try:
        engine.execute(ins, user_id, friend_id)
        # Neo4jにデータ挿入
        insert_friendship_data_neo4j(user_id, friend_id)
    except Exception as e:
        print(e.args)


def get_user_profile(user_id=my_twitter_user_id):
    response = twitter.get(twitter_user_show_url, params={'user_id': user_id})
    return response.json()


def get_friends_info(user_id, cursor=-1, users=[]):
    if len(users) == 0:
        print('Get Friends Data from Twitter')
        params = {
            'user_id': user_id,
            'cursor': cursor
        }

        try:
            response = twitter.get(twitter_user_friend_url, params=params)
        except Exception as e:
            print('Error')
            post_message_slack(e.args)

        if not 'users' in response.json() or not 'next_cursor' in response.json():
            post_message_slack(slack_incoming_webhook, response.json())
            print('Error')
            print(response.json())
            return False, False

        users = response.json()['users']
        cursor = response.json()['next_cursor']
    else:
        print('Use Local User Data')

    need_keys = ['id', 'name', 'screen_name', 'location', 'description', 'followers_count', 'friends_count',
                 'favourites_count', 'profile_background_image_url_https', 'profile_image_url_https']

    users_info = []
    for user in users:
        user_info = {}
        for key in need_keys:
            user_info[key] = user[key]
        users_info.append(user_info)
        # DBにデータ挿入
        insert_user_data(user_info)
        insert_friendship_data(user_id, user_info['id'])
    return users_info, cursor


def data_collection(user_name, user_id=my_twitter_user_id):
    post_message_slack('{}({})の作業開始'.format(user_name, user_id))
    # チェック済みのユーザか判定
    r = engine.execute('select * from checked_users where user_id = {}'.format(user_id)).first()
    if r is not None:
        post_message_slack('チェック済みのユーザ({})なのでスキップ'.format(user_id))
        return False

    next_cursor = -1
    while not next_cursor == 0:
        friends, next_cursor = get_friends_info(user_id=user_id, cursor=next_cursor)
        print('next_cursor: ', next_cursor)
        print('Start to Sleep(60)')
        print('-' * 33)
        time.sleep(60)

    engine.execute('insert into checked_users(user_id) values({})'.format(user_id))
    post_message_slack('{}の作業終了'.format(user_id))
    print('Finish')


def main(current_id=1):
    # DBの中身確認
    me = engine.execute('select * from user where name="' + os.environ['MY_TWITTER_NAME'] + '"').first()
    if me is None:
        print('最初に自分の取得')
        my_twitter_account = get_user_profile()
        print(my_twitter_account)
        insert_user_data(my_twitter_account)
        insert_user_data_neo4j(my_twitter_account)
    else:
        print('自分は存在する')
        data_collection(user_id=me['user_id'], user_name=me['name'])

    while True:
        target_user = engine.execute(
            "select * from user where description LIKE '%s' and id > %s" % ('%%' + os.environ['SEARCH_WORD'] + '%%', current_id)).first()

        if target_user is None:
            post_message_slack('探索終了。奇跡。')
            break

        data_collection(user_id=target_user['user_id'], user_name=target_user['name'])

if __name__ == "__main__":
    main()
