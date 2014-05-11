#! /usr/bin/env python

__docformat__ = 'rst'

import os
from setuptools import setup, find_packages
from sys import version_info

long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read() + '\n\n' + open(os.path.join(os.path.dirname(__file__), 'HISTORY.rst')).read()

install_requires=(
    'configobj>=4.7.2',
    'pynsca>=1.2',
    'requests>=0.10.1',
),
# Python 2.6 and below requires argparse
if version_info[:2] < (2, 7):
    install_requires+=('argparse>=1.1', )

setup(
    name='tanto',
    version='1.1',
    description='Takes monitoring data from Nagios-plugins to push with NSCA (Nagios or Icinga) or WS-Shinken.',
    long_description=long_description,
    author='Ludovic Gasc',
    author_email='ludovic.gasc@eyepea.eu',
    url='https://github.com/Eyepea/tanto',
    packages=find_packages(),
    scripts=['tanto'],
    include_package_data=True,
    zip_safe=False,
    platforms='UNIX',
    package_data={'monitoring_agent.inputs': ['configspecs/*.cfg'],
                  'monitoring_agent.outputs': ['configspecs/*.cfg']},
    data_files=[('etc/tanto', ['etc/tanto/logging.ini']),
                ('etc/tanto/inputs', ['etc/tanto/inputs/nagios_plugins.cfg']),
                ('etc/tanto/outputs', ['etc/tanto/outputs/email.cfg',
                                       'etc/tanto/outputs/nsca.cfg',
                                      'etc/tanto/outputs/ws_shinken.cfg']),
                ('etc/cron.d', ['etc/cron.d/tanto'])],
    license='GNU Affero General Public License v3',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking :: Monitoring',
    ],
)
