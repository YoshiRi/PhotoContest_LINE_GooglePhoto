# LINE Bot for Photo Contest


## Requirements
- python 3.10

## Getting started

### Set environmental variable

```
$ export LINE_CHANNEL_SECRET=YOUR_LINE_CHANNEL_SECRET
$ export LINE_CHANNEL_ACCESS_TOKEN=YOUR_LINE_CHANNEL_ACCESS_TOKEN
$ export GOOGLE_PHOTO_CLIENT_ID=YOUR_GOOGLE_PHOTO_CLIENT_ID
$ export GOOGLE_PHOTO_CLIENT_SECRET=YOUR_GOOGLE_PHOTO_CLIENT_SECRET
$ export GOOGLE_PHOTO_ALBUM_ID=YOUR_GOOGLE_PHOTO_ALBUM_ID
$ export GOOGLE_PHOTO_REFRESH_TOKEN=YOUR_GOOGLE_PHOTO_ACCESS_TOKEN
$ export GOOGLE_PHOTO_REFRESH_TOKEN=YOUR_GOOGLE_PHOTO_REFRESH_TOKEN
$ export DATABASE_URI=YOUR_DATABASE_URI
$ pip install -r requirements.txt
```

or use .env file to  run

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

## How to use Google Photos API
### AUTH CODEを取得する（ブラウザで開く）


## Database uri sample

```
DATABASE_URI=sqlite:///db/photocontest.db
```