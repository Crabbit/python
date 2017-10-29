#####################################
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

"""
import modules
"""
import modules

#logging.basicConfig(filename=Util.get_top_dir() + '/log/load_config.log',
log_file = modules.Util.get_top_dir() + '/log/load_config.log'
logging.basicConfig(filename=log_file,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class Config(object):
    """load register config file"""
    bin_dir = modules.Util.get_top_dir() + "/bin"
    conf_dir = modules.Util.get_top_dir() + "/conf"
    log_dir = modules.Util.get_top_dir() + "/log"
    tmp_dir = modules.Util.get_top_dir() + "/tmp"
    data_dir = modules.Util.get_top_dir() + "/data"
    status_dir = modules.Util.get_top_dir() + "/status"
    modules_dir = modules.Util.get_top_dir() + "/modules"
    callback_dir = modules.Util.get_top_dir() + "/call-back"
    strategy_public_dir = modules.Util.get_top_dir() + "/bin/strategy/public"
    strategy_private_dir = modules.Util.get_top_dir() + "/bin/strategy/private"

    """Initializes register conf file path"""
    debug_sql_sentence_file = data_dir + "/debug_sql_sentence.data"
    debug_sql_data_file = data_dir + "/debug_sql_data.data"
    debug_public_strategy_file = data_dir + "/debug_public_strategy.data"
    debug_private_strategy_file = data_dir + "/debug_private_strategy.data"

    """Initializes register conf file path"""
    register_conf_file = conf_dir + "/register.json"
    monitor_conf_file = conf_dir + "/monitor.json"

    """    initialization mysql databases config"""
    mysql_json_kutype_global_conf_table_count = 0
    mysql_json_kutype_global_conf_table_list = list()

    mysql_json_kutype_metadata_analysis_table_count = 0
    mysql_json_kutype_metadata_analysis_table_list = list()

    @staticmethod
    def load_register_conf():
        """load register configuration file"""

        try:
            register_conf_fd = open(Config.register_conf_file, 'r')
            register_conf_raw = register_conf_fd.read()
            register_json_doc = json.loads(register_conf_raw)
        except (IOError, UnboundLocalError):
            logging.error("register.json file load error!")
        else:
            """
            print "%s" % register_json_doc['build']['kutype'][0]['monitor']['monitor_iterm']['mon_iterms']
            kutype_num = int(register_json_doc['build'][Config.kutype_num_key])
            for ku_count in range(0,Config.kutype_num):
                print ("%d - %s" % (ku_count,register_json_doc['build']['kutype'][ku_count]['monitor']['monitor_iterm']['mon_iterms']))
            """
            register_conf_fd.close()
            return register_json_doc

    @staticmethod
    def load_monitor_conf():
        """load monitor agent configuration file"""

        try:
            monitor_conf_fd = open(Config.monitor_conf_file, 'r')
            monitor_conf_raw = monitor_conf_fd.read()
            monitor_json_doc = json.loads(monitor_conf_raw)
        except (IOError, UnboundLocalError):
            logging.error("monitor.json file load error!")
        else:
            monitor_conf_fd.close()
            return monitor_json_doc

    @staticmethod
    def load_agent_debug_level():
        """load monitor agent configuration"""
        agent_mode_doc = Config.load_monitor_conf()
        return int(agent_mode_doc['monitor_agent']['debug_level'])

    @staticmethod
    def load_strategy_conf():
        """load monitor agent configuration"""
        monitor_strategy_conf_json_doc = Config.load_monitor_conf()
        return monitor_strategy_conf_json_doc['monitor_agent']['strategy']

    @staticmethod
    def load_mysql_conf():
        """load mysql configuration"""
        mysql_conf_json_doc = Config.load_monitor_conf()
        return mysql_conf_json_doc['mysql']

    @staticmethod
    def load_mysql_global_kutype_conf():
        """    load databases agent conf: record ku global information"""
        mysql_json_kutype_global_conf_table_list = list()
        mysql_json_doc = Config.load_mysql_conf()

        for Config.mysql_json_kutype_global_conf_table_count in range(0,\
                int(mysql_json_doc['kutype_global_conf_table_num'])):
            Config.mysql_json_kutype_global_conf_table_list.append(\
mysql_json_doc['kutype_global_conf_table'][Config.mysql_json_kutype_global_conf_table_count])
        return Config.mysql_json_kutype_global_conf_table_list

    @staticmethod
    def load_mysql_kutype_metadata_conf():
        """    load kutype metadata: for strategy analysis"""
        Config.mysql_json_kutype_metadata_analysis_table_list = list()
        mysql_json_doc = Config.load_mysql_conf()

        for Config.mysql_json_kutype_global_conf_table_count in range(0,\
                int(mysql_json_doc['kutype_metadata_analysis_table_num'])):
            Config.mysql_json_kutype_metadata_analysis_table_list.append(\
mysql_json_doc['kutype_metadata_analysis_talbe'][Config.mysql_json_kutype_global_conf_table_count])
        return Config.mysql_json_kutype_metadata_analysis_table_list



if __name__ == "__main__":
    register_json_doc = Config.load_register_conf()
    monitor_json_doc = Config.load_monitor_conf()
    mysql_json_doc = Config.load_mysql_conf()

    register_kutype_num = int(register_json_doc['build']['kutype_num'])
    databases_agent_conf = str(mysql_json_doc['kutype_global_conf_table'])
    #cycle_interval_buffer = register_json_doc['build']['kutype'][1]['cycle_interval_buffer']

    print "register kutype num = %d." % register_kutype_num
    print "mysql global conf table name = %s." % databases_agent_conf

    print Config.load_mysql_global_kutype_conf()
    print Config.load_mysql_kutype_metadata_conf()

    print Config.load_agent_debug_level()
    print Config.load_strategy_conf()
