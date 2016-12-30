import os

import boto3
import paramiko


def lambda_handler(event, context):
    print 'Request ID: {}'.format(context.aws_request_id)

    ssh_host = os.environ['SSH_HOST']
    ssh_dir = os.environ.get['SSH_DIR']
    ssh_port = os.environ.get('SSH_PORT', 22)
    ssh_password = os.environ.get('SSH_PASSWORD')
    key_filename = os.environ.get('SSH_KEY_FILENAME', 'key.pem')

    if not os.path.isfile(key_filename):
        key_filename = None

    sftp, ssh = connect_to_SFTP(
        hostname=ssh_host,
        port=ssh_port,
        password=ssh_password,
        key_filename=key_filename
    )
    s3 = boto3.client('s3')

    try:
        for record in event['Records']:
            uploaded = record['s3']
            filename = uploaded['object']['key'].split('/')[-1]
            remote_dest = '{path}/{filename}'.format(path=ssh_dir,
                                                     filename=filename)

            transfer_file(
                s3_client=s3,
                bucket=uploaded['bucket']['name'],
                key=uploaded['object']['key'],
                sftp_client=sftp,
                sftp_dest=remote_dest
            )
    except Exception as e:
        print 'Could not upload file to SFTP. Error: {}'.format(e)

    else:
        print 'S3 file uploaded to SFTP successfully'

    finally:
        sftp.close()
        ssh.close()


def connect_to_SFTP(hostname, port, password, key_filename):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=hostname,
        port=port,
        password=password,
        key_filename=key_filename
    )
    sftp = ssh.open_sftp()

    return sftp, ssh


def transfer_file(self, s3_client, bucket, key, sftp_client, sftp_dest):
    """
    Download file from S3 and upload to SFTP
    """
    with sftp_client.file(sftp_dest, 'w') as sftp_file:
        s3_client.download_fileobj(
            Bucket=bucket,
            Key=key,
            FileObj=sftp_file
        )
