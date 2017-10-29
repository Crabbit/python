######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-05-05"
######################################

"""
This module is prepared for noah calls
"""

import os
import sys
import logging
import re
import commands
from load_config import Config
from operator import itemgetter
from operator import attrgetter

"""
import modules
"""
import modules

#logging.basicConfig(filename=Util.get_cur_dir() + '/log/load_config.log',
log_file = modules.Util.get_top_dir() + '/log/noah.log'

logging.basicConfig(filename=log_file,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class PrintStatusValue(object):
    """merge status file, and print key - value"""

    def __init__(self):
        """self.kutype_list: the kutype list that needed to print out"""
        if (len(sys.argv) == 1):
            logging.error('Argv is null, at least one kutype is required')
            print('Argv is null, at least one kutype is required')
            self.kutype_list = list()
        else:
            self.kutype_list =  sys.argv[1:]

        """    load register config: record ku work information"""
        """    initialization ku register config"""
        self.register_json_doc = Config.load_register_conf()
        self.register_kutype_list = dict()

        """monitor agent conf"""
        self.status_dir = Config.status_dir

    def validate(self):
        """verify the configuration and argv"""
        count = 0
        single_kutype = ""

        """initialization self.register_kutype_list
            self.register_kutype_list:
                    key: kutype name
                    value: monitor strategy infomation (public + private)
        """
        for count in range(0, int(self.register_json_doc['build']['kutype_num'])):
            self.register_kutype_list[self.register_json_doc['build']['kutype'][count]['name']] =\
                self.register_json_doc['build']['kutype'][count]['monitor']

        """check argv"""
        for single_kutype in self.kutype_list:
            if single_kutype not in self.register_kutype_list.keys():
                logging.error('[Kutype] = ' + single_kutype + 'is not registered!')
                return 1
        return 0

    def print_all_kutype_status_info(self):
        """print all kutype status key - value"""
        single_kutype_name = ""
        single_strategy_type = ""
        single_strategy = ""
        total_monitor_iterm = ""
        single_monitor_iterm = ""

        for single_kutype_name in self.kutype_list:
            """get kutype status dir"""
            single_kutype_status_dir = self.status_dir + '/' + single_kutype_name

            """get strategy type"""
            for single_strategy_type in self.register_kutype_list[single_kutype_name]:

                """get strategy infomation"""
                for single_strategy in self.register_kutype_list[single_kutype_name]\
                                            [single_strategy_type]:
                    total_strategy_monitor_iterm = self.register_kutype_list[single_kutype_name]\
                                            [single_strategy_type][single_strategy]
                    strategy_mon_file= single_kutype_status_dir + '/' + single_strategy + '.status'
                    for single_monitor_iterm in re.split(r';\s*', total_strategy_monitor_iterm):

                        """get analysis strategy, monitor iterms for analysis"""
                        monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=',\
                                                    single_monitor_iterm)[0]
                        monitor_comparison_method = modules.Util.extract_by_regex(\
                            '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', single_monitor_iterm)[0]
                        monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=',\
                                                    single_monitor_iterm)[1]

                        """production shell command"""
                        shell_cmd = 'echo -n ' + single_kutype_name + '_; cat ' +\
                                strategy_mon_file + ' | grep ' + monitor_iterm_key +\
                                ' | tail -1 | awk \'{print $NF}\''
                        shell_cmd_return, shell_cmd_stout = commands.getstatusoutput(shell_cmd)
                        if shell_cmd_return == 0:
                            print shell_cmd_stout
        return 0

    def start_print(self):
        """start print monitor iterm key:value"""
        self.validate()
        self.print_all_kutype_status_info()
        

if __name__ == "__main__":
    debug_instance = PrintStatusValue()
    debug_instance.start_print()
