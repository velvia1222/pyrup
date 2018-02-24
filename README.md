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
