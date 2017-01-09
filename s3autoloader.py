#!/usr/bin/env python3

from daemonize import Daemonize
from threading import Thread
from boto3.s3.transfer import S3Transfer
import inotify.adapters
import logging
import logging.handlers
import time
import boto3
import os
import sys

PATH='/home/gregc/incoming'
BUCKET='gjcstuff'
REGION='ap-southeast-2'
PID='/var/run/s3autoloader.pid'
LOGLEVEL=logging.DEBUG

log = logging.getLogger(__name__)

log.setLevel(LOGLEVEL)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

def s3_copy_file(filename):
    log.debug('uploading file '+filename+' from '+PATH+' to bucket '+BUCKET)
    try:
        client = boto3.client('s3', REGION)
        transfer = S3Transfer(client)
        transfer.upload_file(PATH+'/'+filename, BUCKET, filename)
        os.remove(PATH+'/'+filename)
    except:
        e = sys.exc_info()[0]
        log.critical('error uploading to S3: '+str(e))

def do_something():
    i = inotify.adapters.Inotify()
    i.add_watch(str.encode(PATH))
    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if type_names[0] == 'IN_CLOSE_WRITE':
                    log.debug('Recieved a new file '+bytes.decode(filename))
                    z = Thread(target=s3_copy_file, args=(bytes.decode(filename),))
                    z.start()
    finally:
        i.remove_watch(str.encode(PATH))

if __name__ == '__main__':
    pid=PID
    daemon = Daemonize(app="s3autoloader", pid=pid, action=do_something)
    daemon.start()
