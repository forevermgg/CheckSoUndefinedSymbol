# !/usr/bin/env python coding:utf-8
# This script is aimed to grep logs by application(User should input a packageName
# And then we look up for the process ids then separate logs by process ids).

import os
import sys

from past.builtins import xrange, raw_input

packageName = str(sys.argv[1])


def getDeviceId():
    devices = []
    command = "adb devices -l | sed '1d'| awk '{print $1}'"
    result = os.popen(command)
    device_id = result.readline().strip()
    if device_id != "":
        devices.append(device_id)

    while device_id != "":
        device_id = result.readline().strip()
        if device_id != "":
            devices.append(device_id)
    return devices


def printPackageLog(device, package_name):
    # print device, packageName
    print("Got device: " + device)
    command = "adb -s %s shell ps | grep %s | awk '{print $2}'" % (device, package_name)
    # print command
    p = os.popen(command)
    # for some applications,there are multiple processes,so we should get all the process id
    pid = p.readline().strip()
    filters = pid
    while pid != "":
        pid = p.readline().strip()
        if pid != '':
            filters = filters + "|" + pid
            # print 'command = %s;filters=%s'%(command, filters)
    if filters != '':
        cmd = 'adb -s %s logcat -v time | grep --color=always -E "%s" ' % (device, filters)
        os.system(cmd)


devices = getDeviceId()
devicesNum = len(devices)

if devicesNum < 1:
    print("Device not found.")
elif devicesNum == 1:
    device = devices[0]
    printPackageLog(device, packageName)
else:
    print("Please chose a Device, input the index of the device:")
    for i in xrange(0, devicesNum):
        print(str(i) + "\t" + devices[i])
    index = raw_input("")
    printPackageLog(devices[int(index)], packageName)

# python3 logcatPkg.py com.mx.browser
