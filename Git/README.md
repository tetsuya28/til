## Gitのコミットメッセージに絵文字を追加する

* `.gitmessage_with_emoji.txt`をcloneして以下のコマンドでconfigに設定

```bash
git config --global commit.template .gitmessage_with_emoji.txt
```

* 後は`git commit`したらテンプレートメッセージも表示されるのでコミットするだけ

#### 参考サイト
* [Emojiで楽しく綺麗なコミットを手に入れる](https://goodpatch.com/blog/beautiful-commits-with-emojis/)