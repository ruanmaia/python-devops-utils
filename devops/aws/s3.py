import boto3
from botocore.exceptions import ClientError

import sys

from tqdm import tqdm
from loguru import logger
from pathlib import Path


class S3_DevOps_Utils:
    
    __client = None

    def __init__(self, session):
        self.__client = session.client('s3')

    @property
    def client(self):
        self.__client

    def sync(
        self, 
        local_path, 
        bucket_name,
        show_progress=True,
        dry_run=False
    ):
        files_to_sync = tuple(f for f in Path(local_path).glob('**/*') if not f.is_dir())
        total_files = len(files_to_sync)

        try:
            for i, f in enumerate(files_to_sync, 1):
                if not dry_run:
                    file_key = str(f).replace(local_path, '').lstrip('/')
                    self.__client.upload_file(str(f), bucket_name, file_key)
                if show_progress:
                    logger.opt(colors=True).info('<yellow>{:.2%}</yellow> -> {}', i/total_files, str(f))
        except:
            logger.exception('What is going on?')

    def website_deploy(
        self,
        local_path,
        bucket_name,
        index_file='index.html',
        error_file=None,
        policy=None
    ):
        
        DEFAULT_POLICY='''
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": "arn:aws:s3:::__BUCKET_NAME__/*"
                }
            ]
        }
        '''

        try:
            
            self.__client.head_bucket(Bucket=bucket_name)
            logger.info('The requested bucket already exists. I will update its content based on this path:')
            logger.opt(colors=True).info('"<red>{}</red>"', local_path)

        except ClientError as e:
            
            if int(e.response['Error']['Code']) == 404:
                logger.info('The requested bucket doesn\'t exist! I will create one!')
                response = self.__client.create_bucket(
                    ACL='public-read',
                    Bucket=bucket_name
                )
                logger.info('Bucket "{}" successfully created!',response['Location'])
                logger.info('Now, I will update its content based on this path: "{}"', local_path)
            else:
                logger.error('Your AWS credentials doesn\'t seem to work!')
                sys.exit(1)

        except:
            logger.error('Your AWS credentials doesn\'t seem to work!')
            sys.exit(1)

        logger.info("Look to my progress:")
        self.sync(local_path, bucket_name, dry_run=True)

        logger.opt(colors=True).info('<green>100% - Syncronization completed!</green>')

        logger.info("I know, I'm awesome! So, let me turn this bucket into a website...")