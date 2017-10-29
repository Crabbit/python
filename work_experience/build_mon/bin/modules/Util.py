######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lvlu01(com@baidu.com)"
#__date__="2015-03-20 09:01"
#
#__author__="lili36(com@baidu.com)"
#__date__="2017-03-26 20:44"
#
######################################

"""
This module provide some common features
"""

import os
import urllib
import zipfile
import logging
import commands
import datetime
import subprocess
import time
import json
import re

log_file = re.split(r'/build_monitor/', os.path.dirname(os.path.split(\
            os.path.realpath(__file__))[0]))[0] + '/build_monitor/' + '/log/Util.log'
logging.basicConfig(filename=log_file,
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s : %(message)s '
    ' - %(filename)s: line %(lineno)d'
    , datefmt='[%d/%b/%Y %H:%M:%S]')

class Util(object):
    """some common function"""

    @staticmethod
    def unzip(src, dest):
        """unzip file"""
        z = zipfile.ZipFile(src)
        z.extractall(dest)

    @staticmethod
    def zip(zip_path, file_list, excluded_list=''):
        """zip file"""
        z = zipfile.ZipFile(zip_path, mode='w')
        for path, name in file_list.items():
            Util.write_zip_internal(z, path, name, excluded_list)
        z.close()

    @staticmethod
    def write_zip_internal(z, path, name, excluded_list):
        """write zip internal"""
        if os.path.isdir(path):
            for sub in os.listdir(path):
                if path + os.sep + sub not in excluded_list:
                    Util.write_zip_internal(z, path + os.sep + sub, name + os.sep + sub,\
                            excluded_list)
        else:
