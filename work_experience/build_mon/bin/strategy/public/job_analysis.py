######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-04-25"
######################################

"""
job level analysis module
"""

import os
import sys
import logging
import json
import re
import datetime
import time

from AnalysisBase import AnalysisBaseClass

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

class JobOvertimeNum(AnalysisBaseClass):
    """analysis base"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(JobOvertimeNum, self).__init__(monitor_iterm, metadata, global_conf)

        """Initialization configure"""
        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]
        self.project_name = global_conf['ygg_ku_global_conf'][0][2]
        self.compass_domain = global_conf['ygg_ku_global_conf'][0][10]
        self.hadoop_cluster = global_conf['ygg_ku_global_conf'][0][9]
        self.kutype_job_conf = global_conf['ygg_job_conf']
        self.metadata = metadata
        self.monitor_iterm = monitor_iterm

        """Initialization analysis value"""
        """self.job_autofail_switch: """
        """    0: close """
        """    1: open """
        self.current_unix_time = 0
        self.job_lowsla_time_s = 0
        self.job_sla_time_s = 0
        self.overtime_job_num = 0
        self.job_autofail_switch = 0

        """Initialization failed exec"""
        self.failed_tool_top_dir = Config.callback_dir + '/fail-long-tail-task/'
        self.failed_bin_dir = self.failed_tool_top_dir + 'bin/'
        self.failed_bin = self.failed_bin_dir + 'job.py'

    def analysis(self):
        """Start analysis"""
        single_job_info = list()
        job_name = ""

        """
        +----------+------------+
        | statusId | statusName |
        +----------+------------+
        |        0 | notstarted |
        |        1 | success    |
        |        2 | running    |
        |        3 | failed     |
        |        4 | skipped    |
        |        5 | killed     |
        +----------+------------+
        """
        job_running_status = 2
        job_succ_status = 1
        job_current_status = 0
        job_start_time = 0
        job_used_time = 0

        for single_job_info in self.metadata:
            job_name = single_job_info[0]
            job_current_status = single_job_info[2]
            job_execid = str(single_job_info[9])
            job_start_time_datetime = str(single_job_info[7])

            if job_current_status == job_running_status:
                """get running job information"""
                for raw in range(0, len(self.kutype_job_conf)):
                    """Get timeout configuration"""
                    conf_regex_jobname = str(self.kutype_job_conf[raw][3])
                    job_name_regex = re.compile(conf_regex_jobname)

                    if job_name_regex.findall(job_name):
                        """Check if it times out"""
                        self.job_lowsla_time_s = self.kutype_job_conf[raw][5] * 60
                        self.job_sla_time_s = self.kutype_job_conf[raw][6] * 60
                        self.job_autofail_switch = self.kutype_job_conf[raw][8]
                        job_start_time = modules.Util.datetime_to_unixtime(single_job_info[7])
                        self.current_unix_time = int(re.split(r'\.', str(time.time()))[0])
                        job_used_time_s = self.current_unix_time - job_start_time

                        if job_used_time_s > self.job_sla_time_s:
                            """Record timeout information"""
                            job_used_time_h = job_used_time_s / 3600
                            job_used_time_h = ("%.2f" % job_used_time_h)
                            job_error_time = datetime.datetime.now()
                            check_exists_ret = GeneralOperation.check_and_insert_already_exists_job(\
                                            single_job_info, self.monitor_iterm,\
                                            'job_runningtime=' + str(job_used_time_h) + 'h',\
                                            str(job_error_time))
                            if check_exists_ret == 1:
                                logging.error('\
                                    [JobOvertime] insert new job info to ygg_monitor failed!')
                            self.overtime_job_num += 1

                            """callback function"""
                            if str(self.job_autofail_switch) == '0':
                                """0: means close auto failover function"""
                                continue
                            job_hadoop_url = single_job_info[10]
                            if job_hadoop_url is None:
                                exec_cmd = '[' + job_name + '] hadoop jobid is none.'
                            else:
                                """exec failover cmd"""
                                job_hadoop_jobid = re.split(r'jobid=', job_hadoop_url)[1]
                                job_cluster = self.hadoop_cluster
                                exec_cmd = 'python ' + self.failed_bin
                                exec_cmd = exec_cmd + ' -j ' + job_hadoop_jobid
                                exec_cmd = exec_cmd + ' -c ' + job_cluster
                                exec_cmd = exec_cmd + ' &'
                                print exec_cmd
                                os.system(exec_cmd)
                                print '--- fail over ok ---'

                                """record failover operating"""
                                """This should not use the AccessMysqlData class"""
                                """I should use the GeneralOperation class"""
                                """But......"""
                                time_now = datetime.datetime.now()
                                sql_sentence = 'update ygg_monitor set operator=\'build_bot\', ' +\
                                                'operatingTime=\'' + str(time_now) +'\', ' +\
                                                'operating=\'Failover ' + job_hadoop_jobid + '\'' +\
                                                'where execId=\'' + job_execid + '\' and ' +\
                                                'errorName=\'' + job_name + '\' and ' +\
                                                'errorStarttime=\'' + job_start_time_datetime +\
                                                '\' and currStatus=\'2\';'
                                check_exists_ret = AccessMysqlData.insert_mysql_data_by_table(\
                                                        'ygg_monitor', sql_sentence)
                                if check_exists_ret == 1:
                                    logging.error('\
                                        [JobOvertime] update bot fail info to ygg_monitor failed!')
                            if Config.load_agent_debug_level() >= 3:
                                modules.Util.append_log_content_to_file(\
                                            Config.debug_public_strategy_file,\
                                            ' [' + self.kutype_name +\
                                            '_kutype_auto_failed] record data: ' +\
                                            exec_cmd + '\n')
                        break

        return self.overtime_job_num


class StartAnalysis(object):
    """job level analysis class"""

    def __init__(self, mon_iterm, metadata=None, kutype_global_conf=None):
        """init """

        self.mon_iterm = mon_iterm
        self.monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[0]
        self.monitor_comparison_method = modules.Util.extract_by_regex(\
            '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[0]
        self.monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[1]

        self.meta_data = metadata
        self.kutype_global_conf = kutype_global_conf

    def start(self):
        """start method"""
        '''
        print "job - %s - start analysis!!!" % self.strategy_name
        '''

        if self.monitor_iterm_key == 'job_overtime_job_num':
            analysis_instance = JobOvertimeNum(\
                    self.mon_iterm, self.meta_data, self.kutype_global_conf)
        else:
            return 0

        return analysis_instance.analysis()


if __name__ == "__main__":
    debug_instance = StartAnalysis(strategy_name='job_analysis',\
                    mon_iterm='job_overtime_job_num', metadata='test')
    debug_instance.start()
