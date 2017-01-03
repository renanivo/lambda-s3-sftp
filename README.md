λ S3 to SFTP
============

Send an S3 file, whenever it is uploaded, to a remote server using SFTP

Deployment
----------

1. If you are using a private key to connect to SFTP, edit `main.py` and put its value inside the `PRIVATE_KEY` var
2. `make package`
3. Upload `package.zip` to AWS Lambda (on [console](http://docs.aws.amazon.com/lambda/latest/dg/get-started-create-function.html) or [command line](http://docs.aws.amazon.com/lambda/latest/dg/vpc-ec-upload-deployment-pkg.html))

Supported Events
----------------

* S3 PUT

Function Environment Vars
-------------------------

| Name             | Description                                                           | Required                                                                                 |
|------------------|-----------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| SSH_HOST         | SSH server name or ip address                                         | Yes                                                                                      |
| SSH_PORT         | SSH server port                                                       | Not (default: 22)                                                                        |
| SSH_DIR          | Directory where the uploaded files should be placed in the SSH server | No (default: SFTP home folder)                                                           |
| SSH_USERNAME     | SSH username for the connection                                       | Yes                                                                                      |
| SSH_PASSWORD     | SSH server password                                                   | Not (default: `None`)                                                                    |


Caveats
-------

This function does not replicates the S3 directory structure, it just copies every file uploaded to S3 to the `SSH_DIR` in the `SSH_HOST`.
