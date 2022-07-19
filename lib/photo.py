"""[summary]
    Handle Google Photo api

    - get credentials
    - create session
    - upload photo to album
"""

import urllib
import requests
import json
from lib.key import (
    channel_secret, channel_access_token, google_photo_album_id,
    google_photo_client_id, google_photo_client_secret,
    google_photo_access_token, google_photo_refresh_token
)
import google
from google.auth.transport.requests import AuthorizedSession
import logging
import os

# Needed to get credentials
GOOGLE_PHOTO_TOKEN_URI = "https://oauth2.googleapis.com/token"
GOOGLE_PHOTO_ALBUM_ID = google_photo_album_id
GOOGLE_PHOTO_CLIENT_ID = google_photo_client_id
GOOGLE_PHOTO_CLIENT_SECRET = google_photo_client_secret
GOOGLE_PHOTO_ACCESS_TOKEN = google_photo_access_token
GOOGLE_PHOTO_REFRESH_TOKEN = google_photo_refresh_token


class GooglePhotoUploader():
    """[summary]
    Handle google photo uploading
    Need environmental variable
    """

    def __init__(self, album_id=GOOGLE_PHOTO_ALBUM_ID):
        """[summary]
        Create credentials and session.
        """
        self.credentials_info = self.load_credential_info()
        self.credentials = self.get_credentials(self.credentials_info)
        self.session = self.get_session(self.credentials)

        self.album_id = GOOGLE_PHOTO_ALBUM_ID

    def load_credential_info(self):
        """[summary]    Load credential from environment parameter
        Returns:
            dict: credential information dict containing token, refresh_token, id , secret, token_uri
        """
        credentials_dict = {}
        credentials_dict['token'] = GOOGLE_PHOTO_ACCESS_TOKEN
        credentials_dict['refresh_token'] = GOOGLE_PHOTO_REFRESH_TOKEN
        credentials_dict['client_id'] = GOOGLE_PHOTO_CLIENT_ID
        credentials_dict['client_secret'] = GOOGLE_PHOTO_CLIENT_SECRET
        credentials_dict['token_uri'] = GOOGLE_PHOTO_TOKEN_URI
        return credentials_dict

    def get_credentials(self, credentials_dict):
        """[summary] Get credential from Google

        Args:
            credentials_dict ([type]): [description]

        Returns:
            [type]: [description]
        """

        credentials = google.oauth2.credentials.Credentials(
            credentials_dict['token'],
            refresh_token=credentials_dict['refresh_token'],
            token_uri=credentials_dict['token_uri'],
            client_id=credentials_dict['client_id'],
            client_secret=credentials_dict['client_secret']
        )

        # check if credentials is active
        if credentials.valid:
            print("This credentials is active till:", credentials.expiry)
            return credentials
        elif credentials.expired:
            print("Credentials is somehow expired!", credentials.expiry)
        else:
            print("Can not get credentials!")
        return None

    def get_session(self, credentials):
        """[summary] Get session from valid credentials

        Args:
            credentials ([type]): [description]

        Returns:
            [type]: [description]
        """

        if credentials and credentials.valid:
            session = AuthorizedSession(credentials)
        else:
            print("Please check credential information!")
            return None

        if session.verify:
            return session
        else:
            print("Something is wrong!")
            return None

    def manage_session(self):
        """Verify session status and update if needed
        """

        assert self.session, "No session created!"

        if self.session.verify:
            # session is OK
            return
        else:
            # reinit session
            self.credentials = self.get_credentials(self.credentials_info)
            self.session = self.get_session(self.credentials)

    def create_new_album(self, session, album_title):
        """ Create named album and return id
        Args:
            session ([type]): session
            album_title ([type]): 

        Returns:
            string: album_id
        """
        create_album_body = json.dumps({"album": {"title": album_title}})
        # print(create_album_body)
        resp = session.post(
            'https://photoslibrary.googleapis.com/v1/albums', create_album_body).json()

        logging.debug("Server response: {}".format(resp))

        if "id" in resp:
            logging.info(
                "Uploading into NEW photo album -- \'{0}\'".format(album_title))
            return resp['id']
        else:
            logging.error("Could not find or create photo album '\{0}\'. Server Response: {1}".format(
                album_title, resp))
            return None

    def upload_image_to_album(self, raw_image, image_name=None):
        """[summary]
        Upload raw image
        Args:
            raw_image (bytes): image to be uploaded
            image_name ([string], optional): image name. Defaults to None.
        """
        if not image_name:
            image_name = "no_name"
        session = self.session
        album_id = self.album_id

        # start session
        session.headers["Content-type"] = "application/octet-stream"
        session.headers["X-Goog-Upload-Protocol"] = "raw"

        session.headers["X-Goog-Upload-File-Name"] = os.path.basename(
            image_name)

        logging.info("Uploading photo -- \'{}\'".format(image_name))

        # upload token
        upload_token = session.post(
            'https://photoslibrary.googleapis.com/v1/uploads', raw_image)

        # upload
        if (upload_token.status_code == 200) and (upload_token.content):

            create_body = json.dumps({"albumId": album_id, "newMediaItems": [
                {"description": "", "simpleMediaItem": {"uploadToken": upload_token.content.decode()}}]}, indent=4)

            resp = session.post(
                'https://photoslibrary.googleapis.com/v1/mediaItems:batchCreate', create_body).json()

            logging.debug("Server response: {}".format(resp))

            if "newMediaItemResults" in resp:
                status = resp["newMediaItemResults"][0]["status"]
                if status.get("code") and (status.get("code") > 0):
                    logging.error("Could not add \'{0}\' to library -- {1}".format(
                        os.path.basename(image_name), status["message"]))
                else:
                    logging.info("Added \'{}\' to library and album \'{}\' ".format(
                        os.path.basename(image_name), album_id))
            else:
                logging.error("Could not add \'{0}\' to library. Server Response -- {1}".format(
                    os.path.basename(image_name), resp))

        else:
            logging.error("Could not upload \'{0}\'. Server Response - {1}".format(
                os.path.basename(image_name), upload_token))

        try:
            del(session.headers["Content-type"])
            del(session.headers["X-Goog-Upload-Protocol"])
            del(session.headers["X-Goog-Upload-File-Name"])
        except KeyError:
            pass


def get_photo_data(msg_id):
    # LINE から画像を取得
    url = 'https://api.line.me/v2/bot/message/' + msg_id + '/content'
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        'Authorization': 'Bearer ' + channel_access_token,
    }
    request = urllib.request.Request(url,
                                     method='GET',
                                     headers=headers)
    img_data = None
    with urllib.request.urlopen(request) as response:
        img_data = response.read()

    return img_data
