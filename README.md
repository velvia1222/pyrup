# pyrup
ファイルアップローダー。約３TBまで格納可
- プラットフォーム：raspberry pi3
- WEBサーバー：nginx
- WEBコンテナ：uwsgi
- 言語：python3
- WEBフレームワーク：pyramid
- ORM：sqlalchemy
- DB：sqlite
- SSL：Let's Encrypt

## インストール
### raspbianのインストールと基本設定
- proto-outgoとほぼ同じのため省略

### aptを使用して必要なライブラリをインストール
```
sudo apt update
sudo apt install nginx python3-pip
```

### pyrupインストール
```
cd /usr/local/src
sudo git clone https://github.com/velvia1222/pyrup.git
sudo python3 setup.py install
```

### ファイアウォール設定
```
sudo ufw allow proto tcp from any to any port 443
```

### ルータのポート開放
- 443ポートを開放し、raspberry piにフォワードする

### Let's Encryptインストール
```
sudo curl https://dl.eff.org/certbot-auto -o /usr/local/bin/certbot-auto
sudo ./certbot-auto certonly --standalone
```

### uwsgi起動
```
sudo uwsgi --ini-paste /usr/local/src/pyrup/production.ini
```

### Screenshots
- ログイン画面
<img width="320" src="https://user-images.githubusercontent.com/20614266/36626045-90ae73ea-196e-11e8-9e25-5210788833c9.png">
- サイト一覧
<img width="292" alt="2018-02-24 10 49 03" src="https://user-images.githubusercontent.com/20614266/36626079-869a6fac-196f-11e8-9ddb-80babea95206.png">
- ページ一覧
<img width="270" alt="2018-02-24 10 56 57" src="https://user-images.githubusercontent.com/20614266/36626086-b5e6f67c-196f-11e8-9146-4263c7a977b8.png">
- コンテンツ一覧
<img width="602" alt="2018-02-24 10 57 27" src="https://user-images.githubusercontent.com/20614266/36626087-cf8bab4a-196f-11e8-9e43-be73cf388939.png">
<img width="510" alt="2018-02-24 10 57 43" src="https://user-images.githubusercontent.com/20614266/36626103-ef52f46a-196f-11e8-90cf-2aee58d3c2e0.png">
- サイト追加
<img width="242" alt="2018-02-24 10 58 07" src="https://user-images.githubusercontent.com/20614266/36626114-0d7a019a-1970-11e8-8eab-64d0d70c6c13.png">
- ページ追加
<img width="243" alt="2018-02-24 10 58 30" src="https://user-images.githubusercontent.com/20614266/36626119-1d9b1c76-1970-11e8-841d-dec5973b81fc.png">
- コンテンツ追加
<img width="301" alt="2018-02-24 10 58 56" src="https://user-images.githubusercontent.com/20614266/36626123-2c9f6470-1970-11e8-8838-e22dc6b0eb8b.png">