#            print path
            logging.debug('adding: %s', path)
            z.write(path, name)


    @staticmethod
    def curl(url, option):
        """URL

        Args:
            url: URL 
            option: 
        """
        curl_cmd = 'curl %s %s' % (option, url)
        sed_cmd = "sed -n '/^{/,/^}/p'"
        cmd = "%s | %s" % (curl_cmd, sed_cmd)
        logging.debug("run cmd: %s" % cmd)
        for i in range(3):
            p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = p.communicate()
            status = p.returncode
            logging.debug("get status output: %d : %s", status, output)
            if 0 == status and '' != output:
                return json.loads(output)
            else:
                continue
        return None

    @staticmethod
    def curl_cookie(url, option, Config):
        """curl cookie"""
        curl_cmd = 'curl -c %s/temp/cookie %s %s' % (Config.data_dir, option, url)
        logging.debug("run cmd: curl %s ", option)
        for i in range(3):
            status, output = commands.getstatusoutput('%s' % curl_cmd)
            output = Util.cat('%s/temp/cookie' % Config.data_dir)
            logging.debug("get status output: %d : %s", status, output)
            if 0 == status and '' != output:
                output = output.split('\t')
                return {output[-2]: output[-1]}
            else:
                continue
        return None

    @staticmethod
    def get_cur_dir():
        """get current directory"""
        return os.path.dirname(
                os.path.split(os.path.realpath(__file__))[0])

    @staticmethod
    def get_top_dir():
        """get top directory"""
        top_dir = re.split(r'/build_monitor/', Util.get_cur_dir())[0] + '/build_monitor/'
        return top_dir

    @staticmethod
    def cat(file, target=None, append=True):
        """cat file"""
        if target is None:
            if os.path.isfile(file):
                return subprocess.check_output('cat %s' % file, shell=True).strip()
            else:
                return None
        else:
            if append is True:
                return subprocess.Popen('cat %s >> %s' % (file, target), shell=True).wait() == 0
            else:
                return subprocess.Popen('cat %s > %s' % (file, target), shell=True).wait() == 0
            

    @staticmethod
    def echo(content, file):
        """echo"""
        return subprocess.Popen('echo \'%s\' > %s' % (content, file), shell=True).wait() == 0

    @staticmethod
    def rm(file):
        """remove file"""
        return subprocess.Popen('rm -rf %s' % file, shell=True).wait() == 0

    @staticmethod
    def touch(file):
        """touch file"""
        dir = os.path.dirname(file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        f = open(file, 'a') 
        f.close()
        return True

    @staticmethod
    def get_attempt_id(dir):
        """get job attempt id"""
        if os.path.isdir(dir):
            command = 'ls %s | grep -E "[0-9]+" | sort -n | tail -1' % dir
            attempt_id = subprocess.check_output(command, shell=True).strip()
            if attempt_id is None:
                return -1
            else:
                return int(attempt_id) % 10
        else:
            return -1

    @staticmethod
    def get_newest_value_by_key_file(keyfilepath, key):
        """get value by key and file"""
        if os.path.isfile(keyfilepath):
            command = 'cat ' + keyfilepath + ' | grep \'' + key + '\' | tail -1'
            return_content_fd = os.popen(command)
            return_content = return_content_fd.read()
            if not return_content:
                return 1
            regex_key = key + ':'

            regex_value = re.split(regex_key, return_content)[1]
            regex_value = re.split(r'\s*', regex_value)[0]
            return regex_value
        else:
            logging.info('%s file is note exist.' % keyfilepath)
        return 0

    @staticmethod
    def hadoop_dfs(action, hdfs_default=None, ugi=None):
        """hadoop dfs client"""
        hadoop_command = '${HADOOP_HOME}/bin/hadoop dfs '
        if hdfs_default is not None:
            hadoop_command += '-D fs.default.name=%s ' % hdfs_default
        if ugi is not None:
            hadoop_command += '-D hadoop.job.ugi=%s ' % ugi
        hadoop_command += '-'
        hadoop_command += action
        logging.debug(hadoop_command)
        for i in range(0, 3):
            p = subprocess.Popen(hadoop_command, shell=True, stdin=subprocess.PIPE, \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = p.communicate()
            status = p.returncode
            if 0 == status:
                logging.info('run command \'%s\' succeed.\n%s' % (hadoop_command, output))
                return True
            else:
                logging.error('run command \'%s\' failed.\n%s' % (hadoop_command, error))
                return False

    @staticmethod
    def extract_by_regex(regex_str, string):
        """extractr string by regex expression"""
        #regex_str = 'r' + '\'' + str(regex_str) + '\''
        regex_compile = re.compile(regex_str)
        return regex_compile.findall(string)
        

    @staticmethod
    def convert_compass_time(compass_time):
        """convert compass time"""
        if compass_time > 0:
            x = time.localtime(compass_time / 1000)            
            return time.strftime('%Y-%m-%d %H:%M:%S', x)

    @staticmethod
    def unixtime_to_datetime(unixtime_str):
        """unixtime -> datetime"""
        return datetime.datetime.fromtimestamp(unixtime_str)

    @staticmethod
    def datetime_to_unixtime(datetime_str):
        """datetime -> unixtime"""
        return time.mktime(datetime_str.timetuple())

    @staticmethod
    def timetuple_to_datetime(timetuple_str):
        """timetuple_str -> unixtime -> datetime"""
        unixtime = time.mktime(timetuple_str)
        return Util.unixtime_to_datetime(unixtime)

    @staticmethod
    def append_log_content_to_file(log_file=None, content=None):
        """append log content to the end of the file"""
        if log_file is None:
            logging.error('log file is emputy!')
            return 1
        if content is None:
            logging.error('content is emputy!')
            return 1

        Util.touch(log_file)
        log_file_fd = open(log_file, 'a')
        time_format = "%Y-%m-%d %H:%M:%S"
        time_stamp = time.strftime(time_format, time.localtime())
        log_file_fd.write(time_stamp + ' ' + content)
        log_file_fd.close()


    @staticmethod
    def time_formate_conversion_to_s(conf_time=None):
        """converts the time format to seconds"""
        if conf_time is None:
            logging.error('time_formate_conversion_to_s argv is emputy!')
            return 1

        if str(conf_time) == '0':
            return 0

        re_return = re.match(r'^([0-9]*)([sShHmM])$', conf_time)
        if re_return is None:
            logging.error(conf_time + ' regex time format error!')
            return 2

        time_value = int(re.sub(r'([sShHmM])$', "", conf_time))
        time_unit = re.sub(r'^([0-9]*)', "", conf_time)

        if (time_unit == 's') or (time_unit == 'S'):
            seconds = time_value
            return int(seconds)
        elif (time_unit == 'm') or (time_unit == 'M'):
            seconds = time_value * 60
            return int(seconds)
        elif (time_unit == 'h') or (time_unit == 'H'):
            seconds = time_value * 3600
            return int(seconds)

        

if __name__ == "__main__":
    #print Util.get_attempt_id('/tmp/aaa')
    #print Util.get_attempt_id('/tmp/bbb')
    print Util.get_top_dir()
    Util.time_formate_conversion_to_s('100m')
    filename = Util.get_top_dir() + 'status/vip/cycle.status'
    print Util.get_newest_value_by_key_file(filename, 'BS_NEWEST_CYCLE')
