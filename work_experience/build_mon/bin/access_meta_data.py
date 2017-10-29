######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-03-24"
######################################

"""
This module provide unified access to metadata interfaces
"""

import os
import sys
import MySQLdb
import logging
import time
import datetime
from load_config import Config

import modules

logging.basicConfig(filename='../log/access_meta_data.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class AccessMysqlData(object):
    """access meta data class"""

    @staticmethod
    def operating_mysql_data_by_conf(conf_doc=None, sql_sentence=None):
        """load mysql data by conf doc and sql sentence"""
        mysql_return_info_list = list()

        mysql_host = conf_doc['host']
        mysql_user = conf_doc['user']
        mysql_passwd = conf_doc['passwd']
        mysql_database = conf_doc['database']
        mysql_table = conf_doc['table']

        failed_count = 0

        while 1:
            try:
                mysql_db = MySQLdb.connect(mysql_host, mysql_user, mysql_passwd, mysql_database)
            except:
                logging.error('mysql host: ' + str(mysql_host) + 'connect failed!')
                failed_count += 1
                time.sleep(2)
                if failed_count > 5:
                    return 1
                else:
                    continue
                
            mysql_cursor = mysql_db.cursor()

            try:
                mysql_cursor.execute(sql_sentence)
                mysql_db.commit()
                break
            except:
                logging.error('mysql operation failed! sql: ' + sql_sentence)
                mysql_db.rollback()
                failed_count += 1
                time.sleep(2)
                if failed_count > 5:
                    return 1
        results = mysql_cursor.fetchall()
        mysql_db.close()

        mysql_return_info_list = [[] for i in range(len(results))]

        for line in range(0, len(results)):
            for raw in range(0, len(results[line])):
                mysql_return_info_list[line].append(results[line][raw])
        return mysql_return_info_list

    @staticmethod
    def load_mysql_data_by_table(table_name=None, sql_sentence=None):
        """load mysql data by table and sql sentence"""
        if sql_sentence is None:
            logging.error('sql_sentence value is emputy!')
            return 1

        global_conf = Config.load_mysql_global_kutype_conf()
        metadata_conf = Config.load_mysql_kutype_metadata_conf()

        """load from global conf"""
        for raw in range(0, len(global_conf)):
            if table_name == global_conf[raw]['table']:
                return AccessMysqlData.operating_mysql_data_by_conf(\
                                    global_conf[raw], sql_sentence)

        """load from metadata conf"""
        for raw in range(0, len(metadata_conf)):
            if table_name == metadata_conf[raw]['table']:
                return AccessMysqlData.operating_mysql_data_by_conf(\
                                    metadata_conf[raw], sql_sentence)
        return 1

    @staticmethod
    def insert_mysql_data_by_table(table_name=None, sql_sentence=None):
        """load mysql data by table and sql sentence"""
        if sql_sentence is None:
            logging.error('sql_sentence value is emputy!')
            return 1

        metadata_conf = Config.load_mysql_kutype_metadata_conf()

        for raw in range(0, len(metadata_conf)):
            if table_name == metadata_conf[raw]['table']:
                if Config.load_agent_debug_level() >= 2:
                    modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [insert_mysql_table] sql sentence: ' + sql_sentence + '\n')
                return AccessMysqlData.operating_mysql_data_by_conf(\
                                    metadata_conf[raw], sql_sentence)
        return 1


class GeneralOperation(object):
    """encapsulates several common operations on mysql"""

    @staticmethod
    def insert_ygg_monitor_job(single_job_info, job_error_analysis, job_errorstatus, job_error_appear_time = 'null'):
        """insert the abnormal information into the ygg_monitor"""

        """Initialization abnormal job information"""
        project_name = single_job_info[6]
        iteration_id = str(single_job_info[4])
        cycle_id = str(single_job_info[5])
        exec_id = str(single_job_info[9])
        job_name = single_job_info[0]
        job_current_status = str(single_job_info[2])
        job_start_time_datetime = single_job_info[7]
        job_hadoop_link = single_job_info[10]
        job_stderr_link = single_job_info[11]

        if job_error_appear_time == 'null':
            job_error_appear_time = single_job_info[8]

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'

        sql_sentence = 'insert into ' + ygg_monitor_table_name + '(projectName, iterId, cycleId,\
                        execId, errorName, errorAnalysis, errorStatus, currStatus, \
                        errorStarttime, errorAppeartime, jobHadoopLink, jobStderrLink) values (\'' +\
                        project_name + '\', \'' + iteration_id + '\', \'' + cycle_id + '\', \'' +\
                        exec_id + '\', \'' + job_name + '\', \'' + str(job_error_analysis) +\
                        '\', \'' + str(job_errorstatus) + '\', \'' + job_current_status + '\', \'' \
                        + str(job_start_time_datetime) + '\', \'' + job_error_appear_time + '\', \''\
                        + job_hadoop_link + '\', \'' + job_stderr_link + '\');'

        return AccessMysqlData.insert_mysql_data_by_table(ygg_monitor_table_name, sql_sentence)


    @staticmethod
    def insert_ygg_monitor_flow(single_flow_info):
        """insert the abnormal information into the ygg_monitor"""

        """Initialization abnormal job information"""
        project_name = single_flow_info[0]
        iteration_id = str(single_flow_info[1])
        cycle_id = str(single_flow_info[2])
        exec_id = str(single_flow_info[3])
        error_name = str(single_flow_info[5])
        flow_error_analysis = str(single_flow_info[6])
        flow_error_status = str(single_flow_info[7])
        flow_current_status = str(single_flow_info[8])
        flow_start_time_datetime = str(single_flow_info[4])
        flow_error_appear_time = str(single_flow_info[9])
        flow_project_link= single_flow_info[10]
        flow_link = single_flow_info[11]

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'

        sql_sentence = 'insert into ' + ygg_monitor_table_name + '(projectName, iterId, cycleId,\
                        execId, errorName, errorAnalysis, errorStatus, currStatus, \
                        errorStarttime, errorAppeartime, jobHadoopLink, jobStderrLink) values (\'' +\
                        project_name + '\', \'' + iteration_id + '\', \'' + cycle_id + '\', \'' +\
                        exec_id + '\', \'' + error_name + '\', \'' + str(flow_error_analysis) +\
                        '\', \'' + str(flow_error_status) + '\', \'' + flow_current_status + '\', \'' \
                        + str(flow_start_time_datetime) + '\', \'' + flow_error_appear_time + '\', \'' + \
                        flow_project_link + '\', \'' + flow_link + '\');'

        return AccessMysqlData.insert_mysql_data_by_table(ygg_monitor_table_name, sql_sentence)


    @staticmethod
    def check_and_insert_already_exists_job(single_job_info, job_error_analysis,\
                                            job_errorstatus, job_error_appear_time):
        """check_and_update_already_exists_job"""
        """check and update exist job info"""
        """exist conditions:"""
        """         project_name, iteration_id, cycle_id, exec_id, job_name, job_error_analysis"""
        """Initialization check job information"""
        project_name = single_job_info[6]
        iteration_id = str(single_job_info[4])
        cycle_id = str(single_job_info[5])
        if str(single_job_info[8]) == 'None':
            """some abnormal: start time = none, end time = none"""
            single_job_info[8] = str(datetime.datetime.now())
        if str(single_job_info[7]) == 'None':
            """job status: ready -> kill"""
            single_job_info[7] = str(single_job_info[8])
        job_start_time = str(single_job_info[7])
        exec_id = str(single_job_info[9])
        job_name = single_job_info[0]

        """update information:"""
        """         job_current_status, job_errorstatus, job_error_appear_time"""
        job_current_status = str(single_job_info[2])

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'

        sql_sentence = 'select * from ' + ygg_monitor_table_name + ' where projectName=\'' +\
                        project_name + '\' and iterId=\'' + iteration_id + '\' and cycleId=\'' +\
                        cycle_id + '\' and execId=\'' + exec_id + '\' and errorName=\'' + job_name +\
                        '\' and errorAnalysis=\'' + job_error_analysis + '\' and errorStarttime=\''\
                        + job_start_time +'\';'

        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [check_exists_job] sql sentence: ' + sql_sentence + '\n')
        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

        if mysql_return_data:
            '''
            sql_sentence = 'update ygg_monitor set errorStatus=\'' + job_errorstatus +\
                            '\', currStatus=\'' + job_current_status +\
                            '\' where projectName=\'' + project_name +\
                            '\' and execId=\'' + exec_id + '\' and errorName=\'' + job_name +\
                            '\' and errorAnalysis=\'' + job_error_analysis + '\';'
            return AccessMysqlData.insert_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)
            '''
            return 0
        else:
            return GeneralOperation.insert_ygg_monitor_job(single_job_info, job_error_analysis,\
                                                            job_errorstatus, job_error_appear_time)


    @staticmethod
    def check_and_update_already_exists_flow(single_flow_info):
        """check and update exist flow info"""
        """exist conditions:"""
        """         project_name, iteration_id, cycle_id, exec_id, error_name,  flow_error_analysis """
        """Initialization check flow information"""
        project_name = single_flow_info[0]
        iteration_id = str(single_flow_info[1])
        cycle_id = str(single_flow_info[2])
        exec_id = str(single_flow_info[3])
        flow_error_analysis = single_flow_info[6]
        error_name = 'flow_monitor'

        """update information:"""
        """         flow_current_status, flow_errorstatus, flow_errortime_appeartime"""
        flow_error_status = str(single_flow_info[7])
        flow_current_status = str(single_flow_info[8])
        flow_error_appeartime = str(single_flow_info[9])

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'

        sql_sentence = 'select * from ' + ygg_monitor_table_name + ' where projectName=\'' +\
                        project_name + '\' and iterId=\'' + iteration_id + '\' and cycleId=\'' +\
                        cycle_id + '\' and execId=\'' + exec_id + '\' and errorName=\'' +\
                        error_name + '\' and errorAnalysis=\'' + flow_error_analysis + '\';'

        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [check_exists_flow] sql sentence: ' + sql_sentence + '\n')
        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

        if mysql_return_data:
            sql_sentence = 'update ygg_monitor set errorStatus=\'' + flow_error_status +\
                            '\', currStatus=\'' + flow_current_status +\
                            '\' where projectName=\'' + project_name +\
                            '\' and execId=\'' + exec_id + '\' and errorName=\'' + error_name +\
                            '\' and errorAnalysis=\'' + flow_error_analysis + '\';'
            return AccessMysqlData.insert_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)
        else:
            return 255


    @staticmethod
    def check_and_update_already_exists_kutype(single_kutype_info):
        """check and update exist kutype info"""
        """exist conditions:"""
        """         project_name, iteration_id, cycle_id, exec_id, error_name,  kutype_error_analysis """
        """Initialization check kutype information"""
        project_name = single_kutype_info[0]
        iteration_id = str(single_kutype_info[1])
        cycle_id = str(single_kutype_info[2])
        exec_id = str(single_kutype_info[3])
        kutype_error_analysis = single_kutype_info[6]
        error_name = 'kutype_monitor'

        """update information:"""
        """         kutype_current_status, kutype_errorstatus, kutype_errortime_appeartime"""
        kutype_error_status = str(single_kutype_info[7])
        kutype_current_status = str(single_kutype_info[8])
        kutype_error_appeartime = str(single_kutype_info[9])

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'

        sql_sentence = 'select * from ' + ygg_monitor_table_name + ' where projectName=\'' +\
                        project_name + '\' and iterId=\'' + iteration_id + '\' and cycleId=\'' +\
                        cycle_id + '\' and execId=\'' + exec_id + '\' and errorName=\'' +\
                        error_name + '\' and errorAnalysis=\'' + kutype_error_analysis + '\';'

        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [check_exists_kutype_check] sql sentence: ' + sql_sentence + '\n')
        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

        if mysql_return_data:
            sql_sentence = 'update ygg_monitor set errorStatus=\'' + kutype_error_status +\
                            '\', currStatus=\'' + kutype_current_status +\
                            '\' where projectName=\'' + project_name +\
                            '\' and execId=\'' + exec_id + '\' and errorName=\'' + error_name +\
                            '\' and errorAnalysis=\'' + kutype_error_analysis +\
                            '\' and iterId=\'' + iteration_id + '\'and cycleId=\'' + cycle_id + '\';'
            if Config.load_agent_debug_level() >= 2:
                modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                            ' [check_exists_kutype_update] sql sentence: ' + sql_sentence + '\n')
            return AccessMysqlData.insert_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)
        else:
            return 255


    @staticmethod
    def clear_finished_build_info(global_info):
        """clear the abnormal information in the ygg_monitor table"""
        """ kutype & flow level:"""
        """     Thinking: with bs newest iteration-cycle as the limit, update the information before this limit."""
        """job level:"""
        """     Thinking: update the newest job status"""
        """                 if the newest job status is succ, then update all"""

        kutype_global_info = global_info
        kutype_name = kutype_global_info['ygg_ku_global_conf'][0][1]
        project_name = kutype_global_info['ygg_ku_global_conf'][0][2]

        """get bs newest iteration and cycle id"""
        """iteration_cycle_cursor: record bs newest iteration - cycle, for get kutype information by GetFlowinfoByCursor method"""
        kutype_status_dir = Config.status_dir + '/' + kutype_name
        kutype_bs_newest_iteration_file= kutype_status_dir + '/bs_newest_iteration.status'
        kutype_bs_newest_cycle_file = kutype_status_dir + '/bs_newest_cycle.status'
        bs_newest_iteration = modules.Util.get_newest_value_by_key_file(\
                kutype_bs_newest_iteration_file, 'BS_NEWEST_ITERATION')
        bs_newest_cycle = modules.Util.get_newest_value_by_key_file(\
                kutype_bs_newest_cycle_file, 'BS_NEWEST_CYCLE')

        """Initialization abnormal mysql table name"""
        ygg_monitor_table_name = 'ygg_monitor'
        single_job_info = list()

        """get ygg monitor information"""
        """     flow_monitor: flow level abnormal"""
        """     kutype_monitor: kutype level abnormal"""
        sql_sentence = 'select * from ' + ygg_monitor_table_name + ' where currStatus!=1 and ' +\
                        'projectName=\'' + project_name + '\' and errorName!=\'flow_monitor\' and '\
                        'errorName!=\'kutype_monitor\''
        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [clear_finished_build_info_check] sql sentence: ' + sql_sentence + '\n')
        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

        """check and update job information"""
        for single_job_info in mysql_return_data:
            abnormal_job_project = single_job_info[1]
            abnormal_job_iteratiom = str(single_job_info[2])
            abnormal_job_cycle = str(single_job_info[3])
            abnormal_job_execid = str(single_job_info[4])
            abnormal_job_name = single_job_info[5]
            abnormal_job_analysis = single_job_info[6]

            """get newest job info"""
            sql_sentence = 'select * from ygg_job where jobName=\'' + abnormal_job_name +\
                            '\' and iterId=\'' + abnormal_job_iteratiom + '\' and cycleId=\'' +\
                            abnormal_job_cycle + '\' and kutype=\'' + abnormal_job_project +\
                            '\' and execid=\'' + abnormal_job_execid + '\';'

            if Config.load_agent_debug_level() >= 2:
                modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [clear_finished_build_info_check] sql sentence: ' + sql_sentence + '\n')
            mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    'ygg_job', sql_sentence)
            if mysql_return_data:
                abnormal_job_curr_status = mysql_return_data[0][2]
                abnormal_job_curr_hadoop_link = mysql_return_data[0][10]
                abnormal_job_curr_stderr_link = mysql_return_data[0][11]
                

                """update abnormal job info"""
                error_appear_time = datetime.datetime.now()
                sql_sentence = 'update ' + ygg_monitor_table_name + ' set currStatus=\''\
                    + str(abnormal_job_curr_status) + '\', errorAppeartime=\''\
                    + str(error_appear_time) + '\', jobHadoopLink=\'' +\
                    abnormal_job_curr_hadoop_link + '\', jobStderrLink=\'' +\
                    abnormal_job_curr_stderr_link + '\' where currStatus!=1 and projectName=\''\
                    + project_name + '\' and errorAnalysis=\'' + abnormal_job_analysis +\
                    '\' and execId=\'' + abnormal_job_execid + '\' and errorName=\'' +\
                    abnormal_job_name + '\' and iterId=\'' + abnormal_job_iteratiom +\
                    '\' and cycleId=\'' + abnormal_job_cycle + '\';'

                if Config.load_agent_debug_level() >= 2:
                    modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                    ' [clear_finished_build_info_update_job] sql sentence: ' + sql_sentence + '\n')

                mysql_return_data = AccessMysqlData.insert_mysql_data_by_table(\
                                        ygg_monitor_table_name, sql_sentence)
                if mysql_return_data == 1:
                    return 1


        """update kutype and flow info"""
        error_appear_time = datetime.datetime.now()
        sql_sentence = 'update ' + ygg_monitor_table_name + ' set currStatus=1, errorAppeartime=\''\
                        + str(error_appear_time) + '\' where (currStatus!=1 and projectName=\''\
                        + project_name + '\') and ((iterId<\'' + bs_newest_iteration +\
                        '\') or (iterId=\'' + bs_newest_iteration +\
                        '\' and cycleId<=\'' + bs_newest_cycle + '\'))'

        if Config.load_agent_debug_level() >= 2:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                        ' [clear_finished_build_info_update_flow] sql sentence: ' + sql_sentence + '\n')
        mysql_return_data = AccessMysqlData.load_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

        return AccessMysqlData.insert_mysql_data_by_table(\
                                    ygg_monitor_table_name, sql_sentence)

