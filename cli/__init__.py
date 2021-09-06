#### LIBRARIES IMPORT
import click

#### DEFAULT CLI GROUP
@click.group()
def cli():
    '''
    A set of devops command line utility tools.\n
    The main idea behind this project is to simply the deployment process, providing
    just one command line interface for all services and modules frequently used when
    writing CI/CD pipelines.\n
    Some commands are just a wrapper for the respective python 3rd party module.
    '''

@cli.command('version')
def version():
    print('v0.1.0')

@cli.command('slugify')
@click.argument('string')
def slugify(string):
    from slugify import slugify
    print(slugify(string))