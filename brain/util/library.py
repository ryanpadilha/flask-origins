import os
import base64
import boto3
import pytz

from flask import request
from boto3.s3.transfer import S3Transfer
from uuid import uuid4
from werkzeug.utils import secure_filename
from flask_login import current_user
from dateutil.tz import tzlocal
from datetime import datetime


def user_logged_in():
    return current_user.name if current_user is not None else 'REST-API'


def current_timestamp_tz():
    now = datetime.now().replace(tzinfo=tzlocal())
    return now.astimezone(pytz.timezone('America/Sao_Paulo'))


def current_request_ip():
    if 'X-Forwarded-For' in request.headers:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
    else:
        remote_addr = request.remote_addr or 'untrackable'

    return remote_addr


def generate_secret_key():
    """
        Return a random URL-safe text string, in Base64 encoding.
        The string has *nbytes* random bytes.

    :return: secret key
    """
    token = os.urandom(32)
    key = base64.urlsafe_b64encode(token).rstrip(b'=').decode('ascii')
    return key


AWS_REGION = 'sa-east-1'
S3_LOCATION = 'https://s3-sa-east-1.amazonaws.com/'
S3_KEY = ''
S3_SECRET = ''
S3_UPLOAD_DIRECTORY = 'uploads'
S3_BUCKET = ''


def s3_upload(source_file, file_name, upload_dir=None, acl='public-read'):
    """ Uploads WTForm File Object to Amazon S3
        Expects following app.config attributes to be set:
            S3_KEY              :   S3 API Key
            S3_SECRET           :   S3 Secret Key
            S3_BUCKET           :   What bucket to upload to
            S3_UPLOAD_DIRECTORY :   Which S3 Directory.
        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.
    """

    if upload_dir is None:
        upload_dir = S3_UPLOAD_DIRECTORY

    source_filename = secure_filename(source_file.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension

    # Connect to S3 and upload file.
    conn = boto3.client('s3', region_name=AWS_REGION,
                        aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    APP_DIR = os.path.abspath(os.curdir)
    DEST = APP_DIR + '/brain/static/uploads/images/' + file_name

    transfer = S3Transfer(conn)
    transfer.upload_file(DEST, S3_BUCKET, destination_filename)

    # sml = b.new_key("/".join([upload_dir, destination_filename]))
    # sml.set_contents_from_string(source_file.data.read())
    # sml.set_acl(acl)

    return destination_filename
