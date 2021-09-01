from cli.aws import aws_cli

@aws_cli.group()
def s3():
    print('Enable S3')

@s3.command('website-deploy')
def website_deploy():
    print('Making deploy!')