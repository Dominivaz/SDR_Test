from setuptools import setup

setup_args = {
    'name': 'SDR_Testing', 
    'author': 'Dominic',
    'url': 'https://github.com/Dominivaz/module_test.git',
    'license': 'bsd',
    'description': 'SDR Testing',
    'version': '1.0.1',
    'install_requires': ['numpy>=1.14'],
    'package_dir': {'SDR_Testing':'SDR_Testing'},
    'packages': ['SDR_Testing'],
}

if __name__ == '__main__':
    setup(**setup_args)