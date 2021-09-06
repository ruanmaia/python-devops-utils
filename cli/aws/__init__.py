__all__ = ['s3']

import os
import click

from devops.aws import AWS_DevOps_Utils
from cli import cli

@cli.group(name='aws')
@click.option(
    '--access-key', 
    required=True, 
    help='''
        If not provided, the system will try to load the value 
        from AWS_ACCESS_KEY environment variable.
    ''', 
    default=lambda: os.environ.get('AWS_ACCESS_KEY', None)
    )
@click.option(
    '--secret-key', 
    required=True, 
    help='''
        If not provided, the system will try to load the value 
        from AWS_SECRET_KEY environment variable.
    ''', 
    default=lambda: os.environ.get('AWS_SECRET_KEY', None)
    )
@click.pass_context
def aws_cli(ctx, access_key, secret_key):
    ctx.ensure_object(dict)
    ctx.obj['aws_access_key'] = access_key
    ctx.obj['aws_secret_key'] = secret_key

    aws_utils = AWS_DevOps_Utils(access_key, secret_key)
    ctx.obj['aws_utils_instance'] = aws_utils 