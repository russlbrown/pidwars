try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'name': 'PIDWars',
	'description': 'Autonomous bots battle it out on teams',
	'author': 'Russ Brown',
	'author_email': 'russbrown@protonmail.com',
	'url': 'home page for the package',
	'download_url': 'https://github.com/russlbrown/pidwars.git',
	
	'version': '0.1',
	'install_requires': ['nose', 'pygame', 'pyOpenGL'],

	'packages': ['pidwars'],
	'scripts': []
	
	}

setup(**config)