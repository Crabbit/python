######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-04-25"
######################################

"""
flow level analysis module
"""

import os
import sys
import logging
import json
import re
import datetime
import time

from AnalysisBase import AnalysisBaseClass
from AnalysisBase import GetFlowinfoByCursor

"""
import basic class
"""
sys.path.append("./../../")
import modules
from operator import itemgetter
from operator import attrgetter
from access_meta_data import AccessMysqlData
from access_meta_data import GeneralOperation
from load_config import Config

class FlowOvertimeNum(AnalysisBaseClass):
    """analysis base"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(FlowOvertimeNum, self).__init__(monitor_iterm, metadata, global_conf)

        """Initialization configure"""
        self.kutype_running_time = global_conf['ygg_ku_global_conf'][0][6]
        self.kutype_running_time_s = modules.Util.time_formate_conversion_to_s(\
                                        self.kutype_running_time)
        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]
        self.project_name = global_conf['ygg_ku_global_conf'][0][2]
        self.compass_domain = global_conf['ygg_ku_global_conf'][0][10]
        self.metadata = metadata
        self.monitor_iterm = monitor_iterm

        """Initialization analysis value"""
        self.current_unix_time = 0
        self.overtime_flow_num = 0

    def analysis(self):
        """Start analysis"""
        single_job_info = list()
        job_name = ""
        regex_start_job_flag = re.compile(r'download')
        regex_end_job_flag = re.compile(r'^end')

        """flow_iter_cycle_start_end_time: key:[iter_id_cycleid_(start|end)], value:[unixformat_time]"""
        flow_iter_cycle_start_end_time = dict()

        """flow information, for ygg monitor"""
        """  example: [ 'project', 'iterid', 'cycleid', 'flow_monitor', 'error_analysis', 'error_status',"""
        """             'flow_current_status', 'error_starttime', 'error_appear_time', 'project link',' flow link',   ]"""
        flow_information_list = list()
        project_link = self.compass_domain + '/manager?project='+\
                                self.project_name + '&flow=end#executions'

        for single_job_info in self.metadata:
            job_name = single_job_info[0]
            flag = ""

            """get all build process download job info"""
            """start: get the earliest start download job time for each cycle as the flow start time"""
            """end: get the end job time for each cycle as the flow end time"""
            if regex_start_job_flag.findall(job_name):
                flag = '_start'
                iteration_cursor = str(single_job_info[4])
                cycle_cursor = int(single_job_info[5])
                if str(single_job_info[7]) == 'None':
                    continue
                dateformat_time = single_job_info[7]
                unixformat_time = int(re.split(r'\.',\
                        str(time.mktime(dateformat_time.timetuple())))[0])

                dict_key = str(iteration_cursor) + '_' + str(cycle_cursor) + flag
                if (not flow_iter_cycle_start_end_time.has_key(dict_key)) or\
                    (unixformat_time < flow_iter_cycle_start_end_time[dict_key]):
                    flow_iter_cycle_start_end_time[dict_key] = unixformat_time
            elif (regex_end_job_flag.findall(job_name)) and (int(single_job_info[2]) == 1):
                flag = '_end'
                iteration_cursor = str(single_job_info[4])
                cycle_cursor = int(single_job_info[5])
                dateformat_time = single_job_info[7]
                unixformat_time = int(re.split(r'\.',\
                        str(time.mktime(dateformat_time.timetuple())))[0])

                dict_key = str(iteration_cursor) + '_' + str(cycle_cursor) + flag
                if (not flow_iter_cycle_start_end_time.has_key(dict_key)):
                    flow_iter_cycle_start_end_time[dict_key] = unixformat_time

        """ for sort by iteration then cycle"""
        """  [ iteration_cycle ] ---> [[iteration1, cycle1], [iteration2, cycle2], ...]"""
        dict_key_list = list()

        for count in range(0, len(flow_iter_cycle_start_end_time.keys())):
            iteration_cursor_current = int(\
                        re.split(r'_', flow_iter_cycle_start_end_time.keys()[count])[0])
            cycle_cursor_current = int(\
                        re.split(r'_', flow_iter_cycle_start_end_time.keys()[count])[1])
            """In order to get heavy: start / end flasg"""
            list_cursor_current = [iteration_cursor_current, cycle_cursor_current]
            if list_cursor_current not in dict_key_list:
                dict_key_list.append(list_cursor_current)
        dict_key_list.sort(key=itemgetter(0, 1))

        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                ' [' + self.kutype_name + '_flow_overtime_num] temp data: ' +\
                str(flow_iter_cycle_start_end_time) + '\n')

        """find the incomplete flow, and calculate whether the timeout"""
        """if the timeout expires, the counter is incremented"""
        for iteration_cycle_cursor in dict_key_list:
            """get current iteration and cycle id"""
            iteration_cursor_current = str(iteration_cycle_cursor[0])
            cycle_cursor_current = str(iteration_cycle_cursor[1])

            dict_start_key = iteration_cursor_current + '_' + cycle_cursor_current + '_start'
            dict_end_key = iteration_cursor_current + '_' + cycle_cursor_current + '_end'
            iter_cycle_cusror_start_time = int(flow_iter_cycle_start_end_time[dict_start_key])

            """calculating time"""
            self.current_unix_time = int(re.split(r'\.', str(time.time()))[0])
            running_time_s = iter_cycle_cusror_start_time + self.kutype_running_time_s -\
                            self.current_unix_time
            used_time_h = (self.kutype_running_time_s - running_time_s) / 3600.0
            used_time_h = ("%.2f" % used_time_h)

            """record flow information"""
            """ This realization is not the best way, forced by time"""
            get_flow_info_instance = GetFlowinfoByCursor(\
                self.metadata, iteration_cycle_cursor, iter_cycle_cusror_start_time)
            flow_information_list = get_flow_info_instance.get_flow_key_information()
            exec_id = flow_information_list[3]
            flow_link = self.compass_domain + '/executor?execid='
            flow_link = flow_link + str(exec_id) + '#jobslist'

            flow_information_list.append('flow_monitor')
            flow_information_list.append(self.monitor_iterm)
            flow_information_list.append('flow-usedtime=' + str(used_time_h) + 'h')
            flow_information_list.append('2')
            flow_information_list.append(str(datetime.datetime.now()))
            flow_information_list.append(project_link)
            flow_information_list.append(flow_link)

            if Config.load_agent_debug_level() >= 3:
                modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                    ' [' + self.kutype_name + '_flow_overtime_num] temp data: ' +\
                    str(flow_information_list) + '\n')

            """if flow not done"""
            if (not flow_iter_cycle_start_end_time.has_key(dict_end_key)):

                """if overtime, record error info"""
                if running_time_s <= 0:
                    self.overtime_flow_num += 1
                    check_exists_ret = GeneralOperation.check_and_update_already_exists_flow(\
                                                                        flow_information_list)
                    if check_exists_ret == 255:
                        GeneralOperation.insert_ygg_monitor_flow(flow_information_list)
            else:
                """if flow done, update end time stamp"""
                flow_information_list[8] = '1'
                flow_information_list[9] = modules.Util.unixtime_to_datetime(\
                                            flow_iter_cycle_start_end_time[dict_end_key])
                GeneralOperation.check_and_update_already_exists_flow(flow_information_list)

        return self.overtime_flow_num


class StartAnalysis(object):
    """flow level analysis class"""

    def __init__(self, mon_iterm, metadata=None, kutype_global_conf=None):
        """init """

        self.mon_iterm = mon_iterm
        """get analysis strategy, monitor iterms for analysis"""
        self.monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[0]

        self.meta_data = metadata
        self.kutype_global_conf = kutype_global_conf
        pass

    def start(self):
        """start method"""
        """
        print "flow - %s - start analysis!!!" % self.strategy_name
        """

        if self.monitor_iterm_key == 'flow_overtime_num':
            analysis_instance = FlowOvertimeNum(\
                    self.mon_iterm, self.meta_data, self.kutype_global_conf)
        else:
            return 0

        return analysis_instance.analysis()


if __name__ == "__main__":
    ku_global_conf_list = dict()
    ku_global_conf = Config.load_mysql_global_kutype_conf()
    kutype = 'wp'

    for raw in range(0, len(ku_global_conf)):
        sql_sentence = 'select * from ' + ku_global_conf[raw]['table'] + \
                        ' where kuType=\'' + kutype + '\';'
        ku_global_conf_list[ku_global_conf[raw]['data_name']] = \
            AccessMysqlData.load_mysql_data_by_conf(ku_global_conf[raw], sql_sentence)
    kutype_global_conf = ku_global_conf_list

    debug_instance = StartAnalysis('flow_overtime_num', 'test', kutype_global_conf)
    debug_instance.start()
