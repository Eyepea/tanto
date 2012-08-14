#! /usr/bin/env python

__docformat__ = 'rst'

import os
from setuptools import setup, find_packages

long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name='eyepea-monitoring-agent',
    version='0.9',
    description='Takes monitoring data from Nagios-plugins to push with NSCA (Nagios or Icinga) or WS-Shinken.',
    long_description=long_description,
    author='Ludovic Gasc',
    author_email='ludovic.gasc@eyepea.eu',
    url='https://github.com/Eyepea/eyepea_monitoring_agent',
    packages=find_packages(),
    scripts=['eyepea_monitoring_agent'],
    include_package_data=True,
    zip_safe=False,
    platforms='UNIX',
    package_data={'monitoring_agent': ['configspecs/*.cfg']},
    data_files=[('/etc/eyepea_monitoring_agent', ['etc/logging.ini',
                                                  'etc/nagios_plugins.cfg',
                                                  'etc/nsca.cfg',
                                                  'etc/ws_shinken.cfg']),
                ('/etc/cron.d', ['etc/cron.d/eyepea_monitoring_agent']),
                ('/var/run/eyepea_monitoring_agent', ['etc/.placeholder']),
                ('/var/lib/eyepea_monitoring_agent', ['etc/.placeholder']),],
    license='GNU Affero General Public License v3',
    install_requires=[
        'argparse>=1.1',
        'configobj>=4.7.2',
        'pynsca>=1.2',
        'requests>=0.10.1',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
    ],
)
