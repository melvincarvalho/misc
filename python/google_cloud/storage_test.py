import oauth2client
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient import discovery, http
import argparse
import filecmp
import json
import tempfile
import logging
#import http

logging.basicConfig(filename='debug.log',level=logging.DEBUG)

#CLIENT_SECRETS_JSON_FILE = '/Users/nishant/Downloads/client_secret.json'
#CLIENT_SECRETS_JSON_FILE = '/Users/nishant/Downloads/test1-eceb571d111a.json'
CLIENT_SECRETS_JSON_FILE = '/Users/nishant/Downloads/test1-96d2ba747ad4.json'

def main(bucket, filename, gckey=None, readers=[], owners=[]):
    print('Uploading object..')
    if not gckey:
        gckey = filename
    resp = upload_object(bucket, filename, readers, owners, gckey)
    print(json.dumps(resp, indent=2))


def create_service():
    scopes = ['https://www.googleapis.com/auth/devstorage.read_write']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CLIENT_SECRETS_JSON_FILE, scopes)
    http_auth = credentials.authorize(Http())
    return discovery.build('storage', 'v1', http=http_auth)


def download_object(bucket, gckey, localfile):
    service = create_service()
    req = service.objects().get_media(
        bucket=bucket, object=gckey)
    x = req.execute()
    with open(localfile, 'wb') as f:
        f.write(x)

def download_large_object(bucket, gckey, localfile):
    service = create_service()
    req = service.objects().get_media(
        bucket=bucket, object=gckey)
    with open(localfile, 'wb') as f:
        downloader = http.MediaIoBaseDownload(f, request, chunksize=1024*1024)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print "Download %d%%." % int(status.progress() * 100)
    print "Download Complete!"

def upload_large_object(bucket, filename, gckey):
    service = create_service()
    body = {
        'name': gckey,
    }
    with open(filename, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket, body=body,
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            media_body=http.MediaIoBaseUpload(f, 'application/octet-stream')
        )
        resp = req.execute()



def upload_object(bucket, filename, readers, owners, gckey):
    service = create_service()

    # This is the request body as specified:
    # http://g.co/cloud/storage/docs/json_api/v1/objects/insert#request
    body = {
        #'name': filename,
        'name': gckey,
    }

    # If specified, create the access control objects and add them to the
    # request body
    if readers or owners:
        body['acl'] = []

    for r in readers:
        body['acl'].append({
            'entity': 'user-%s' % r,
            'role': 'READER',
            'email': r
        })
    for o in owners:
        body['acl'].append({
            'entity': 'user-%s' % o,
            'role': 'OWNER',
            'email': o
        })

    # Now insert them into the specified bucket as a media insertion.
    # http://g.co/dv/resources/api-libraries/documentation/storage/v1/python/latest/storage_v1.objects.html#insert
    with open(filename, 'rb') as f:
        req = service.objects().insert(
            bucket=bucket, body=body,
            # You can also just set media_body=filename, but for the sake of
            # demonstration, pass in the more generic file handle, which could
            # very well be a StringIO or similar.
            #media_body=http.MediaIoBaseUpload(f, 'application/octet-stream')
            media_body=filename
        )
        resp = req.execute()

    return resp
