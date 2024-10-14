import click

from modules.commands import *

@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(hash_object)
cli.add_command(cat_file)
cli.add_command(write_tree)

if __name__ == '__main__':
    cli()
