# USB-Detector-Agent
 
As most of you already know, connecting devices to computers using a USB port can lead to security breaches. You can block USB devices via third-party software or physical devices, but most of the time if you are leaving it unprotected, you don’t know which USB devices are connected to your laptop/computer.
For this reason, I developed the USB Detector Agent that detects and reports USB connections events. Adding or removing devices will report to the ELK and this agent can improve the monitoring of your USB devices.


•	A USB device monitoring and reporting service

•	Supports Windows environment (Support for Linux is currently in development)

•	Works in background (Running in silent mode by default)

•	Developed in Python.

•	Supports sending events directly to ELK & via Syslog.

•	Easy to use & configure.


#########################################################################################

# USB Detector Agent supporting in two reporting methods:

•	Uploading your events directly to ELK (Elasticsearch) via Elasticsearch Python package (https://pypi.org/project/elasticsearch/ )

•	Uploading your events via Syslog (if you are using Logstash, you can use “grok_pattern_example” for parsing)

