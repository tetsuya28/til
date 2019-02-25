## docker-compose起動
* `./docker`の中の`docker-compose.yml`を使用

## 新規データベース作成

```MySQL
CREATE DATABASE <DATABASE> CHARACTER SET utf8;
```

## 新規テーブル作成
* text型にはUNIQUE KEYは付けられない

```MySQL
create table <DATABASE>.<TABLE>(id int not null primary key auto_increment,article_id int not null unique, article_url text not null, article_title char(255) not null)
```

## Created_at, Updated_at
* MySQL5.6以上ではON UPDATEオプションを付けたら自動で日付を更新してくれる

```MySQL
updated_at datetime not null DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```