'''
This is basically a 1 to 1 port of laptop-detect with one exception: the order
of the checks has been altered so that the checks that are most likely to
succeed come first (on linux that is, sorry not sorry mac users).
'''

import os
from shutil import which

# So user can loop up why we are believed to be a laptop.
reason = [
    "We're not on a laptop (no relevant hint found)",
    "We're a portable (dmi)",
    "We're a laptop (dmi)",
    "We're a notebook (dmi)",
    "We're a hand held (dmi)",
    "We're a laptop (non device ACPI batteries found)",
    "We're a laptop (ACPI batteries found)",
    "We're a laptop (APM batteries found)",
    "We're a laptop (Mac batteries found)",
]


def laptop_detect():
    '''Check if device is a laptop.'''
    # Check sysfs for the chassis type.
    if os.path.isfile('/sys/devices/virtual/dmi/id/chassis_type'):
        with open('/sys/devices/virtual/dmi/id/chassis_type', 'r') as ct:
            chassis_type = int(ct.read().strip())
        if chassis_type == 8:
            return 1  # We're a portable
        if chassis_type == 9:
            return 2  # We're a laptop
        if chassis_type == 10:
            return 3  # We're a notebook
        if chassis_type == 11:
            return 4  # We're a hand held

    # Use dmidecode to grab the Chassis type.
    if all((os.access('/dev/mem', os.R_OK),
            (dmidecode := which('dmidecode')),
            os.access(dmidecode, os.X_OK))):
        dmitype = os.popen(f'{dmidecode} --string chassis-type').read().strip()
        if dmitype == 'Portable':
            return 1
        if dmitype == 'Laptop':
            return 2
        if dmitype == 'Notebook':
            return 3
        if dmitype == 'Hand Held':
            return 4

    # Check sysfs for non device ACPI batteries.
    sysfs_power_supply = '/sys/class/power_supply'
    if os.path.isdir(sysfs_power_supply):
        for power_supply in os.listdir(sysfs_power_supply):
            with open(os.path.join(sysfs_power_supply, power_supply, 'type'), 'r') as t:
                if 'Battery' in t.read():
                    if not os.path.exists((scope := os.path.join(sysfs_power_supply, power_supply, 'scope'))):
                        return 5  # We're a laptop (non device ACPI batteries found)
                    with open(scope, 'r') as s:
                        if 'Device' not in s.read():
                            return 5  # We're a laptop (non device ACPI batteries found)

    # Check procfs for ACPI batteries:
    pab = '/proc/acpi/battery'
    if os.path.isdir(pab):
        for d in (os.path.join(pab, d) for d in os.listdir(pab)):
            for b in (os.path.join(d, b) for b in os.listdir(d)):
                if os.path.isdir(b):
                    return 6  # We're a laptop (ACPI batteries found)

    # Check for APM batteries. This sucks because we'll only get a valid
    # response if the laptop has a battery fitted at the time.
    if os.path.isfile('/proc/apm'):
        with open('/proc/apm', 'r') as apm:
            battery = apm.read().split()[5]
        if battery != '0xff' and battery != '0x80':
            return 7  # We're a laptop (APM batteries found)

    # Are we a mac?
    if os.path.isdir('/proc/pmu'):
        with open('/proc/pmu/info', 'r') as i:
            batteries = [line.partition(':')[2] for line in i.readlines() if 'Battery' in line]
        if len(batteries) != 0:
            return 8  # We're a laptop (Mac batteries found)
        return 0

    return 0  # We're not on a laptop (no relevant hint found)
