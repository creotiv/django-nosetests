import sys
try:
    import ez_setup
    ez_setup.use_setuptools()
except ImportError:
    pass

from setuptools import setup

setup(
    name='Html output plugin',
    version='0.1.2',
    author='Andrey Nikishaev',
    author_email = 'creotiv@gmail.com',
    description = 'Nose html output plugin',
    license = 'GNU LGPL',
    requires = ['coverage (>= 2.85)'],
    py_modules = ['htmlplug','template'],
    entry_points = {
        'nose.plugins.0.10': [
            'htmlout = htmlplug:HtmlOutput'
            ]
        }

    )
