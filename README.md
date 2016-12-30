λ S3 to SFTP
============

Send an S3 file, whenever it is uploaded, to a remote server using SFTP

Deployment
----------

* `make package`
* Upload `package.zip` to AWS Lambda (on [console](http://docs.aws.amazon.com/lambda/latest/dg/get-started-create-function.html) or [command line](http://docs.aws.amazon.com/lambda/latest/dg/vpc-ec-upload-deployment-pkg.html))

Supported Events
----------------

* S3 PUT

Function Environment Vars
-------------------------

| Name             | Description                                                           | Required                                                                                |
|------------------|-----------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| SSH_HOST         | SSH server name or ip address                                         | Yes                                                                                     |
| SSH_PORT         | SSH server port                                                       | Not (default 22)                                                                        |
| SSH_DIR          | Directory where the uploaded files should be placed in the SSH server | Yes                                                                                     |
| SSH_PASSORD      | SSH server password                                                   | Not (default `None`)                                                                    |
| SSH_KEY_FILENAME | Path to ssh key file                                                  | Not (default `key.pem` if `key.pem` is included in the deployment package, else `None`) |
