import ctypes
import  time
import logging
from config import CONFIG
from deepdiff import DeepDiff
from data_handler import data_handler
from query_handler import get_wmipnp_devices
from offline_data_handler import offline_data_handler


def usb_detector(offline_data_handler):
    """

    Args:
        offline_data_handler:

    Returns:

    """
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    usb_devices_before = {}
    usb_devices_after = {}

    for device in get_wmipnp_devices():
        usb_devices_before.update({device.PNPDeviceID[1]: device })

    while True:
        print('Searcing for devices - Detecting Process...')
        time.sleep(CONFIG.USBDETECTORINTERVALTIME)
        for device in get_wmipnp_devices():
            usb_devices_after.update({device.PNPDeviceID[1]: device })

        comparing_results = comapre_wmipnp_devices_dict(usb_devices_before, usb_devices_after)

        reporting_results(usb_devices_before, usb_devices_after, comparing_results ,offline_data_handler.get_offline_data_object() )
        usb_devices_before = usb_devices_after.copy()
        usb_devices_after = {}
        if not offline_data_handler.get_offline_data_object().is_queue_empty():
            dh = data_handler(offline_data=offline_data_handler.get_offline_data_object())
            dh._report_to_elastic_search()
        offline_data_handler.dump_pickle()

def reporting_results(devices_before,devices_after,comparing_results,offline_data):
    """
    reporting data , which devices are new (connected)
    and which one are Disconnected
    Args:
        devices_before(list): list of WMIinternalPNPObjectProperties before scan
        devices_after(list): list of WMIinternalPNPObjectProperties after scan
        comparing_results:
        offline_data(offline_data):
    """
    logging.debug(comparing_results[0])
    if comparing_results[0]:
        for device_added in comparing_results[0]:
            report_data=data_handler(WMIinternalPNPObjectProperties=devices_after[device_added], action="Device_Added",
                                     offline_data=offline_data)
            report_data.report_data()

    logging.debug(comparing_results[1])
    if comparing_results[1]:
        for device_removed in comparing_results[1]:
            report_data = data_handler(WMIinternalPNPObjectProperties=devices_before[device_removed],
                                        action="Device_Removed",offline_data=offline_data)
            report_data.report_data()


def comapre_wmipnp_devices_dict(pre_scan_device,post_scan_device):
    """
    compare between 2 wmipnp devices lists , as results from that we can know which devices are new (connected)
    and which one are Disconnected
    Args:
        pre_scan_device:
        post_scan_device:

    Returns(list): list with 2 cells
        cell 0 contain all the devices that connected
        cell 1 contain all the devices that disconnected

    """
    wmipnp_device_removed = []
    wmipnp_device_added= []
    pre_scan_device_keys = list(pre_scan_device.keys())
    post_scan_device_keys = list(post_scan_device.keys())

    comapre_dict = DeepDiff(pre_scan_device_keys, post_scan_device_keys,ignore_order=True )
    comapre_dict_results = dict(comapre_dict)
    if 'iterable_item_removed' in comapre_dict_results:
        for wmipnp_removed_device in comapre_dict_results["iterable_item_removed"].items():
            wmipnp_device_removed.append(wmipnp_removed_device[1])

    if 'iterable_item_added' in comapre_dict_results:
        for wmipnp_added_device in comapre_dict_results["iterable_item_added"].items():
            wmipnp_device_added.append(wmipnp_added_device[1])

    return [wmipnp_device_added,wmipnp_device_removed]


if __name__ == '__main__':
    offline_data_handler = offline_data_handler()
    usb_detector(offline_data_handler=offline_data_handler)





