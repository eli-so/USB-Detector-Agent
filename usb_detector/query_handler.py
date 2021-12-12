import json
import subprocess
import logging
from pypnpobjects import WMIStorePNPObjects

def get_wmipnp_devices():
    """
    Get wmipnp_devices , scan over connected devices
    Returns:
            pnpdevices(list) : list of pnpdevices
    """
    with WMIStorePNPObjects() as wmipnp_devices:
        proc_res = wmipnp_devices.load()
        if proc_res[0] == 0:
            pnpdevices = list(wmipnp_devices.query('*', pnpclass='USB', case_sensitive_comparision=False,
                                                   comparision_operator='like'))
            for dev in pnpdevices:
                logging.debug('Device %s is %s' % (dev.Name))
            logging.debug(len(pnpdevices))
        else:
            logging.info('Error with code %d : %s' % (proc_res))
    return pnpdevices


def send_powershell_query(command):
    """`
     wrapper for powershell queries
    Args:
        command(str): command for send
    Returns:
          results(json): command results
    `"""
    proc = subprocess.run(
        args=[
            'powershell',
            '-noprofile',
            '-command',
            f'{command} | ConvertTo-Json'
        ],
        text=True,
        stdout=subprocess.PIPE
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        print('Failed to enumerate drives')
        return []
    results = json.loads(proc.stdout)
    return results


def get_disk_drive_name(deviceid=""):
    try:
        result = send_powershell_query(
            command="Get-PnpDevice -Class DiskDrive -PresentOnly  | Where { $_.InstanceId.contains(" + f"'{deviceid}'" + ") }")
        return result["FriendlyName"]
    except Exception as exception:
        return f"Can't locate FriendlyName, Exception {exception} "
