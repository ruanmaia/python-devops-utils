__all__ = ['s3', 'ecs']

import os
import click

from devops.aws import AWS_DevOps_Utils
from cli import cli

@cli.group(name='aws')
@click.option(
    '--access-key',
    help='''
        If not provided, the system will try to load the value 
        from AWS_ACCESS_KEY environment variable.
    ''', 
    default=lambda: os.environ.get('AWS_ACCESS_KEY', None)
    )
@click.option(
    '--secret-key', 
    help='''
        If not provided, the system will try to load the value 
        from AWS_SECRET_KEY environment variable.
    ''', 
    default=lambda: os.environ.get('AWS_SECRET_KEY', None)
    )
@click.option(
    '--region',
    help='''
        If not provided, the system will try to load the value 
        from AWS_REGION environment variable.
    ''', 
    default=lambda: os.environ.get('AWS_REGION', 'us-east-1')
    )
@click.pass_context
def aws_cli(ctx, access_key, secret_key, region):

    aws_utils = None
    ctx.ensure_object(dict)

    if not ((access_key is None) or (secret_key is None) or (region is None)):
        ctx.obj['aws_region'] = region
        ctx.obj['aws_access_key'] = access_key
        ctx.obj['aws_secret_key'] = secret_key
        aws_utils = AWS_DevOps_Utils(access_key, secret_key, region)
    
    ctx.obj['aws_utils_instance'] = aws_utils