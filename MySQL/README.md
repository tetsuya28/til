## docker-compose起動
* `./docker`の中の`docker-compose.yml`を使用

## 新規データベース作成

```
CREATE DATABASE <DATABASE> CHARACTER SET utf8;
```

## 新規テーブル作成
* text型にはUNIQUE KEYは付けられない

```
create table <DATABASE>.<TABLE>(id int not null primary key auto_increment,article_id int not null unique, article_url text not null, article_title char(255) not null)
```