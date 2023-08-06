import os


def author() -> str:
    return 'ulbwa'


def author_url() -> str:
    return 'https://ulbwa.xyz'


def version() -> str:
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                           'setup.py'), 'r') as f:
        data = f.read()
        return data.split('version=\'')[1].split('\',')[0]
