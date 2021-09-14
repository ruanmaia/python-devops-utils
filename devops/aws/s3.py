import boto3
from botocore.exceptions import ClientError

import sys
import hashlib
import re
import mimetypes

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
        if show_progress:
            logger.info("Starting syncronization process:")
            
        files_to_sync = tuple(f for f in Path(local_path).glob('**/*') if not f.is_dir())
        total_files = len(files_to_sync)

        try:
            
            for i, f in enumerate(files_to_sync, 1):
                if not dry_run:
                    
                    file_key = str(f).replace(local_path, '').lstrip('/')
                    mimetype = mimetypes.guess_type(file_key, strict=False)[0]

                    self.__client.upload_file(
                        str(f), 
                        bucket_name, 
                        file_key, 
                        ExtraArgs={
                            'ContentType': mimetype if mimetype else ''
                        }
                    )
                if show_progress:
                    logger.opt(colors=True).info('<yellow>{:.2%}</yellow> -> {}', i/total_files, str(f))
                    logger.opt(colors=True).info('<green><b>100% completed!</b></green>')
        except:
            logger.exception('What is going on?')

    def website_deploy(
        self,
        local_path,
        bucket_name,
        index_file='index.html',
        error_file='error.html',
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
                logger.opt(colors=True).error('<b>Your AWS credentials doesn\'t seem to work!</b>')
                sys.exit(1)

        except:
            logger.opt(colors=True).error('<b>Your AWS credentials doesn\'t seem to work!</b>')
            sys.exit(1)

        self.sync(local_path, bucket_name)

        logger.info('I know, I\'m awesome! So, let me turn this bucket into a website...')
        logger.info('Checking bucket policy...')

        default_policy = DEFAULT_POLICY.replace('__BUCKET_NAME__', bucket_name).strip()
        if policy is not None:
            default_policy = policy.replace('__BUCKET_NAME__', bucket_name).strip()

        try:
            
            res = self.__client.get_bucket_policy(Bucket=bucket_name)

            current_bucket_policy = hashlib.md5(
                self.__policy_sanitizer(res['Policy']).encode()
            ).hexdigest()
            
            updated_bucket_policy = hashlib.md5(
                self.__policy_sanitizer(default_policy).encode()
            ).hexdigest()

            if current_bucket_policy == updated_bucket_policy:
                logger.opt(colors=True).info('<cyan><b>Bucket policy is already updated.</b></cyan> I will just skip this process!')
            else:
                logger.opt(colors=True).info('<magenta><b>This bucket policy needs to be updated.</b></magenta> I will do it!')
                res = self.__client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=default_policy
                )
                logger.opt(colors=True).info('<green><b>Bucket policy successfully updated!</b></green>')

        except ClientError as e:
            
            if e.response['Error']['Code'] == 'MalformedPolicy':
                logger.opt(colors=True).error('<b>{} - {}</b>', e.response['Error']['Code'], e.response['Error']['Message'])
            else:
                logger.opt(colors=True).info('<magenta><b>This bucket doesn\'t have any policy.</b></magenta> I will create one...')
                res = self.__client.put_bucket_policy(
                    Bucket=bucket_name,
                    Policy=default_policy
                )
                logger.opt(colors=True).info('<green><b>Bucket policy successfully created!</b></green>')
        except:
            logger.exception('What is going on?')

        logger.info('Adjust bucket website settings...')
        try:
            self.__client.put_bucket_website(
                Bucket=bucket_name,
                WebsiteConfiguration={
                    'ErrorDocument': {
                        'Key': error_file
                    },
                    'IndexDocument': {
                        'Suffix': index_file
                    }
                }
            )
            logger.opt(colors=True).info('Your bucket website URL is: <blue><b>http://{}.s3-website-us-east-1.amazonaws.com</b></blue>', bucket_name)
        except:
            logger.exception('what?')

    def __policy_sanitizer(self, policy):
        regex = re.compile("[\n,\s,\t]")
        return regex.sub('', policy)