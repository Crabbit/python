######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-03-24"
######################################

"""
This module provide argv implementation
"""

import os
import sys
import logging
import json
from optparse import OptionParser
from optparse import IndentedHelpFormatter
from load_config import Config
from monitor_start import MonitorAgentStart

"""
import modules
"""
import modules

logging.basicConfig(filename='../log/Command.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class Command(object):
    """Command object, link argv and class"""

    def __init__(self,usage):
        """
        Initialization some value

        self.args: additional argv
        """
        formatter = IndentedHelpFormatter(max_help_position=400, width=800)
        if usage is not None:
            self.parser = OptionParser(formatter=formatter, usage=usage)
        else:
            self.parser = OptionParser(formatter=formatter)
        self.parser.add_option('', "--conf_dir", help='specified the conf dir.')
        self.parser.add_option('', "--log_dir", help='specified the conf dir.')
        self.parser.add_option('', "--modules_dir", help='specified the log dir.')
        self.parser.add_option('', "--strategy_pub_dir", help='specified the log dir.')
        self.parser.add_option('', "--strategy_pri_dir", help='specified the log dir.')

        self.args = ''

    def set_args(self, args):
        """set additional value"""
        self.args = args

    def validate(self, options, args):
        """object check method"""
        pass

    def execute(self):
        """object execute method"""
        (options, args) = self.parser.parse_args(self.args)
        Config.conf_dir = Config.conf_dir if options.conf_dir is None else options.conf_dir
        Config.log_dir = Config.log_dir if options.log_dir is None else options.log_dir
        Config.modules_dir = Config.modules_dir if options.modules_dir is None else options.modules_dir
        Config.strategy_public_dir = Config.strategy_public_dir if options.strategy_pub_dir is None else options.strategy_public_dir
        Config.strategy_private_dir = Config.strategy_private_dir if options.strategy_pri_dir is None else options.strategy_private_dir

        return True

class MonAgentStart(Command):
    """start monitor agent"""

    def __init__(self, usage=None):
        super(MonAgentStart, self).__init__(usage)

    """check method"""
    def validate(self, options, args):
        return True

    """execute method"""
    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if not self.validate(options, args):
            self.parser.print_help()
            return False
        super(MonAgentStart, self).execute()
        monitor_start_instance = MonitorAgentStart()
        process_list=monitor_start_instance.kutype_mon_start()
        print 'monitor agent start method'

class MonAgentStop(Command):
    """stop monitor agent"""

    def __init__(self, usage=None):
        super(MonAgentStop, self).__init__(usage)
        self.parser.add_option('-F', '--force', action='store_true',\
        dest='force', help='force stop monitor.')

    def validate(self, options, args):
        return True

    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if not self.validate(options, args):
            self.parser.print_help()
            return False
        super(MonAgentStop, self).execute()
        print 'monitor agent stop method'

class MonAgentReload(Command):
    """reload conf """

    def __init__(self, usage=None):
        super(MonAgentReload, self).__init__(usage)

    def validate(self, options, args):
        return True

    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if not self.validate(options, args):
            self.parser.print_help()
            return False
        super(MonAgentReload, self).execute()
        print 'monitor agent reload method'

class MonAgentRestart(Command):
    """restart monitor agent"""

    def __init__(self, usage=None):
        super(MonAgentRestart, self).__init__(usage)

    def validate(self, options, args):
        return True

    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if not self.validate(options, args):
            self.parser.print_help()
            return False
        super(MonAgentRestart, self).execute()
        print 'monitor agent restart method'

class CheckConf(Command):
    """check register conf"""

    def __init__(self, usage=None):
        super(CheckConf, self).__init__(usage)

    def validate(self, options, args):
        return True

    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if not self.validate(options, args):
            self.parser.print_help()
            return False
        super(CheckConf, self).execute()
        print 'Check Conf method'

class Help(Command):
    """help info"""

    def __init__(self, usage=None, command_names=None, commands=None):
        formatter = IndentedHelpFormatter(max_help_position=400, width=800)
        self.parser = OptionParser(formatter=formatter, usage=usage)
        if command_names is None:
            self.command_names = {}
            self.commands = {}
        else:
            self.command_names = command_names
            self.commands = commands
        self.usage = usage

    def execute(self):
        (options, args) = self.parser.parse_args(self.args)
        if len(args) == 0:
            print self.usage
            print '\nAvailable subcommands:'
            for command_name in self.command_names:
                print '\t%s' % command_name
            print ''

        for arg in args:
            if arg in self.commands:
                self.commands[arg].parser.print_help()
            else:
                print '"%s": unknown command.' % arg
            print ''

        return True


if __name__ == "__main__":
    debug_instance = Config()
    json_fd = debug_instance.load_register_conf()
    print int(json_fd['build']['kutype_num'])
