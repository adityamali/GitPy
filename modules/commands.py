import os
import click

from . import data
from . import base


"""Initialize a new Git repository."""
# Create a .gitpy directory at the root of the current working directory
# Initialize the .gitpy/config file with the appropriate settings
# Create the .gitpy/objects directory
@click.command()
def init(): 
    data.init()
    click.echo(f'Initialized empty GitPy repository at {os.getcwd()}/{data.GIT_DIR}')


"""Hash the contents of a file."""
# Read the contents of the file and hash it using SHA-1
# Write the hash to the objects directory
@click.command()
@click.argument('file')
def hash_object(file):
    with open(file, 'rb') as f:
        print(data.hash_object(f.read()))


"""Print the contents of a file."""
# Read the contents of the object from the objects directory
# Print the contents
@click.command()
@click.argument('object')
def cat_file(object):
    click.echo(data.get_object(object, expected=None))


"""Write a tree object from the contents of the index."""
# Iterate over the entries in the index (base.py)
# If the entry is a file, write the contents to the objects directory (call hash_object on the file from data.py)
# If the entry is a directory, recursively call write_tree on the directory
@click.command()
def write_tree():
    base.write_tree()