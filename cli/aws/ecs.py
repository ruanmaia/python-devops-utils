from cli.aws import aws_cli

import click
import sys
import yaml
import json

### This command exists just for organization purposes
@aws_cli.group()
def ecs(): pass

@ecs.command('deploy')
@click.option(
    '-f', 
    '--file', 
    'config_file',
    required=True,
    type=click.File('rb')
    )
@click.option(
    '--format',
    'config_file_format',
    default='yaml',
    type=click.Choice(['yaml', 'json'])
    )
@click.pass_context
def deploy(ctx, config_file, config_file_format):  
    aws_utils = ctx.obj.get('aws_utils_instance', None)
    if aws_utils is None:
        aws_ctx = ctx.parent.parent
        aws_ctx.fail("Please, check your AWS configuration!\n\n{}".format(aws_ctx.get_help()))
        ctx.exit(1)

    if config_file_format == 'yaml':
        data = yaml.load(config_file, Loader=yaml.FullLoader)
    elif config_file_format == 'json':
        data = json.load(config_file)

    aws_utils.ecs.deploy(data)