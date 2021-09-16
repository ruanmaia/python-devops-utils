import boto3

from devops.aws.s3 import S3_DevOps_Utils
from devops.aws.ecs import ECS_DevOps_Utils

class AWS_DevOps_Utils:

    __session = None
    __s3_utils = None
    __ecs_utils = None

    def __init__(self, aws_access_key, aws_secret_key, region_name):
        self.__session = boto3.Session(
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )

    @property
    def session(self):
        return self.__session

    @property
    def s3(self):
        if self.__s3_utils is None:
            self.__s3_utils = S3_DevOps_Utils(self.__session)
        return self.__s3_utils

    @property
    def ecs(self):
        if self.__ecs_utils is None:
            self.__ecs_utils = ECS_DevOps_Utils(self.__session)
        return self.__ecs_utils