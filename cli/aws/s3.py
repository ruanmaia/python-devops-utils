from cli.aws import aws_cli

import click

### This command exists just for organization purposes
@aws_cli.group()
def s3(): pass

@s3.command('website-deploy')
@click.argument('local_path')
@click.argument('bucket_name')
@click.option('--index-file', default='index.html')
@click.option('--error-file', default='error.html')
@click.option('--policy', default=None)
@click.pass_context
def website_deploy(
    ctx, 
    local_path, 
    bucket_name,
    index_file,
    error_file,
    policy
):
    aws_utils = ctx.obj.get('aws_utils_instance', None)
    aws_utils.s3.website_deploy(local_path, bucket_name, index_file, error_file, policy)