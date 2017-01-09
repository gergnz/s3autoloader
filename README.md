# S3AutoLoader

Some dodgy python that watches a directory and uploads a file to S3.

This uses the inotify module in python, and the s3transfer boto3 helper to upload files to s3.

This will only create one event once the file is completely uploaded regardless of whether the S3transfer decides to do a multipart upload. It will also NOT generate a zero length event.

## Requirements
* Daemonize
* inotify
* boto3

### Installing Requirements
```bash
sudo pip install -r requirements.txt
```

## Configuration
Edit the file and set appropriately:
```python
PATH='/home/gregc/incoming'
BUCKET='gjcstuff'
REGION='ap-southeast-2'
PID='/var/run/s3autoloader.pid'
LOGLEVEL=logging.DEBUG
```
### PATH
This is the path of the directory to monitor.

### BUCKET
set the bucket

### REGION
set the region where the bucket lives

### PID
a location for the pid file

### LOGLEVEL
a python loglevel

## AWS IAM Policy Setup
I strongly suggest you use an EC2 IAM Role. This is the policy I used for testing:
```javascript
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1483952762000",
            "Effect": "Allow",
            "Action": [
                "s3:AbortMultipartUpload",
                "s3:ListMultipartUploadParts",
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:PutObjectVersionAcl"
            ],
            "Resource": [
                "arn:aws:s3:::gjcstuff/*"
            ]
        }
    ]
}
```

# TODO
Lots!
