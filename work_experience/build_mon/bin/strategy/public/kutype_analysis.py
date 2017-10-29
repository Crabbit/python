######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-04-25"
######################################

"""
kutype level analysis module
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
import modules
"""
sys.path.append("./../../")
import modules
from operator import itemgetter
from operator import attrgetter
from access_meta_data import AccessMysqlData
from access_meta_data import GeneralOperation
from load_config import Config

class KutypeRunningFlowNum(AnalysisBaseClass):
    """kutype running job analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(KutypeRunningFlowNum, self).__init__(monitor_iterm, metadata, global_conf)

        self.metadata = metadata

    def analysis(self):
        """Start KutypeRunningJobNum analysis"""
        single_job_info = list()
        compass_exec_id_list = dict()
        single_exec_id = 0
        job_name = ""
        job_status = 0
        total_running_flow_count = 0

        """start analysis"""
        for single_job_info in self.metadata:
            single_exec_id = single_job_info[9]
            if single_exec_id not in compass_exec_id_list.keys():
                compass_exec_id_list[single_exec_id] = ""

            job_name = single_job_info[0]
            job_status = single_job_info[2]
            if (job_name == "end") and (job_status == 1):
                compass_exec_id_list[single_exec_id] = 'end'

        for single_exec_id in compass_exec_id_list.keys():
            if compass_exec_id_list[single_exec_id] != 'end':
                total_running_flow_count += 1

        return total_running_flow_count


class KutypeRunningJobNum(AnalysisBaseClass):
    """kutype running floe analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(KutypeRunningJobNum, self).__init__(monitor_iterm, metadata, global_conf)

        self.metadata = metadata
        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]
        
    def analysis(self):
        """Start KutypeRunningFlowNum analysis"""
        single_job_info = list()
        single_job_status = 0
        total_running_job_count = 0

        """
        +----------+------------+
        | statusId | statusName |
        +----------+------------+
        |        0 | notstarted |
        |        1 | success    |
        |        2 | running    |
        |        3 | failed     |
        |        4 | skipped    |
        +----------+------------+
        """
        job_running_status = 2
        job_name_regex = re.compile(self.kutype_name)

        """start analysis"""
        """for multiple kutype uses one build env"""
        for single_job_info in self.metadata:
            single_job_status = single_job_info[2]
            if (job_name_regex.findall(single_job_info[0])) and\
                    (single_job_status == job_running_status):
                total_running_job_count += 1

        if total_running_job_count == 0:
            for single_job_info in self.metadata:
                single_job_status = single_job_info[2]
                if (single_job_status == job_running_status):
                    total_running_job_count += 1
            

        return total_running_job_count


