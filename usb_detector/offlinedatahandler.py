import pickle
from os import path
from config import CONFIG
from offlinedata import offlinedata

class offlinedatahandler:
    def __init__(self):
        """
        Store offlinedata Object to external file using by Pickle,
        more information about pickle you can find at: https://docs.python.org/3/library/pickle.html
        """
        self.offline_data_path = CONFIG.OFFLINE_DATA_PATH
        if not path.exists(CONFIG.OFFLINE_DATA_PATH):
            self.offline_data = offlinedata()
            self.dump_pickle()
            self.load_pickle()
        else:
            self.load_pickle()

    def load_pickle(self):
        """
        load offline_data Object from pickle file
        """
        with open(self.offline_data_path, "rb") as pickle_read:
            self.offline_data = pickle.load(pickle_read)
            pickle_read.close()

    def dump_pickle(self):
        """
        Dump offline_data Object to pickle file
        """
        with open(CONFIG.OFFLINE_DATA_PATH, "wb") as pickle_file:
            pickle.dump(self.offline_data, file=pickle_file)
            pickle_file.close()

    def get_offline_data_object(self):
        """
        Get Offline_Data Object
        Returns:
               offlinedata :  offline_data
        """
        return self.offline_data
