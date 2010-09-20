#!/usr/bin/env python
from distutils.core import setup

setup(
      name='django-nosetests',
      version='0.1',
      author='George Song, Mikhail Korobov',
      author_email='george@55minutes.com, kmike84@gmail.com',
      url = 'http://bitbucket.org/kmike/django-coverage/',
      download_url = 'http://bitbucket.org/kmike/django-coverage/get/tip.zip',

      description = 'Django Test Coverage App',
      long_description = "A test coverage reporting tool that utilizes "
                         "Ned Batchelder's excellent coverage.py to show how "
                         "much of your code is exercised with your tests.",

      license = 'Apache License 2.0',
      packages=['django_nosetests',
                'django_nosetests.utils',
                'django_nosetests.utils.module_tools',
                'django_nosetests.utils.coverage_report',
                'django_nosetests.utils.coverage_report.templates'],

      requires = ['django (>=1.0.2)', 'coverage (>= 2.85)', 'htmlplug (>=0.1)'],

      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Framework :: Django',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ],
)
