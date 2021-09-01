__all__ = ['s3']

from cli import cli

@cli.group(name='aws')
def aws_cli():
    print('Enable AWS')