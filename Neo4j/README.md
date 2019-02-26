## GraphDB - Neo4j

### 使い方
* とりあえず`docker`の中の`docker-compose`から起動する

### TwitterからNeo4jにユーザデータ挿入
* .env.sample参考に
* バックグラウンドで起動するために以下のコマンド使用  

`nohup python get_twitter_user_data_to_neo4j.py &`
