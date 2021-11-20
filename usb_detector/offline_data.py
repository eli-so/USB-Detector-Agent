
class Offline_Data() :
    """
            Offline_Data Class
            in case of connectivity issue between agent to the server this class suppose to save the data offline
            until it will be pop out from the list
    """
    def __init__(self):

        self.offline_data = []

    def add_offline_data(self,data):
        """
        Add Data to the internal list
        Args:
            data(dict): Data dict
        """
        self.offline_data.append(data)

    def get_offline_data_poll(self):
        """
        Returns:
            self.offline_data(dict) : Data dict

        """
        return self.offline_data.pop()

    def get_offline_data_list(self):
        """
        Returns:


        """
        return self.offline_data

    def is_queue_empty(self):
        """
        Check if the list is empty
        Returns:
            Boolean : True If the list is Empty Else False
        """
        if self.offline_data:
            return False
        else:
            return True

    def queue_size(self):
        """
        check the list size
        Returns:
            list size(int)
        """
        return len(self.offline_data.qsize())