if __name__ == "__main__":

    single_job_info = list()
    raw = 0

    global_conf = Config.load_mysql_global_kutype_conf()
    metadata_conf = Config.load_mysql_kutype_metadata_conf()
    '''
    debug_info = AccessMysqlData.load_mysql_data_by_table(\
        'ygg_job', 'select * from ygg_job where kuType=\'swift\' and iterId=\'14\' and cycleId=\'22\' and errorName regexp \'download*\';')

    for single_job_info in debug_info:
        print single_job_info
        job_error_analysis = 'kutype_failed_job_num<1'
        nowtime = str(datetime.datetime.now())
        GeneralOperation.check_and_update_already_exists_job(single_job_info, job_error_analysis, job_error_analysis, nowtime)
        GeneralOperation.insert_ygg_monitor_job(single_job_info, job_error_analysis, 'job_failed', '2017-05-10 17:24:13')

    print AccessMysqlData.insert_mysql_data_by_table('ygg_monitor', 'INSERT INTO ygg_monitor \
        (projectName, iterId, cycleId, errorName, errorAnalysis, errorStatus, currStatus,\
        jobStarttime, jobErrortime, jobLink, operating) VALUES (\'wdna\', \'14\', \'22\',\
         \'wdna-2:call-dew\', \'job_overtime_job_num>0\', \'overtime\', \'1\',\
         \'2017-05-09 13:22:13\', \'2017-05-09 14:22:13\', \'http://yq01-build-compass10.yq01:8081/executor?execid=41543&job=wdna-2:call-dew\',\
         \'fail\');')
    '''
