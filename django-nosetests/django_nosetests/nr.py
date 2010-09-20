"""
Django test runner that invokes nose.

Usage:
    ./manage.py test DJANGO_ARGS -- NOSE_ARGS

The 'test' argument, and any other args before '--', will not be passed
to nose, allowing django args and nose args to coexist.

You can use

    NOSE_ARGS = ['list', 'of', 'args']

in settings.py for arguments that you always want passed to nose.
"""
import sys

from django.conf import settings
import default_settings
from django.db import connection
from django.test import utils

import nose

import coverage
import os
import sys
import logging
import logging.handlers

from django.db.models import get_app, get_apps
from django.db import connection, transaction
from django.test.simple import run_tests as base_run_tests

from utils.module_tools import get_all_modules
from utils.coverage_report import html_report



# These can't contain the name *test* otherwise nose will pick them up as a testcase.
SETUP_ENV = 'setup_environment'
TEARDOWN_ENV = 'teardown_environment'


# Setup logger #################################################################    
# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s'\
                              '%(message)s')


if os.path.exists(os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_debug.txt')):
    os.remove(os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_debug.txt'))

# create file handler which logs even debug messages
log_debug = logging.handlers.RotatingFileHandler(\
filename=os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_debug.txt'),\
mode="a",maxBytes=2097152,backupCount=15)

log_debug.setLevel(0)
log_debug.setFormatter(formatter) 
logger.addHandler(log_debug)        


if os.path.exists(os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_error.txt')):
    os.remove(os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_error.txt'))

# create console handler with a higher log level
log_error = logging.handlers.RotatingFileHandler(\
filename=os.path.join('..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'log_error.txt'),\
mode="a",maxBytes=2097152,backupCount=15)

log_error.setLevel(logging.ERROR)
log_error.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(log_error)
      
################################################################################

def _get_app_package(app_model_module):
    """
    Returns the app module name from the app model module.
    """
    return '.'.join(app_model_module.__name__.split('.')[:-1])

def get_test_enviroment_functions():
    """The functions setup_environment and teardown_environment in
    <appname>.tests modules will be automatically called before and after
    running the tests.
    """
    setup_funcs = []
    teardown_funcs = []
    for app_name in settings.INSTALLED_APPS:
        mod = __import__(app_name, fromlist=['tests'])
        if hasattr(mod, 'tests'):
            if hasattr(mod.tests, SETUP_ENV):
                setup_funcs.append(getattr(mod.tests, SETUP_ENV))
            if hasattr(mod.tests, TEARDOWN_ENV):
                teardown_funcs.append(getattr(mod.tests, TEARDOWN_ENV))
    return setup_funcs, teardown_funcs


def setup_test_environment(setup_funcs):
    utils.setup_test_environment()
    for func in setup_funcs:
        func()


def teardown_test_environment(teardown_funcs):
    utils.teardown_test_environment()
    for func in teardown_funcs:
        func()


def run_tests(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    setup_funcs, teardown_funcs = get_test_enviroment_functions()
    # Prepare django for testing.
    setup_test_environment(setup_funcs)
    old_db_name = settings.DATABASES['default']['NAME']
    connection.creation.create_test_db(verbosity, autoclobber=not interactive)

    #from django.db import connection, transaction

    # Pretend it's a production environment.
    settings.DEBUG = False

    nose_argv = [
        'nosetests', '-verbose', '--with-html-output', 
        '--html-output='+os.path.join(
            '..',default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR,'tests.html'
        )
    ]
    nose_argv.extend(default_settings.NOSE_ARGV)

    # Everything after '--' is passed to nose.
    if '--' in sys.argv:
        hyphen_pos = sys.argv.index('--')
        nose_argv.extend(sys.argv[hyphen_pos + 1:])


    if default_settings.NOSE_SCHEMA:
        cursor = connection.cursor()
        
        fp = file(default_settings.NOSE_SCHEMA,'r')
        data = fp.read()
        fp.close()
        
        # fuckin Django models forget to make commit!
        transaction.commit_unless_managed() 
        try:
            cursor.execute(data)
            transaction.commit_unless_managed()
        except Exception,err:
            print 'DB Schema load error: ',err
        else:
            print 'DB Schema loaded.'
    else:
        print 'No Schema found.'
    
    print 'Start running tests.'
    #####

    coverage.use_cache(0)
    for e in default_settings.COVERAGE_CODE_EXCLUDES:
        coverage.exclude(e)
    coverage.start()

    #####

    nose.run(argv=nose_argv)

    #####

    coverage.stop()
    #####
    
    print 'Testing ended.'

    # Clean up django.
    connection.creation.destroy_test_db(old_db_name, verbosity)
    teardown_test_environment(teardown_funcs)

    #####

    coverage_modules = []
    if test_labels:
        for label in test_labels:
            label = label.split('.')[0]
            app = get_app(label)
            coverage_modules.append(_get_app_package(app))
    else:
        for app in get_apps():
            coverage_modules.append(_get_app_package(app))

    coverage_modules.extend(default_settings.COVERAGE_ADDITIONAL_MODULES)

    packages, modules, excludes, errors = get_all_modules(
        coverage_modules, default_settings.COVERAGE_MODULE_EXCLUDES,
        default_settings.COVERAGE_PATH_EXCLUDES)

    outdir = default_settings.COVERAGE_REPORT_HTML_OUTPUT_DIR
    if outdir is None:
        coverage.report(modules.values(), show_missing=1)
        if excludes:
            print >>sys.stdout
            print >>sys.stdout, "The following packages or modules were excluded:",
            for e in excludes:
                print >>sys.stdout, e,
            print >>sys.stdout
        if errors:
            print >>sys.stdout
            print >>sys.stderr, "There were problems with the following packages or modules:",
            for e in errors:
                print >>sys.stderr, e,
            print >>sys.stdout
    else:
        outdir = os.path.abspath(outdir)
        if default_settings.COVERAGE_CUSTOM_REPORTS:
            html_report(outdir, modules, excludes, errors)
        else:
            coverage._the_coverage.html_report(modules.values(), outdir)
        print >>sys.stdout
        print >>sys.stdout, "HTML reports were output to '%s'" %outdir


