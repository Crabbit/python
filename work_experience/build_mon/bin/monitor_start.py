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
import time
import datetime
import logging
import json
import re
import threading
import MySQLdb
from load_config import Config
from operator import itemgetter, attrgetter
from access_meta_data import AccessMysqlData
from access_meta_data import GeneralOperation
from strategy_schedule import PublicStrategySchedule
from strategy_schedule import PrivateStrategySchedule

"""
import modules
"""
import modules

#logging.basicConfig(filename=Util.get_cur_dir() + '/log/load_config.log',
logging.basicConfig(filename='../log/monitor_start.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

threadLock = threading.Lock()


class MonitorAgentStart(object):
    """schedule modules"""

    def __init__(self):
        """    load monitor agent config"""
        self.monitor_agent_json_doc = Config.load_monitor_conf()

        """    load register config: record ku work information"""
        """    initialization ku register config"""
        self.register_json_doc = Config.load_register_conf()
        self.register_json_kutype_mon_thread_list = list()

    def validate(self, database_kutype_name=None):
        """verify the configuration"""
        if database_kutype_name is None:
            logging.error('database_kutype_name value is emputy!')
            return 1

        ku_global_conf_list = dict()

        """load global kutype mysql configure"""
        """ku_global_conf: monitotr.json/ mysql/ kutype_global_conf_table"""
        ku_global_conf = Config.load_mysql_global_kutype_conf()

        for raw in range(0, len(ku_global_conf)):
            """kutype config"""
            if ku_global_conf[raw]['data_name'] == 'ygg_ku_global_conf':
                sql_sentence = 'select * from ' + ku_global_conf[raw]['table'] + \
                                ' where kuType=\'' + database_kutype_name + '\';'
                if Config.load_agent_debug_level() >= 2:
                    modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [Load ygg_ku_global_conf] sql sentence: ' + sql_sentence + '\n')
                ku_global_conf_list[ku_global_conf[raw]['data_name']] = \
                    AccessMysqlData.operating_mysql_data_by_conf(ku_global_conf[raw], sql_sentence)

            """job sla config"""
            if ku_global_conf[raw]['data_name'] == 'ygg_job_conf':
                sql_sentence = 'select * from ' + ku_global_conf[raw]['table'] + \
                                ' where kuType regexp \'(^|[,])' + database_kutype_name + ',\';'
                if Config.load_agent_debug_level() >= 2:
                    modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [Load ygg_job_conf] sql sentence: ' + sql_sentence + '\n')
                ku_global_conf_list[ku_global_conf[raw]['data_name']] = \
                    AccessMysqlData.operating_mysql_data_by_conf(ku_global_conf[raw], sql_sentence)
        return ku_global_conf_list
            

    def kutype_mon_start(self):
        """start kutype mon"""
        count = 0

        """    open up new process for every kutype"""
        for count in range(0, int(self.register_json_doc['build']['kutype_num'])):
            kutype_register_info = self.register_json_doc['build']['kutype'][count]
            kutype_name = kutype_register_info['name']
            kutype_global_info = self.validate(kutype_register_info['database_kutype'])
            if kutype_global_info is not None:
                self.register_json_kutype_mon_thread_list.append(KutypeMonitorThread(\
                    thread_id=count,\
                    kutype_name=kutype_name,\
                    kutype_register_info=kutype_register_info,\
                    kutype_global_info=kutype_global_info))

        for thread in self.register_json_kutype_mon_thread_list:
            thread.start()
            time.sleep(3)

        return self.register_json_kutype_mon_thread_list


class KutypeMonitorThread(threading.Thread):
    """kutype monitor agent thread"""

    def __init__(self, thread_id, kutype_name, kutype_register_info, kutype_global_info):

        """    initialization kutype monitor thread info"""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.kutype_name = kutype_name
        self.thread_name = self.kutype_name + '_monitor_agent'
        self.kutype_register_info = kutype_register_info
        self.kutype_global_info = kutype_global_info
        self.value = 0

        """   initialization kutype log file"""
        self.kutype_monitor_agent_log_path = Config.log_dir + '/' + self.kutype_name 
        self.kutype_monitor_agent_log_file = self.kutype_monitor_agent_log_path +\
                                                            '/monitor_agent.log'
        self.kutype_status_log_file = self.kutype_monitor_agent_log_path + '/status.log'
        self.kutype_error_log_file = self.kutype_monitor_agent_log_path + '/error.log'

        """   initialization kutype status file"""
        self.kutype_monitor_agent_status_path = Config.status_dir + '/' + self.kutype_name
        self.kutype_monitor_iteration_file = self.kutype_monitor_agent_status_path +\
                                                            '/bs_newest_iteration.status'
        self.kutype_monitor_cycle_file = self.kutype_monitor_agent_status_path +\
                                                            '/bs_newest_cycle.status'
        self.kutype_monitor_bs_file = self.kutype_monitor_agent_status_path +\
                                                            '/bs.status'

        """    initialization kutype register config"""
        self.project_name = self.kutype_register_info['project_name']
        self.database_kutype = self.kutype_register_info['database_kutype']
        self.use_mysql_tablename = self.kutype_register_info['use_mysql_tablename']
        self.load_mysql_interval = int(modules.Util.time_formate_conversion_to_s(\
                                self.kutype_register_info['load_mysql_interval']))
        self.monitor_strategy_public = \
                            self.kutype_register_info['monitor']['monitor_strategy_public']
        self.monitor_strategy_private = \
                            self.kutype_register_info['monitor']['monitor_strategy_private']

        """    initialization kutype monitor value"""
        self.ku_current_iteration = 0
        self.ku_current_cycle = 0
        """example: | 7 | wdna | swift | 32 | 12 | yq01-global | wdna=96 | 0 | 0 | 30 | 0 |"""
        self.ku_total_cycle = int(kutype_global_info['ygg_ku_global_conf'][0][3])
        self.ku_total_cycle_info = list()

        """    trick kutype -> build_env for monitor use"""
        self.ku_monitor_trick_type = str(kutype_global_info['ygg_ku_global_conf'][0][2])

    def __del__(self):
        """   clean env   """
        pass

    def validate(self):
        print 'kutype = %s,' % self.kutype_name

    def get_newest_bs_cursor(self, bs_iteration_cycle_info):
        """get newest bs cursor: iteration - cycle"""
        """bs_iteration_cycle_info: list() - [iteration,cycleid] , sort by cycleid"""

        """bs_current_newest_cursor: record newest iteration id and cycle id"""
        """bs_iteration_cycle_info : save total iteration info"""
        bs_current_newest_cursor = dict()
        iteration_cursor_current = 0
        cycle_cursor_current = 0
        iteration_cursor_next = 0
        cycle_cursor_next = 0
        iteration_cursor_last = 0
        cycle_cursor_last = 0
        count = 0
        bs_current_newest_cursor['iteration'] = 0
        bs_current_newest_cursor['cycle'] = 0

        '''
        for single_iteration_cycle in bs_iteration_cycle_info:
            single_iteration = str(single_iteration_cycle[0])
            single_cycle = str(single_iteration_cycle[1])

            bs_iteration_cycle_info[count].append(single_iteration)
            bs_iteration_cycle_info[count].append(single_cycle)
            count += 1
        '''

        """sort by iteration(1st) - cycleid(2nd)"""
        bs_iteration_cycle_info.sort(key=itemgetter(0, 1))
        iteration_cursor_current = int(bs_iteration_cycle_info[0][0])
        iteration_cursor_last = iteration_cursor_current
        cycle_cursor_current = int(bs_iteration_cycle_info[0][1])
        cycle_cursor_last = cycle_cursor_current

        for count in range(0, len(bs_iteration_cycle_info)):
            if cycle_cursor_current == (self.ku_total_cycle - 1):
                '''full amount mode'''
                ''' and roll mode, in the last cycle'''
                iteration_cursor_next = iteration_cursor_current + 1
                cycle_cursor_next = 0
            else:
                ''' roll mode'''
                iteration_cursor_next = iteration_cursor_current
                cycle_cursor_next = cycle_cursor_current + 1

            if (iteration_cursor_current == int(bs_iteration_cycle_info[count][0])) and\
                    (cycle_cursor_current == int(bs_iteration_cycle_info[count][1])):
                '''check condition'''
                if (count != (len(bs_iteration_cycle_info) -1)):
                    '''get the cursor last cursor, in order to handle missing of release db in the middle'''
                    iteration_cursor_last = iteration_cursor_current
                    cycle_cursor_last = cycle_cursor_current

                    iteration_cursor_current = iteration_cursor_next
                    cycle_cursor_current = cycle_cursor_next
                else:
                    '''normal exit'''
                    break
            else:
                '''missing of release db in the middle'''
                iteration_cursor_current = iteration_cursor_last
                cycle_cursor_current = cycle_cursor_last
                logging.error('[Kutype]=[' + self.kutype_name + ']' + ' newest iteration-cycle error!')
                break

        bs_current_newest_cursor['iteration'] = iteration_cursor_current
        bs_current_newest_cursor['cycle'] = cycle_cursor_current
        count += 1
        print bs_current_newest_cursor
        return bs_current_newest_cursor

    def get_behind_bs_iteration_cycle(self, load_mysql_table_name='ygg_job'):
        """get total cycle range """
        """Thinking:"""
        """     mode1: full mode, just get bs the latest iteration."""
        """     mode2: roll mode, consider the missing of release db in the middle"""

        """mysql_data_iteration_min: means bs data version"""
        """mysql_data_cycle_min: means bs db number"""
        range_iteration_min = 0
        range_iteration_max = 0
        range_cycle_min = 0
        range_cycle_max = 0

        bs_current_iteration = 0
        bs_current_cycle = 0
        build_succ_iteration_cycle= list()

        """get bs current iteration - cycle"""
        sql_sentence = 'select * from ' + load_mysql_table_name +\
        ' where kuType=\'' + self.ku_monitor_trick_type +\
        '\' and jobName regexp \'^end\' and jobStatus=\'1\' order by iterId DESC, cycleId DESC limit 1;'
        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                ' [' + self.thread_name + '] sql sentence: ' + sql_sentence + '\n')

        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
            load_mysql_table_name, sql_sentence)

        if mysql_return_data == '1':
            logging.error('get bs cursor mysql operating failed.')
            return 1

        bs_current_iteration = int(mysql_return_data[0][4])
        bs_current_cycle = int(mysql_return_data[0][5])

        """find current total cycle range"""
        if ((int(bs_current_cycle) == 0) and (self.ku_total_cycle == 1)) or\
                (int(bs_current_cycle) == (self.ku_total_cycle - 1)):
            """full amount mode"""
            """roll mode, and current cycle is 0."""
            range_iteration_min = int(bs_current_iteration)

            sql_sentence = 'select iterId,cycleId from ' + load_mysql_table_name +\
                ' where kuType=\'' + str(self.ku_monitor_trick_type) +\
                '\' and iterId=\'' + str(range_iteration_min) +\
                '\' and jobName regexp \'^end\' and jobStatus=\'1\' order by cycleId ASC;'
        else:
            """roll mode, and current cycle is not 0."""
            range_iteration_min = int(bs_current_iteration) - 1
            range_iteration_max = int(bs_current_iteration)
            range_cycle_min = int(bs_current_cycle) + 1
            range_cycle_max = int(bs_current_cycle)

            sql_sentence = 'select iterId,cycleId from ' + load_mysql_table_name +\
                ' where ( kuType=\'' + str(self.ku_monitor_trick_type) +\
                '\' and jobName regexp \'^end\' and jobStatus=\'1\' )' +\
                ' and (( iterId=\'' + str(range_iteration_min) +\
                '\' and cycleId>=\'' + str(range_cycle_min) +\
                '\' ) or ( iterId=\'' + str(range_iteration_max) +\
                '\' and cycleId<=\'' + str(range_cycle_max) +\
                '\' )) order by cycleId ASC;'

        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                ' [' + self.thread_name + '] get bs cursor sql sentence: ' + sql_sentence + '\n')
        build_succ_iteration_cycle = AccessMysqlData.load_mysql_data_by_table(\
            load_mysql_table_name, sql_sentence)

        if build_succ_iteration_cycle == '1':
            logging.error('get bs cursor mysql operating failed.')
            return 1

        bs_current_newest_cursor = self.get_newest_bs_cursor(build_succ_iteration_cycle)

        """print iteration and cycle id to status file"""
        status_content = ' - [' + self.kutype_name + '] - BS_NEWEST_ITERATION:'\
            + str(bs_current_newest_cursor['iteration']) + '\n'
        modules.Util.append_log_content_to_file(\
            self.kutype_monitor_iteration_file, status_content)
        status_content = ' - [' + self.kutype_name + '] - BS_NEWEST_CYCLE:'\
            + str(bs_current_newest_cursor['cycle']) + '\n'
        modules.Util.append_log_content_to_file(\
            self.kutype_monitor_cycle_file, status_content)

        return bs_current_newest_cursor

    def load_meta_data(self, load_mysql_all_table_name=None):
        """load meta config"""

        """get mysql data range"""
        """mysql_data_iteration_min: means bs data version"""
        """mysql_data_cycle_min: means bs db number"""
        range_iteration_min = 0
        range_iteration_max = 0
        range_cycle_min = 0
        range_cycle_max = 0

        """initialization self.ku_total_cycle_info value"""
        self.ku_total_cycle_info = list()

        if load_mysql_all_table_name is None:
            logging.error('load_mysql_all_table_name value is emputy!')
            return 1

        """load mysql data from register table name"""
        for load_mysql_single_table_name in load_mysql_all_table_name.split(';'):

            """get current iteration - cycle"""
            if load_mysql_single_table_name == 'ygg_job':

                """get current total cycle range"""
                bs_current_newest_cursor = self.get_behind_bs_iteration_cycle(\
                                            load_mysql_single_table_name)

                """load mysql data for strategy analysis"""
                sql_sentence = 'select * from ' + load_mysql_single_table_name +\
                ' where (kuType=\'' + str(self.ku_monitor_trick_type) +\
                '\') and ((iterId=\'' + str(bs_current_newest_cursor['iteration']) +\
                '\' and cycleId>=\'' + str(bs_current_newest_cursor['cycle']) +\
                '\') or ( iterId>\'' + str(bs_current_newest_cursor['iteration']) +\
                '\'));'
                if Config.load_agent_debug_level() >= 2:
                    modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [' + self.thread_name + '] sql sentence : [' + sql_sentence + ']\n')
                self.ku_total_cycle_info = AccessMysqlData.load_mysql_data_by_table(\
                    load_mysql_single_table_name, sql_sentence)

                if self.ku_total_cycle_info == '1':
                    logging.error('load mysql data operating failed.')
                    return 1
        return 0

    def load_public_strategy(self):
        """scan & check & load public strategy """

        """monitor_iterm: register monitor iterm"""
        """single_public_strategy: register public strategy"""
        """monitor_iterm_key: record register monitor iterm key"""
        """monitor_comparison_method: Record the comparison of key and value"""
        """monitor_iterm_value: record register monitor iterm value"""
        """analysis_return_value: record register monitor iterm value"""
        single_public_strategy = ""
        monitor_iterm = ""
        monitor_iterm_key = ""
        monitor_comparison_method = ""
        monitor_iterm_value = ""
        analysis_return_value = ""

        for single_public_strategy in self.monitor_strategy_public.keys():
            for monitor_iterm in re.split(r';\s*',\
                    self.monitor_strategy_public[single_public_strategy]):

                """get analysis strategy, monitor iterms for analysis"""
                monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
                monitor_comparison_method = modules.Util.extract_by_regex(\
                    '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
                monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[1]

                """start analysis"""
                analysis_return_value = PublicStrategySchedule.public_strategy_analysis(\
                    public_strategy_name=single_public_strategy, mon_iterm=monitor_iterm,\
                    metadata=self.ku_total_cycle_info, kutype_global_conf=self.kutype_global_info)

                """save key:value to status file"""
                modules.Util.append_log_content_to_file(self.kutype_monitor_agent_status_path +\
                '/' + str(single_public_strategy) + '.status', monitor_iterm_key + ':' +\
                    str(analysis_return_value) + '\n')
        return 0

    def load_private_strategy(self):
        """scan & check & load private strategy """
        single_private_strategy = ""
        monitor_iterm = ""
        monitor_iterm_key = ""
        monitor_comparison_method = ""
        monitor_iterm_value = ""
        analysis_return_value = ""

        for single_private_strategy in self.monitor_strategy_private.keys():
            for monitor_iterm in re.split(r';\s*',\
                    self.monitor_strategy_private[single_private_strategy]):

                """get analysis strategy, monitor iterms for analysis"""
                monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
                monitor_comparison_method = modules.Util.extract_by_regex(\
                    '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
                monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[1]

                """start analysis"""
                analysis_return_value = PrivateStrategySchedule.private_strategy_analysis(\
                    private_strategy_name=single_private_strategy, mon_iterm=monitor_iterm_key,\
                    metadata=self.ku_total_cycle_info, kutype_global_conf=self.kutype_global_info)

                """save key:value to status file"""
                modules.Util.append_log_content_to_file(self.kutype_monitor_agent_status_path +\
                '/' + str(single_private_strategy) + '.status', monitor_iterm_key + ':' +\
                    str(analysis_return_value) + '\n')
        return 0


    def run(self):
        """monitor agent main function"""
        log_content = ' - [' + self.thread_name + '] is starting.\n'
        modules.Util.append_log_content_to_file(self.kutype_monitor_agent_log_file, log_content)
        log_content = ' - [' + self.thread_name + '] - [START]\n'
        modules.Util.append_log_content_to_file(self.kutype_status_log_file, log_content)

        self.validate()
        while True:
            print "=================locak check======================"
            if threadLock.acquire(2):
                print self.kutype_name
                print datetime.datetime.now()
                self.load_meta_data(self.use_mysql_tablename)
                status_content = str(self.ku_total_cycle_info) + '\n'
                if Config.load_agent_debug_level() >= 4:
                    modules.Util.append_log_content_to_file(\
                            self.kutype_monitor_bs_file, status_content)
                self.load_public_strategy()
                self.load_private_strategy()
                GeneralOperation.clear_finished_build_info(self.kutype_global_info)
                threadLock.release()
                time.sleep(self.load_mysql_interval)
            else:
                logging.error('lock! lock! lock!')

    def stop(self):
        """stop monitor agent function"""
        log_content = ' - [' + self.thread_name + '] is stoping.\n'
        modules.Util.append_log_content_to_file(self.kutype_monitor_agent_log_file, log_content)
        log_content = ' - [' + self.thread_name + '] - [STOP]\n'
        modules.Util.append_log_content_to_file(self.kutype_status_log_file, log_content)
        return 0
        

        #time.sleep(self.kutype_register_info['load_mysql_interval'])
        #time.sleep(60)

    """father process"""
    def mon_child_process(self):
        """get child process status"""


if __name__ == "__main__":
    debug_instance = MonitorAgentStart()
    debug_instance.kutype_mon_start()
    print "Monitor Agent Running..."
