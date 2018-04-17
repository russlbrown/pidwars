try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'projectname',
	'description': 'My Project',
	'author': 'Russ Brown',
	'author_email': 'russbrown@protonmail.com',
	'url': 'home page for the package',
	'download_url': 'Where to download it.',
	
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['NAME'],
	'scripts': []
	
	}

setup(**config)