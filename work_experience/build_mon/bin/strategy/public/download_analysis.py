######################################
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#__author__="lili36"
#__date__="2017-04-25"
######################################

"""
download info analysis module
"""

import os
import sys
import logging
import json

"""
import basic class
"""
from AnalysisBase import AnalysisBaseClass

class DownloadUsedTime(AnalysisBaseClass):
    """analysis base"""

    def __init__(self, monitor_iterms, metadata, global_conf):
        """Initialization data"""
        super(DownloadUsedTime, self).__init__(monitor_iterms, metadata, global_conf)

    def analysis(self):
        """Start analysis"""
        pass


class DownloadUrlNum(AnalysisBaseClass):
    """analysis base"""

    def __init__(self, monitor_iterms, metadata, global_conf):
        """Initialization data"""
        super(DownloadUrlNum, self).__init__(monitor_iterms, metadata, global_conf)

    def analysis(self):
        """Start analysis"""
        pass


class StartAnalysis(object):
    """download info analysis class"""

    def __init__(self, strategy_name, mon_iterm, metadata=None, kutype_global_conf=None):
        """init """

        self.strategy_name = strategy_name
        self.mon_iterm = mon_iterm
        self.meta_data = metadata
        self.kutype_global_conf = kutype_global_conf
        pass

    def start(self):
        """start method"""
        print "download - %s - start analysis!!!" % self.strategy_name
        pass


if __name__ == "__main__":
    debug_instance = StartAnalysis(strategy_name='download_analysis',\
                    mon_iterm='download_used_time', metadata='test')
    debug_instance.start()
