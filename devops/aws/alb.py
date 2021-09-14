import boto3
import json
import sys

from botocore.exceptions import ClientError
from loguru import logger


class ALB_DevOps_Utils:
    
    __client = None
    __session = None

    def __init__(self, session):
        self.__session = session
        self.__client = session.client('elbv2')

    @property
    def client(self):
        self.__client