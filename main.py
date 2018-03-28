import os
from StringIO import StringIO

import boto3
import paramiko

PRIVATE_KEY = ''


def lambda_handler(event, context):
    ssh_username = os.environ['SSH_USERNAME']
    ssh_host = os.environ['SSH_HOST']
    ssh_dir = os.environ['SSH_DIR']
    ssh_port = int(os.environ.get('SSH_PORT', 22))
    ssh_password = os.environ.get('SSH_PASSWORD')
    key_filename = os.environ.get('SSH_KEY_FILENAME', 'key.pem')

    pkey = None

    if PRIVATE_KEY:
        pkey = paramiko.RSAKey.from_private_key(StringIO(PRIVATE_KEY))

    if not os.path.isfile(key_filename):
        key_filename = None

    sftp, transport = connect_to_SFTP(
        hostname=ssh_host,
        port=ssh_port,
        username=ssh_username,
        password=ssh_password,
        pkey=pkey
    )
    s3 = boto3.client('s3')

    if ssh_dir:
        sftp.chdir(ssh_dir)

    with transport:
        for record in event['Records']:
            uploaded = record['s3']
            filename = uploaded['object']['key'].split('/')[-1]

            try:
                transfer_file(
                    s3_client=s3,
                    bucket=uploaded['bucket']['name'],
                    key=uploaded['object']['key'],
                    sftp_client=sftp,
                    sftp_dest=filename
                )
            except Exception:
                print 'Could not upload file to SFTP'
                raise

            else:
                print 'S3 file "{}" uploaded to SFTP successfully'.format(
                    uploaded['object']['key']
                )


def connect_to_SFTP(hostname, port, username, password, pkey):
    transport = paramiko.Transport((hostname, port))
    transport.connect(
        username=username,
        password=password,
        pkey=pkey
    )
    sftp = paramiko.SFTPClient.from_transport(transport)

    return sftp, transport


def transfer_file(s3_client, bucket, key, sftp_client, sftp_dest):
    """
    Download file from S3 and upload to SFTP
    """
    with sftp_client.file(sftp_dest, 'w') as sftp_file:
        s3_client.download_fileobj(
            Bucket=bucket,
            Key=key,
            Fileobj=sftp_file
        )
