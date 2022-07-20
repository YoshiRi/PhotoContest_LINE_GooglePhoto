# LINE Bot for Photo Contest


forked from https://github.com/ichiroex/linebot-photocontest

[参考にしたページ](https://qiita.com/ichiroex/items/5dd6ec89112f88f87159)

## Requirements

- python 3.8 later
- LINE BOT API
- Google Photo API

## Getting started


### Python dependencies

```
pip install -r requirements.txt
```

### Set environmental variable

In the your environment following environmental variable should be set

```
LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
GOOGLE_PHOTO_CLIENT_ID=YOUR_GOOGLE_PHOTO_CLIENT_ID
GOOGLE_PHOTO_CLIENT_SECRET=YOUR_GOOGLE_PHOTO_CLIENT_SECRET
GOOGLE_PHOTO_ALBUM_ID=YOUR_GOOGLE_PHOTO_ALBUM_ID
GOOGLE_PHOTO_REFRESH_TOKEN=YOUR_GOOGLE_PHOTO_ACCESS_TOKEN
GOOGLE_PHOTO_REFRESH_TOKEN=YOUR_GOOGLE_PHOTO_REFRESH_TOKEN
DATABASE_URI=YOUR_DATABASE_URI
```

If you want to run in heroku, use heroku config:set command.

```
heroku config:set VAR=YOUR_VAR
```

You can use .env file and run following commands to automatically set config.

```sh
# linux
heroku config:set $(cat .env)

# windows
FOR /F "usebackq" %i IN (`type .env`) DO heroku config:set %i
```




## Usage
```
$ python main.py
```

## Deploy
```
# To github repository
$ git push origin master

# To heroku server
$ git push heroku master
```

## How to use Google Photos AP

### AUTH CODEを取得する




## Database uri sample

```
DATABASE_URI=sqlite:///db/photocontest.db
```