class KutypeFailedFlowNum(AnalysisBaseClass):
    """kutype failed flow analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(KutypeFailedFlowNum, self).__init__(monitor_iterm, metadata, global_conf)

    def analysis(self):
        """Start KutypeFailedFlowNum analysis"""
        print 'Start KutypeFailedFlowNum analysis'
        return 0


class KutypeFailedJobNum(AnalysisBaseClass):
    """kutype failed flow analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(KutypeFailedJobNum, self).__init__(monitor_iterm, metadata, global_conf)

        """Initialization argv value"""
        """get analysis strategy, monitor iterms for analysis"""
        self.monitor_iterm = monitor_iterm
        self.monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
        self.monitor_comparison_method = modules.Util.extract_by_regex(\
            '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[0]
        self.monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', monitor_iterm)[1]
        self.metadata = metadata
        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]

        """Initialization status dir"""
        self.kutype_status_dir = Config.status_dir + '/' + self.kutype_name
        self.single_public_strategy = 'kutype_analysis'


    def analysis(self):
        """Start KutypeFailedJobNum analysis"""
        single_job_info = list()
        single_job_status = 0
        single_job_name = ""
        failed_job_name_list = ""
        total_failed_job_count = 0

        """
        +----------+------------+
        | statusId | statusName |
        +----------+------------+
        |        0 | notstarted |
        |        1 | success    |
        |        2 | running    |
        |        3 | failed     |
        |        4 | skipped    |
        +----------+------------+
        """
        job_failed_status = 3
        job_name_regex = re.compile(self.kutype_name)

        """start analysis"""
        for single_job_info in self.metadata:
            single_job_status = single_job_info[2]
            single_job_name = single_job_info[0]
            '''
            if (job_name_regex.findall(single_job_info[0])) and\
                    single_job_status == job_failed_status:
            '''
            """Record failed job information"""
            if single_job_status == job_failed_status:
                job_error_time = single_job_info[8]
                if not job_error_time:
                    job_error_time = datetime.datetime.now()
                failed_job_name_list = single_job_name + '; ' + failed_job_name_list
                check_exists_ret = GeneralOperation.check_and_insert_already_exists_job(\
                    single_job_info, self.monitor_iterm, 'job_failed', str(job_error_time))
                if check_exists_ret == 1:
                    logging.error('insert new job info to ygg_monitor failed!')
                total_failed_job_count += 1

        """save key:value to status file"""
        if total_failed_job_count == 0:
            failed_job_name_list = 'None'
        else:
            modules.Util.append_log_content_to_file(self.kutype_status_dir +\
            '/' + str(self.single_public_strategy) + '.status', 'kutype_failed_job_list:' +\
                str(failed_job_name_list) + '\n')


        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                        ' [' + self.kutype_name + '_kutype_failed_job_num] temp data: ' +\
                        failed_job_name_list + '\n')

        return total_failed_job_count

        return 0


