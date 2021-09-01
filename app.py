#### LIBRARIES IMPORT
import click

#### DEFAULT CLI GROUP
@click.group()
def cli(): pass

@cli.command('version')
def version():
    print('v0.1.0')

@cli.group()
def aws(): pass

@aws.group()
def s3(): pass

@s3.command()
def website_deploy(): pass