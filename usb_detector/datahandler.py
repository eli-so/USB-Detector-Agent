import json
import logging.handlers
from datetime import datetime
import pytz
from config import CONFIG
from elasticsearch import Elasticsearch
from query_handler import get_disk_drive_name

class datahandler:
    """
    datahandler Class
    """
    def __init__(self, WMIinternalPNPObjectProperties=None, action=None, offline_data=None,
                 report_pipeline=["elasticsearch"]):
        """
        Create DataHandler object
        This Object supporting 2 push method
        1. push data to ELK via ElasticSearch package
        *  while using this method , all data saved first in offline_data object and send if the ELK host is reachable
        in case of connectivity issue , the data saved in offline_data object and will push once the Host will be
        reachable
        NOTE - For covering cases that data will be lost following connectivity issue & terminate application
        this code using "pickle" that save offline_data object in external file every few sec.

        2. push data via syslog

        Args:
            WMIinternalPNPObjectProperties(WMIinternalPNPObjectProperties):
            action(str): What action was taken ( device removed or added)
            offline_data(Offline_Data): Store all data offline before sending it to ELK
            report_pipeline(list): which push method to use
        """
        self.data = {}
        self.queue = []
        self.report_pipeline = report_pipeline
        self.action = action
        self.WMIinternalPNPObjectProperties = WMIinternalPNPObjectProperties
        self.offline_data = offline_data

    def report_data(self):
        """
        create data structure , pushing the data following the requested report_pipeline
        """
        friendlyname = "None"
        timezone = pytz.timezone(CONFIG.TIMEZONE)
        date_now = datetime.now(timezone)
        date_now.strftime('%Y-%m-%dT%H:%M:%S%z')
        if self.WMIinternalPNPObjectProperties.Service[1] == "USBSTOR" and self.action == "Device_Added":
            friendlyname = get_disk_drive_name(
                deviceid=self.WMIinternalPNPObjectProperties.PNPDeviceID[1].split("\\")[-1])
        self.data = {
            "@timestamp": date_now.strftime('%Y-%m-%dT%H:%M:%S%z'),
            "Action": self.action,
            "HostName": self.WMIinternalPNPObjectProperties.SystemName[1],
            "PNPDeviceID": self.WMIinternalPNPObjectProperties.PNPDeviceID[1],
            "Service": self.WMIinternalPNPObjectProperties.Service[1],
            "FriendlyName": friendlyname,
            "Agent": "usb_detector"
        }
        if "syslog" in self.report_pipeline:
            self.syslog_reporter()
        if "elasticsearch" in self.report_pipeline:
            self.report_to_elastic_search()

    def report_to_elastic_search(self):
        """
        push data to ELK host

        1. push data to ELK via Elasticsearch package *  while using this method , all data saved first in
        offline_data object and send if the ELK host is reachable in case of connectivity issue , the data saved in
        offline_data object and will push once the Host will be reachable NOTE - For covering cases that data will be
        lost following connectivity issue & terminate application this code using "pickle" that save offline_data
        object in external file every few sec.

        """

        self.offline_data.add_offline_data(json.dumps(self.data))
        self._report_to_elastic_search()

    def _report_to_elastic_search(self):
        try:
            elasticsearch = Elasticsearch([{'host': CONFIG.ESHOST, 'port': CONFIG.ESPORT}])
            if elasticsearch.ping():
                while not self.offline_data.is_queue_empty():
                    body = self.offline_data.get_offline_data_poll()
                    print(body)
                    print(
                        elasticsearch.index(index=CONFIG.ESINDEX, doc_type='_doc', body=json.dumps(json.loads(body))))
        except:
            raise Exception("ELK Host is not available")

    def syslog_reporter(self):
        """
        push data via syslog
        """
        print("".join(str(key) + "=" + str(value) + " " for key, value in self.data.items()))
        syslog_message = "".join(str(key) + "=" + str(value) + " " for key, value in self.data.items())
        syslog = logging.getLogger('MyLogger')
        syslog.setLevel(logging.INFO)
        handler = logging.handlers.SysLogHandler(address=(CONFIG.SYSLOGHOST, CONFIG.SYSLOGPORT))
        syslog.addHandler(handler)
        syslog.info(syslog_message)
