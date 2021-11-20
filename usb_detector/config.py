
class CONFIG:
    USBDETECTORINTERVALTIME = 5 #in sec
    # -----------------------------------------
    ESHOST = '192.XX.XX.XX'
    ESPORT = 9200
    ESINDEX = 'security_agent_test'
    # -----------------------------------------
    SYSLOGHOST = '192.XXX.XX.XX'
    SYSLOGPORT = 12514
    # -----------------------------------------
    #  You can control report pipeline :
    #  For upload data via syslog ["syslog"]
    #  For upload data via elasticsearch and syslog ["elasticsearch","syslog"]
    REPORT_PIPELINE = ["elasticsearch"]
    # -----------------------------------------
    TIMEZONE = 'America/New_York'
    # ------------------------------------------
    OFFLINE_DATA_PATH = 'offline_data.pkl'



















