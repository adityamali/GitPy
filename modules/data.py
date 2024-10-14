import hashlib
import os

GIT_DIR = '.gitpy'

def init():
    os.makedirs(GIT_DIR, exist_ok=True)
    with open(os.path.join(GIT_DIR, 'config'), 'w') as f:
        f.write('[core]\n\trepositoryformatversion = 0\n\tfilemode = false\n')
    os.makedirs(os.path.join(GIT_DIR, 'objects'), exist_ok=True)


def hash_object(data, type_='blob'):
    obj = type_.encode () + b'\x00' + data
    oid = hashlib.sha1 (obj).hexdigest ()
    with open (f'{GIT_DIR}/objects/{oid}', 'wb') as out:
        out.write (obj)
    return oid


def get_object (oid, expected='blob'):
    with open (f'{GIT_DIR}/objects/{oid}', 'rb') as f:
        obj = f.read ()
    
    type_, data = obj.split (b'\x00')
    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return data