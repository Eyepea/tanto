# -*- coding: utf-8 -*-

#from pprint import pprint as pp # debug only
import logging
import subprocess
import os
import time

import configurator

STATUSES = [('OK', logging.INFO),
            ('WARNING', logging.INFO),
            ('CRITICAL', logging.INFO),
            ('UNKNOWN', logging.ERROR)]

class NagiosPlugins(object):
    '''
    Class to handle each nagios-plugin
    '''


    def __init__(self, config_file):
        '''
        Constructor
        '''
        # Setup servers dict from config file
        self.plugins = configurator.read(config_file,
                                         configspec='configspecs/nagios_plugins.cfg',
                                         list_values=True)

    def launch_plugin(self):
        '''
        launch nagios_plugin command
        '''
        # nagios_plugins probes
        for plugin in self.plugins:
            # Construct the nagios_plugin command
            command = ('%s%s' % (self.plugins[plugin]['path'], self.plugins[plugin]['command'])).split(' ')

            try:
                nagios_plugin = subprocess.Popen(command,
                                                 shell=False,
                                                 stdout=subprocess.PIPE,
                                                 stderr=subprocess.PIPE)
            except OSError:
                logging.error("[nagios_plugins]: '%s' executable is missing",
                              command[0])
            else:
                return_value = nagios_plugin.communicate()[0].strip()
                return_code = nagios_plugin.returncode
                logging.log(STATUSES[return_code][1],
                            "[nagios_plugins][%s] (%s status): %s",
                            os.path.basename(command[0]),
                            STATUSES[return_code][0],
                            return_value)
                yield {'return_code': int(return_code),
                       'return_value': str(return_value),
                       'time_stamp': int(time.time()),
                       'service_description': plugin,
                       'specific_servers': self.plugins[plugin]['servers']}