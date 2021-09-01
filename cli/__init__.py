#### LIBRARIES IMPORT
import click

#### DEFAULT CLI GROUP
@click.group()
def cli(): pass

@cli.command('version')
def version():
    print('v0.1.0')