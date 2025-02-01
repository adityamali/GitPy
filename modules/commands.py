import os
import click
import textwrap


from . import data
from . import base


oid = base.get_oid


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
@click.argument('object', type=oid)
def cat_file(object):
    click.echo(data.get_object(object, expected=None))


"""Write a tree object from the contents of the index."""
# Iterate over the entries in the index (base.py)
# If the entry is a file, write the contents to the objects directory (call hash_object on the file from data.py)
# If the entry is a directory, recursively call write_tree on the directory
@click.command()
def write_tree():
    click.echo(base.write_tree())


"""Read a tree object from the objects directory."""
# Parse the tree object and return a list of tuples containing the name, object ID, and type of each entry
# If the type is 'blob', read the contents of the object from the objects directory and return it
# If the type is 'tree', recursively call read_tree on the object ID
@click.command()
@click.argument('tree', type=oid)
def read_tree(tree):
    base.read_tree(tree)


"""Commit Messages"""
# Get the current HEAD commit
# Get the parent commit of the HEAD commit
# Write the commit message to the objects directory
@click.command()
@click.option('-m', '--message', required=True)
def commit(message):
    if message is None:
        click.echo("No message provided")
        return
    click.echo(base.commit(message))


"""Log Messages"""
# Get the current HEAD commit
# Get the parent commit of the HEAD commit
# Print the commit message
@click.command()
@click.argument('oid', required=False, type=oid)
def log(oid):
    if oid is None:
        oid = data.get_ref('HEAD')

    while oid:
        commit = base.get_commit(oid)

        click.echo(f'commit {oid}\n')
        click.echo(textwrap.indent(commit.message, '    '))
        click.echo('')

        oid = commit.parent


@click.command()
@click.argument('oid', type=oid, required=False)
def checkout(oid):
    base.checkout(oid)


@click.command()
@click.argument('tag')
@click.argument('oid' type=oid, required=False)
def tag(tag, oid):
    if oid is None:
        oid = data.get_ref('HEAD')
    
    base.create_tag(tag, oid)
