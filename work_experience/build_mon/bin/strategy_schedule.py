######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-03-24"
######################################

"""
This module provide strategy schedule features
"""

import os
import sys
import logging
import json
import re
from load_config import Config

"""
import modules
"""
import modules
import strategy

import strategy.public as str_pub

#logging.basicConfig(filename=Util.get_cur_dir() + '/log/load_config.log',
logging.basicConfig(filename='../log/strategy_schedule.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class PublicStrategySchedule(object):
    """public strategy schedule class"""

    support_register_public_strategys = list()
    bind_strategy_and_feature = dict()


    @staticmethod
    def validate_configuration():
        """validate public configuration"""

        """count : in order to check strategy num"""
        count = 0
        config_single_public_strategy = ""
        public_strategy_json_doc = Config.load_strategy_conf()

        for config_single_public_strategy in re.split(r';\s*',\
                     public_strategy_json_doc['public_strategy']):
            count += 1

        if int(count) != int(public_strategy_json_doc['public_strategy_num']):
            logging.error("register public strategy count error!")
            return 1
        return 0


    @staticmethod
    def register_strategy_and_features(mon_iterm, metadata=None, kutype_global_conf=None):
        """register strategy and features"""
        PublicStrategySchedule.bind_strategy_with_feature('kutype_analysis',\
                str_pub.kutype_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('flow_analysis',\
                str_pub.flow_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('error_analysis',\
                str_pub.error_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('job_analysis',\
                str_pub.job_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('output_analysis',\
                str_pub.output_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('download_analysis',\
                str_pub.download_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('parser_analysis',\
                str_pub.parser_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('dag_analysis',\
                str_pub.dag_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))
        PublicStrategySchedule.bind_strategy_with_feature('transmint_analysis',\
                str_pub.transmint_analysis.StartAnalysis(mon_iterm, metadata, kutype_global_conf))


    @staticmethod
    def bind_strategy_with_feature(strategy_name, features):
        """bind strategy and features"""
        PublicStrategySchedule.support_register_public_strategys.append(strategy_name)
        PublicStrategySchedule.bind_strategy_and_feature[strategy_name] = features


    @staticmethod
    def public_strategy_analysis(\
            public_strategy_name, mon_iterm, metadata=None, kutype_global_conf=None):
        """schedule public strategy for analysis"""
        PublicStrategySchedule.validate_configuration()
        PublicStrategySchedule.register_strategy_and_features(\
                mon_iterm, metadata, kutype_global_conf)

        if public_strategy_name not in PublicStrategySchedule.support_register_public_strategys:
            logging.error('Unkown strategy : %s.' % public_strategy_name)
            return 1

        if Config.load_agent_debug_level() >= 5:
            modules.Util.append_log_content_to_file(Config.debug_sql_data_file,\
                ' strategy_name : [' + public_strategy_name + '] mon_iterm : [' + mon_iterm +\
                ' ] metadata : [' + str(metadata) + '] kutype_global_conf : [' +\
                 str(kutype_global_conf) + ']\n')
        excute_analysis_features = \
            PublicStrategySchedule.bind_strategy_and_feature[public_strategy_name]

        return excute_analysis_features.start()


class PrivateStrategySchedule(object):
    """private strategy schedule class"""

    @staticmethod
    def schedule_private_strategy(strategy, mon_iterm, metadata=None, kutype_global_conf=None):
        """load private strategy"""
        pass

    @staticmethod
    def private_strategy_analysis(\
            private_strategy_name, mon_iterm, metadata=None, kutype_global_conf=None):
        """private analysis"""
        pass


if __name__ == "__main__":
    PublicStrategySchedule.public_strategy_analysis(\
    public_strategy_name='flow_analysis', mon_iterm='kutype_running_flow_num', metadata='test')