class KutypeCoverCountDown(AnalysisBaseClass):
    """kutype cover tount down analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        super(KutypeCoverCountDown, self).__init__(monitor_iterm, metadata, global_conf)

        """Thinking: bs latest cycle page time - now time < coverd_time"""
        """  |------start download page--------------------------end--------------------------------start download page============now|"""
        """  |---------------|----------------------------------------------cover time----------------------------------------------|"""
        """global_conf: type: dict()"""
        """             data from monitor.json/mysql/kutype_global_conf_table/ key:data_name, value:ygg_ku_global_conf"""
        """             data example: {u'ygg_ku_global_conf': [[7L, 'wdna', 'swift', 32L, 12L, 28L, 'yq01-global', 'wdna=96', '0', '0', 30L, 0L]]}"""

        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]
        self.database_kutype_name = global_conf['ygg_ku_global_conf'][0][2]
        self.kutype_coverd_time = global_conf['ygg_ku_global_conf'][0][7]
        self.kutype_coverd_time_s = modules.Util.time_formate_conversion_to_s(\
                                    self.kutype_coverd_time)
        self.kutype_coverd_buffer = global_conf['ygg_ku_global_conf'][0][8]
        self.kutype_coverd_buffer_s = modules.Util.time_formate_conversion_to_s(\
                                    self.kutype_coverd_buffer)
        self.compass_domain = global_conf['ygg_ku_global_conf'][0][10]
        self.project_name = global_conf['ygg_ku_global_conf'][0][2]
        self.monitor_iterm = monitor_iterm

        """get bs newest iteration and cycle id"""
        """self.iteration_cycle_cursor: record bs newest iteration - cycle, for get kutype information by GetFlowinfoByCursor method"""
        self.kutype_status_dir = Config.status_dir + '/' + self.kutype_name
        self.kutype_bs_newest_iteration_file= self.kutype_status_dir + '/bs_newest_iteration.status'
        self.kutype_bs_newest_cycle_file = self.kutype_status_dir + '/bs_newest_cycle.status'
        self.bs_newest_iteration = modules.Util.get_newest_value_by_key_file(\
                self.kutype_bs_newest_iteration_file, 'BS_NEWEST_ITERATION')
        self.bs_newest_cycle = modules.Util.get_newest_value_by_key_file(\
                self.kutype_bs_newest_cycle_file, 'BS_NEWEST_CYCLE')
        self.iteration_cycle_cursor = [self.bs_newest_iteration, self.bs_newest_cycle]

        """get bs newest build env info"""
        sql_sentence = 'select * from ygg_job' +\
            ' where kuType=\'' + str(self.database_kutype_name) +\
            '\' and iterId=\'' + str(self.bs_newest_iteration) + \
            '\' and cycleId=\'' + str(self.bs_newest_cycle) + \
            '\' and jobName regexp \'download\''
        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_sql_sentence_file,\
                ' [' + self.kutype_name + '_' + self.kutype_name + \
                '_cover_countdown] sql sentence: ' + sql_sentence + '\n')
        self.metadata = AccessMysqlData.load_mysql_data_by_table('ygg_job', sql_sentence)

        """bs newest page time"""
        self.bs_newest_page_unix_time = 0
        self.current_unix_time = 0

    def calculate_cover_countdown(self):
        """Initialization record abnormal kutype information"""
        project_link = self.compass_domain + '/manager?project='+\
                                self.project_name + '&flow=end#executions'
        flow_link = self.compass_domain + '/executor?execid='

        """Calculate the coverage countdown"""
        self.current_unix_time = int(re.split(r'\.', str(time.time()))[0])
        countdown_time_s = self.bs_newest_page_unix_time + self.kutype_coverd_time_s\
                            - self.current_unix_time
        countdown_time_h = countdown_time_s / 3600.0
        countdown_time_h = ("%.2f" % countdown_time_h)
        countdown_minus_buffer_s = countdown_time_s - self.kutype_coverd_buffer_s

        """record abnormal kutype information"""
        get_kutype_info_instance = GetFlowinfoByCursor(self.metadata,\
                             self.iteration_cycle_cursor, self.bs_newest_page_unix_time)
        kutype_information_list = get_kutype_info_instance.get_flow_key_information()
        exec_id = kutype_information_list[3]
        flow_link = flow_link + str(exec_id) + '#jobslist'

        kutype_information_list.append('kutype_monitor')
        kutype_information_list.append(self.monitor_iterm)
        kutype_information_list.append('kutype-cover-countdown=' + str(countdown_time_h) + 'h')
        kutype_information_list.append('2')
        kutype_information_list.append(str(datetime.datetime.now()))
        kutype_information_list.append(project_link)
        kutype_information_list.append(flow_link)

        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                ' [' + self.kutype_name + '_kutype_cover_countdown] temp data: ' +\
                str(kutype_information_list) + '\n')

        """if there is no time buffer,  insert / update monitor mysql table"""
        if (int(self.kutype_coverd_buffer_s) != 0) and (countdown_minus_buffer_s <= 0):
            check_exists_ret = GeneralOperation.check_and_update_already_exists_kutype(\
                                                                kutype_information_list)
            if check_exists_ret == 255:
                GeneralOperation.insert_ygg_monitor_flow(kutype_information_list)
        else:
            """If returned to normal, update abnormal information"""
            kutype_information_list[8] = '1'
            GeneralOperation.check_and_update_already_exists_kutype(kutype_information_list)

        """0: means that there is no time limit to cover"""
        if int(self.kutype_coverd_time_s) == 0:
            return 0
        else:
            return countdown_time_h

    def analysis(self):
        """Start KutypeCoverCountDown analysis"""

        if int(self.kutype_coverd_time_s) == 0:
            return 0

        """single_job_info : save singel job information"""
        """job_name: save singel job name"""
        """prefix_job_name: save prefix job name"""
        """unixformat_time: temp use, save unix format time"""
        """download_job_dict: save all download job name - starttime"""
        single_job_info = list()
        job_name = ""
        prefix_job_name = ""
        unixformat_time = 0
        regex_download_name = re.compile(r'download')
        regex_kutype_name = re.compile('^' + self.kutype_name)
        download_job_dict = dict()

        """get all download job name and start time"""
        for single_job_info in self.metadata:
            job_name = single_job_info[0]
            prefix_job_name = re.split(r'-\d+', job_name)[0]

            """filter out with download field job"""
            if (regex_download_name.findall(job_name)):
                dateformat_time = single_job_info[7]
                unixformat_time = int(re.split(r'\.',\
                        str(time.mktime(dateformat_time.timetuple())))[0])

                """If there is no numeric suffix, the download job number is 1"""
                """If with a digital suffix, then take the earliest download job"""
                if (not download_job_dict.has_key(prefix_job_name)) or\
                        (unixformat_time < download_job_dict[prefix_job_name]):
                    download_job_dict[prefix_job_name] = unixformat_time

        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                ' [' + self.kutype_name + '_kutype_cover_countdown] temp data: ' +\
                str(download_job_dict) + '\n')

        """Get the latest download time as start time"""
        for find_kutype_download in download_job_dict.keys():
            """get the kutype downlaod start time"""
            """  1. Find the dwonload newest time with kutype job name"""
            """  2. initialized the bs newest time"""
            """  3. Find the dwonload newest time without kutype job name"""
            if (regex_kutype_name.findall(find_kutype_download)):
                self.bs_newest_page_unix_time = download_job_dict[find_kutype_download]
            elif (self.bs_newest_page_unix_time == 0):
                self.bs_newest_page_unix_time = download_job_dict[find_kutype_download]
            elif (self.bs_newest_page_unix_time != 0) and\
                        (download_job_dict[find_kutype_download] < self.bs_newest_page_unix_time):
                self.bs_newest_page_unix_time = download_job_dict[find_kutype_download]

        return self.calculate_cover_countdown()


class KutypeStartInterval(AnalysisBaseClass):
    """kutype start interval analysis method"""

    def __init__(self, monitor_iterm, metadata, global_conf):
        """Initialization data"""
        """Thinking: from the last bs cycle as a starting point"""
        """          calculate the time of the subsequent cycle"""
        super(KutypeStartInterval, self).__init__(monitor_iterm, metadata, global_conf)
        self.metadata = metadata
        self.monitor_iterm = monitor_iterm

        self.kutype_name = global_conf['ygg_ku_global_conf'][0][1]
        self.project_name = global_conf['ygg_ku_global_conf'][0][2]
        self.total_cycle_num = global_conf['ygg_ku_global_conf'][0][3]
        self.kutype_interval_time =  global_conf['ygg_ku_global_conf'][0][4]
        self.kutype_interval_time_s = modules.Util.time_formate_conversion_to_s(\
                                    self.kutype_interval_time)
        self.kutype_interval_buffer = global_conf['ygg_ku_global_conf'][0][5]
        self.kutype_interval_buffer_s = modules.Util.time_formate_conversion_to_s(\
                                    self.kutype_interval_buffer)
        self.compass_domain = global_conf['ygg_ku_global_conf'][0][10]

        """get current unix time"""
        self.current_unix_time = 0

    def get_all_start_record(self, iter_cycle_dict):
        """Difficulty: running time and start interval without any relationship"""
        """            The current run is not necessarily up to date"""
        """[ |--------|                                                       ]"""
        """[     |--------|                                                   ]"""
        """[                |--------|                                        ]"""
        """[                           |XXXXXXXX|                             ]"""
        """[                                      |--------|                  ]"""

        """Initialization record abnormal kutype information"""
        project_link = self.compass_domain + '/manager?project='+\
                                self.project_name + '&flow=end#executions'
        flow_link = self.compass_domain + '/executor?execid='

        """  [ iteration_cycle ] ---> [[iteration1, cycle1], [iteration2, cycle2], ...]"""
        """  iter_cycle_dict dict example: {'59_39': 1494860631, '59_38': 1494853426}"""
        """  dict_key_list dict example: """
        dict_key_list = [[] for i in range(len(iter_cycle_dict.keys()))]
        for count in range(0, len(iter_cycle_dict.keys())):
            dict_key_list[count].append(int\
                    (re.split(r'_', iter_cycle_dict.keys()[count])[0]))
            dict_key_list[count].append(int\
                    (re.split(r'_', iter_cycle_dict.keys()[count])[1]))

        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                ' [' + self.kutype_name + '_kutype_start_interval] temp data: ' +\
                str(iter_cycle_dict) + '\n')

        """ for sort by iteration then cycle"""
        dict_key_list.sort(key=itemgetter(0, 1))

        for iteration_cycle_cursor in dict_key_list:
            """get current iteration and cycle id"""
            iteration_cursor_current = int(iteration_cycle_cursor[0])
            cycle_cursor_current = int(iteration_cycle_cursor[1])

            """get next iteration and cycle id"""
            if cycle_cursor_current == (self.total_cycle_num - 1):
                iteration_cursor_next = iteration_cursor_current + 1
                cycle_cursor_current_next = 0
            else:
                iteration_cursor_next = iteration_cursor_current
                cycle_cursor_current_next = cycle_cursor_current + 1

            """combination next key"""
            dict_key = str(iteration_cursor_next) + '_' + str(cycle_cursor_current_next)

            """missing the next iteration-cycle cursor, means: end key, or missing a build process"""
            """print interval time"""
            if (not iter_cycle_dict.has_key(dict_key)):
                dict_key = str(iteration_cursor_current) + '_' + str(cycle_cursor_current)
                unixformat_time = iter_cycle_dict[dict_key]
                self.current_unix_time = int(re.split(r'\.', str(time.time()))[0])
                start_interval_countdown_s = self.kutype_interval_time_s + unixformat_time\
                                    + self.kutype_interval_buffer_s - self.current_unix_time
                start_interval_countdown_h = start_interval_countdown_s / 3600.0
                start_interval_countdown_h = ("%.2f" % start_interval_countdown_h)
                break

        """check and update/insert kutype information in the ygg monitor table """
        """kutype_information_list: project_name, intertion_id, cycle_id, exec_id, self.starttime"""
        """                         error_analysis, monitor_iterm, error_status, current_status, error_starttime"""
        """                         errpr_apppeartime, link1, link2"""
        iteration_cycle_cursor = [iteration_cursor_current, cycle_cursor_current]
        get_kutype_info_instance = GetFlowinfoByCursor(self.metadata,\
                            iteration_cycle_cursor, unixformat_time)
        kutype_information_list = get_kutype_info_instance.get_flow_key_information()
        exec_id = kutype_information_list[3]
        flow_link = flow_link + str(exec_id) + '#jobslist'

        kutype_information_list.append('kutype_monitor')
        kutype_information_list.append(self.monitor_iterm)
        kutype_information_list.append('kutype-start-interval=' +\
                                        str(start_interval_countdown_h) + 'h')
        kutype_information_list.append('2')
        kutype_information_list.append(str(datetime.datetime.now()))
        kutype_information_list.append(project_link)
        kutype_information_list.append(flow_link)

        if Config.load_agent_debug_level() >= 3:
            modules.Util.append_log_content_to_file(Config.debug_public_strategy_file,\
                ' [' + self.kutype_name + '_kutype_start_interval] temp data: ' +\
                str(kutype_information_list) + '\n')

        if int(start_interval_countdown_s) <= 0:
            kutype_information_list[1] = iteration_cursor_next
            kutype_information_list[2] = cycle_cursor_current_next
            kutype_information_list[3] = '0000'
            kutype_information_list[8] = '0'
            kutype_information_list[4] = '0000-00-00 00:00:00'
            check_exists_ret = GeneralOperation.check_and_update_already_exists_kutype(\
                                                                kutype_information_list)
            if check_exists_ret == 255:
                GeneralOperation.insert_ygg_monitor_flow(kutype_information_list)
        else:
            kutype_information_list[8] = '1'
            GeneralOperation.check_and_update_already_exists_kutype(kutype_information_list)
            
        return start_interval_countdown_h


    def analysis(self):
        """Start KutypeStartInterval analysis"""
        """single_job_info: save single job info"""
        """job_name: save single job name"""
        """unixformat_time: temp use, save unix format time stamp"""
        """download_start_time: save the key:iteration_cycle value:earliest_starttime"""
        single_job_info = list()
        job_name = ""
        unixformat_time = 0
        download_start_time_with_kuname = dict()
        download_start_time_without_kuname = dict()
        regex_start_job_flag = re.compile(r'download')
        regex_kutype_name = re.compile('^' + self.kutype_name)

        """get the newest bs cycle download start time"""
        for single_job_info in self.metadata:
            job_name = single_job_info[0]

            """get all build process downloa start time"""
            if regex_start_job_flag.findall(job_name):
                
                iteration_cursor = str(single_job_info[4]) 
                cycle_cursor = int(single_job_info[5]) 

                """download job name with kutype name"""
                if regex_kutype_name.findall(job_name):
                    """get current iteration-cycle download job earliest start time"""
                    if str(single_job_info[7]) == 'None':
                        continue
                    dateformat_time = single_job_info[7]
                    unixformat_time = int(re.split(r'\.',\
                            str(time.mktime(dateformat_time.timetuple())))[0])
                    """Compare the start time of two download tasks"""
                    dict_key = str(iteration_cursor) + '_' + str(cycle_cursor)
                    if (not download_start_time_with_kuname.has_key(dict_key)) or\
                        (unixformat_time < download_start_time_with_kuname[dict_key]):
                        download_start_time_with_kuname[dict_key] = unixformat_time

                else:
                    """download job name without kutype name"""
                    if str(single_job_info[7]) == 'None':
                        continue
                    dateformat_time = single_job_info[7]
                    unixformat_time = int(re.split(r'\.',\
                            str(time.mktime(dateformat_time.timetuple())))[0])
                    dict_key = str(iteration_cursor) + '_' + str(cycle_cursor)
                    if (not download_start_time_without_kuname.has_key(dict_key)) or\
                        (unixformat_time < download_start_time_without_kuname[dict_key]):
                        download_start_time_without_kuname[dict_key] = unixformat_time

        """check start time"""
        count = 0

        if download_start_time_with_kuname:
            iter_cycle_starttime_dict =  download_start_time_with_kuname.copy()
        else:
            iter_cycle_starttime_dict =  download_start_time_without_kuname.copy()

        return self.get_all_start_record(iter_cycle_starttime_dict)



class StartAnalysis(object):
    """kutype level analysis class"""

    def __init__(self, mon_iterm, metadata=None, kutype_global_conf=None):
        """init analysis argvs"""
        self.mon_iterm = mon_iterm
        """get analysis strategy, monitor iterms for analysis"""
        self.monitor_iterm_key = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[0]
        self.monitor_comparison_method = modules.Util.extract_by_regex(\
            '>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[0]
        self.monitor_iterm_value = re.split(r'>{1}(?!=)|<{1}(?!=)|==|!=|>=|<=', self.mon_iterm)[1]

        self.meta_data = metadata
        self.kutype_global_conf = kutype_global_conf

    def start(self):
        """start method"""

        '''
        print "Kutype - %s start analysis!!!" % self.strategy_name
        '''

        if self.monitor_iterm_key == 'kutype_running_flow_num':
            analysis_instance = KutypeRunningFlowNum(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        elif self.monitor_iterm_key == 'kutype_running_job_num':
            analysis_instance = KutypeRunningJobNum(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        elif self.monitor_iterm_key == 'kutype_failed_flow_num':
            analysis_instance = KutypeFailedFlowNum(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        elif self.monitor_iterm_key == 'kutype_failed_job_num':
            analysis_instance = KutypeFailedJobNum(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        elif self.monitor_iterm_key == 'kutype_cover_countdown':
            analysis_instance = KutypeCoverCountDown(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        elif self.monitor_iterm_key == 'kutype_start_interval':
            analysis_instance = KutypeStartInterval(\
                                self.mon_iterm, self.meta_data, self.kutype_global_conf)
        else:
            return 0
            
        return analysis_instance.analysis()


if __name__ == "__main__":
    if Config.load_agent_debug_level() >= 3:
        modules.Util.append_log_content_to_file(Config.debug_public_strategy_file, 'test')
