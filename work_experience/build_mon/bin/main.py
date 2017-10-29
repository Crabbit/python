######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-03-24"
######################################

import os
import sys
import logging
import json
import Command

logging.basicConfig(filename='../log/main.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class ControlEntrance(object):
    """main function control"""

    def __init__(self):
        """
        Initialization command control argv and function.

        self.command_name: proram name
        self.sub_command_names: save the argv list
        self.sub_commands: bind argv and method
        """

        self.command_name = 'main'
        self.sub_command_names = []
        self.sub_commands = {}

        self.register_argv('start', Command.MonAgentStart)
        self.register_argv('stop', Command.MonAgentStop)
        self.register_argv('reload', Command.MonAgentReload)
        self.register_argv('restart', Command.MonAgentRestart)
        self.register_argv('check-conf', Command.CheckConf)
        #self.register_argv('help', Command.Help)
        self.register_help_command()

    def register_argv(self, sub_command_name, sub_command_type, usage=None):
        """bind argv and method"""

        self.sub_command_names.append(sub_command_name)
        if usage is None:
            usage = 'usage: %s %s options' % (self.command_name, sub_command_name)
        self.sub_commands[sub_command_name] = sub_command_type(usage)

    def register_help_command(self):
        """print help info method"""

        help_usage = 'usage: %s help [SUBCOMMAND...]' % self.command_name
        help_command = Command.Help(help_usage, self.sub_command_names, self.sub_commands)
        self.sub_command_names.append('help')
        self.sub_commands['help'] = help_command

    def run_with_argv(self):
        """process argv"""

        if len(sys.argv) == 1:
            sub_command_name = 'help'
            args = []
        else:
            sub_command_name = sys.argv[1]
            args = sys.argv[2:]
        if sub_command_name not in self.sub_commands:
            print "unkown sub_command '%s'." % sub_command_name
            print "Try '%s help' for usage." % self.command_name
            return 1
        else:
            sub_command = self.sub_commands[sub_command_name]
            logging.debug('execute command %s start!' % sub_command_name)
            sub_command.set_args(args)
            result = sub_command.execute()

            if result == True:
                logging.debug('execute command %s succeed!' % sub_command_name)
            else:
                logging.debug('execute command %s failed.' % sub_command_name)
            return (0 if result == True else 1)

if __name__ == "__main__":

    monitor_start = ControlEntrance()
    sys.exit(monitor_start.run_with_argv())
"""
    debug_instance = load_config.Config()
    json_fd = debug_instance.load_register_conf()
    print int(json_fd['build']['kutype_num'])
"""
