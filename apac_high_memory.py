#!usr/bin/python3

# This script is to check the memory of Cisco switches, to make sure it is less than 80%
# The output should be a table of switch name, memory percentage for each switch unit
# Usage: python3 apac_high_memory.py --testbed apac_tb.yaml

import logging
import jinja2
import json
from pyats import aetest
from genie.testbed import load

#TODO: Get the logger for script
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

#TODO: Connect to device
class Common_setup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_device(self, testbed):
        for device_name, device in testbed.devices.items():
            log.info(f"Connecting to {device_name}")
            device.connect()
            # Store device_name as variable "device_name", to use in other test cases
            self.parent.parameters['device_name'] = device_name

#TODO: Parse the cli "show platform software status control-processor brief", and write output to a text file to double-check
class Check_memory(aetest.Testcase):
    @aetest.test
    def show_platform_memory(self, testbed):
        self.platform_memory = {}
        for device_name, device in testbed.devices.items():
            log.info(f"{device_name} connected status: {device.connected}")
            log.info(f"Running commnd 'show platform software status control-processor brief' on {device_name}")
            # Add the parse result as the value of key "device_name"
            self.platform_memory[device_name] = device.parse("show platform software status control-processor brief")
        # Display result to console
        log.info(self.platform_memory)
        # Store the platform_memory as variable "platform_memory", to use in other test cases
        self.parent.parameters['platform_memory'] = self.platform_memory
        # Output the result of command to a text file
#        with open("show platform memory.txt", "w") as f:
#            json_data = json.dumps(self.platform_memory, indent=4)
#            f.write(json_data)

#TODO: Confirm the memory is less than 80%, and display the memory as a table of switch name, switch unit, memory percentage
class Memory_less_than_80(aetest.Testcase):
    @aetest.test
    def memory_check(self):
        platform_memory = self.parent.parameters.get('platform_memory', {})

        with open("apac_switch_memory.txt", "w") as fh:
            for device, info in platform_memory.items():
                fh.write(f"******** Memory status of {device} ********\n")
                fh.write("Switch number         Used memory (%)\n")
                fh.write("-------------------------------------\n")
                memory_status = [] 
                for switch_unit, unit_info in info['slot'].items():
                    log.info(f"Found switch: {switch_unit}")
                    used_memory = unit_info['memory']['used_percentage']
                    memory_status.append(f"{switch_unit}\t{used_memory}")
        
            # Output used memory for each switch unit
                for line in memory_status:
                    switch_unit, used_memory = line.split('\t')
                    if int(used_memory) > 50:
                        fh.write(f"{switch_unit.ljust(20)}{used_memory.rjust(8)} <==== Need to check\n")
                        log.info(f"Memory test of {device} is FAILED ***")
                    else:
                        fh.write(f"{switch_unit.ljust(20)}{used_memory.rjust(8)}\n")
                        log.info(f"Memory test of {device} is PASSED")
                fh.write("=======================================")
                fh.write(2*"\n")                
                      
#TODO: Disconnect from device
class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_device(self, testbed):
        for device_name, device in testbed.devices.items():
            log.info(f"Disconnecting from {device_name}")
            device.disconnect()

if __name__ == ("__main__"):
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed', type=loader.load)
    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
