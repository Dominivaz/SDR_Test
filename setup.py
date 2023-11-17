from setuptools import setup

setup_args = {
    'name': 'SDR_Test', 
    'author': 'Dominic',
    'url': 'https://github.com/Dominivaz/SDR_Test.git',
    'license': 'bsd',
    'description': 'SDR Test',
    'version': '1.0.1',
    'install_requires': ['numpy>=1.14'],
    'package_dir': {'SDR_Test':'SDR_Test'},
    'packages': ['SDR_Test'],
}

if __name__ == '__main__':
    setup(**setup_args)