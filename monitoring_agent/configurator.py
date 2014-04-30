# -*- coding: utf-8 -*-
'''
Read configuration via configobj
'''

from os import path
import socket
from configobj import ConfigObj
import validate

class ConfiguratorException(RuntimeError):
    """When the config file is wrong, this exception is raised."""
    def __init__(self, config_file, validation_errors):
        super(ConfiguratorException, self).__init__()
        self.config_file = config_file
        self.validation_errors = validation_errors

    def __str__(self):
        return str(self.validation_errors)

def read(config_file, configspec, server_mode=False, default_section='default_settings', list_values=True):
    '''
    Read the config file with spec validation
    '''
#    configspec = ConfigObj(path.join(path.abspath(path.dirname(__file__)), configspec),
#                           encoding='UTF8',
#                           interpolation='Template',
#                           list_values=False,
#                           _inspec=True)
    config = ConfigObj(config_file,
                       configspec=path.join(path.abspath(path.dirname(__file__)),
                                            configspec),
                                            list_values=list_values)
    validation = config.validate(validate.Validator(), preserve_errors=True)

    if validation == True:
        config = dict(config)
        for section in config:
            if section != default_section:
                if server_mode: # When it's a servers config file, retrieve the correct fqdn
                    config[section]['availability'] = True
                    if config[section]['custom_fqdn'] == None:
                        config[section]['custom_fqdn'] = socket.getfqdn()
                for option in config[section]:  # retrieve default configuration for missing values
                    if config[section][option] == None:
                        config[section][option] = config[default_section][option]

        del(config[default_section])

        return config
    else:
        raise ConfiguratorException(config_file, validation)