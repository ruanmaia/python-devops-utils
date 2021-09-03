#### LIBRARIES IMPORT
import click

#### DEFAULT CLI GROUP
@click.group()
def cli(): pass

@cli.command('version')
def version():
    print('v0.1.0')

@cli.command('slugify')
@click.argument('string')
def slugify(string):
    from slugify import slugify
    print(slugify(string))