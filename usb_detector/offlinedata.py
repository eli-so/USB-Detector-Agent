class offlinedata:
    """
            Offline_Data Class
            In case of connectivity issue between USB Detector agent to ELK server,
            This class will save the data 'offline' in queue.
    """
    def __init__(self):
        self.offline_data = []

    def add_offline_data(self, data):
        """
        Adding new data to offline_data list
        Args:
            Dict : Data dict
        """
        self.offline_data.append(data)

    def get_offline_data_poll(self):
        """
        Pop data from offline_data polling list
        """
        return self.offline_data.pop()

    def get_offline_data_list(self):
        """
        Get offline_data list
        Returns:
             List : offline_data
        """
        return self.offline_data

    def is_queue_empty(self):
        """
        Check if the list is empty
        Returns:
            Bool : True If the list is Empty Else False
        """
        if self.offline_data:
            return False
        else:
            return True

    def queue_size(self):
        """
        checking list size
        Returns:
                Int : list size
        """
        return len(self.offline_data.qsize())
