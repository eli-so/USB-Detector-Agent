import ctypes
import time
import logging
from config import CONFIG
from deepdiff import DeepDiff
from datahandler import datahandler
from query_handler import get_wmipnp_devices
from offlinedatahandler import offlinedatahandler


def usb_detector(offlinedatahandler):
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    usb_devices_pre_scan = {}
    usb_devices_post_scan = {}

    for device in get_wmipnp_devices():
        usb_devices_pre_scan.update({device.PNPDeviceID[1]: device})

    while True:
        print('Searcing for devices - Detecting Process...')
        time.sleep(CONFIG.USBDETECTORINTERVALTIME)
        for device in get_wmipnp_devices():
            usb_devices_post_scan.update({device.PNPDeviceID[1]: device})

        comparing_results = compare_wmipnp_devices_dict(usb_devices_pre_scan, usb_devices_post_scan)

        reporting_results(usb_devices_pre_scan, usb_devices_post_scan, comparing_results,
                          offlinedatahandler.get_offline_data_object())
        usb_devices_pre_scan = usb_devices_post_scan.copy()
        usb_devices_post_scan = {}
        if not offlinedatahandler.get_offline_data_object().is_queue_empty():
            dhandler = datahandler(offline_data=offlinedatahandler.get_offline_data_object())
            dhandler.report_to_elastic_search()
        offlinedatahandler.dump_pickle()


def reporting_results(devices_pre_scan, devices_post_scan, comparing_results, offline_data):
    """
    reporting data, which devices Connected
    and which one Disconnected
    Args:
        devices_pre_scan(list): list of WMIinternalPNPObjectProperties pre scan
        devices_post_scan(list): list of WMIinternalPNPObjectProperties post scan
    """
    logging.debug(comparing_results[0])
    if comparing_results[0]:
        for device_added in comparing_results[0]:
            report_data = datahandler(WMIinternalPNPObjectProperties=devices_post_scan[device_added],
                                      action="Device_Added",
                                      offline_data=offline_data)
            report_data.report_data()

    logging.debug(comparing_results[1])
    if comparing_results[1]:
        for device_removed in comparing_results[1]:
            report_data = datahandler(WMIinternalPNPObjectProperties=devices_pre_scan[device_removed],
                                      action="Device_Removed", offline_data=offline_data)
            report_data.report_data()


def compare_wmipnp_devices_dict(pre_scan_device, post_scan_device):
    """
    Comparing between 2 wmipnp devices lists , as results from that we can know which devices are connected to the
    machine and which one are Disconnected from the machine
    Args:
        pre_scan_device(dict): devices pre agent scanning
        post_scan_device(dict): devices post agent scanning

    Returns(list): list with 2 cells
        cell 0 contain all the devices that connected
        cell 1 contain all the devices that disconnected

    """
    wmipnp_device_removed = []
    wmipnp_device_added = []
    pre_scan_device_keys = list(pre_scan_device.keys())
    post_scan_device_keys = list(post_scan_device.keys())

    comapre_dict = DeepDiff(pre_scan_device_keys, post_scan_device_keys, ignore_order=True)
    comapre_dict_results = dict(comapre_dict)
    if 'iterable_item_removed' in comapre_dict_results:
        for wmipnp_removed_device in comapre_dict_results["iterable_item_removed"].items():
            wmipnp_device_removed.append(wmipnp_removed_device[1])

    if 'iterable_item_added' in comapre_dict_results:
        for wmipnp_added_device in comapre_dict_results["iterable_item_added"].items():
            wmipnp_device_added.append(wmipnp_added_device[1])

    return [wmipnp_device_added, wmipnp_device_removed]


if __name__ == '__main__':
    offline_data_handler = offlinedatahandler()
    usb_detector(offlinedatahandler=offline_data_handler)
