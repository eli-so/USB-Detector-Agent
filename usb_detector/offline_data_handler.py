import pickle
from os import path
from config import CONFIG
from offline_data import Offline_Data


class offline_data_handler():

    def __init__(self):
        self.offline_data_path = CONFIG.OFFLINE_DATA_PATH
        if not path.exists(CONFIG.OFFLINE_DATA_PATH):
            self.offline_data = Offline_Data()
            self.dump_pickle()
            self.load_pickle()
        else:
            self.load_pickle()

    def load_pickle(self):
        """
        load pickle file as offline_data variable
        """
        with open( self.offline_data_path, "rb") as pickle_read:
            self.offline_data = pickle.load(pickle_read)
            pickle_read.close()

    def dump_pickle(self):
        """
        dump ickle file as offline_data variable
        """
        with open(CONFIG.OFFLINE_DATA_PATH, "wb") as pickle_file:
            pickle.dump( self.offline_data, file=pickle_file)
            pickle_file.close()

    def get_offline_data_object(self):
        """
        return Offline_Data Object
        Returns:
                offline_data
        """
        return self.offline_data



