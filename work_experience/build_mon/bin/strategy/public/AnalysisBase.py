######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-04-25"
######################################

"""
analysis basic class
"""

import os
import sys
import logging
import json

"""
import modules
"""
sys.path.append("./../../")
import modules

class AnalysisBaseClass(object):
    """analysis base"""

    def __init__(self, monitor_iterm=None, metadata=None, global_conf=None):
        """Initialization data"""
        self.metadata = metadata
        self.global_conf = global_conf
        pass

    def analysis(self):
        """Start analysis"""
        pass


class GetFlowinfoByCursor(object):
    """get flow information from iteration and cycle"""

    def __init__(self, metadata, iteration_cycle_cursor, starttime=None):
        """Initialization the base information"""
        self.iteration_cursor_current = str(iteration_cycle_cursor[0])
        self.cycle_cursor_current = str(iteration_cycle_cursor[1])
        self.metadata = metadata
        if starttime is not None:
            self.starttime = str(modules.Util.unixtime_to_datetime(starttime))

        """return list"""
        self.return_list = list()

    def get_flow_key_information(self):
        """get flow key information by metadata & cursor"""
        for single_job_info in self.metadata:
            intertion_id = single_job_info[4]
            cycle_id = single_job_info[5]

            if (int(intertion_id) == int(self.iteration_cursor_current)) and\
                    (int(cycle_id) == int(self.cycle_cursor_current)):
                project_name = single_job_info[6]
                exec_id = single_job_info[9]

                self.return_list.append(project_name)
                self.return_list.append(intertion_id)
                self.return_list.append(cycle_id)
                self.return_list.append(exec_id)
                self.return_list.append(self.starttime)
                return self.return_list


if __name__ == "__main__":
    print 'ok'
