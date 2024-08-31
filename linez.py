#!/usr/bin/env python3
import udi_interface
import sys
import time
import requests

LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom
polyglot = None
Parameters = None
n_queue = []

class LinezNode(udi_interface.Node):
    id = 'linez'
    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},   # NodeServer Connected
        {'driver': 'GV0', 'value': 1, 'uom': 25}, # HeartBeat (1/-1)
        {'driver': 'GV1', 'value': 0, 'uom': 56}, # Linez Serial Number
        {'driver': 'GV2', 'value': 0, 'uom': 73}, # Grid Power
        {'driver': 'GV3', 'value': 0, 'uom': 73}, # Solar Power
        {'driver': 'GV4', 'value': 0, 'uom': 73}, # Building Power
        {'driver': 'GV5', 'value': 0, 'uom': 73}, # Power A
        {'driver': 'GV6', 'value': 0, 'uom': 73}, # Power B
        {'driver': 'GV7', 'value': 0, 'uom': 73}, # Power AB
        {'driver': 'GV8', 'value': 0, 'uom': 73}, # Power C
        {'driver': 'GV9', 'value': 0, 'uom': 73}, # Power D
        {'driver': 'GV10', 'value': 0, 'uom': 73}, # Power CD
        {'driver': 'GV11', 'value': 0, 'uom': 72}, # Voltage A
        {'driver': 'GV12', 'value': 0, 'uom': 72}, # Voltage B
        {'driver': 'GV13', 'value': 0, 'uom': 72}, # Voltage AB
        {'driver': 'GV14', 'value': 0, 'uom': 1},  # Current A
        {'driver': 'GV15', 'value': 0, 'uom': 1},  # Current B
        {'driver': 'GV16', 'value': 0, 'uom': 1},  # Current C
        {'driver': 'GV17', 'value': 0, 'uom': 1},  # Current D
        {'driver': 'GV18', 'value': 0, 'uom': 53}, # Power Factor
        {'driver': 'GV19', 'value': 0, 'uom': 90}, # Frequency
    ]

    def __init__(self, polyglot, primary, address, name):
        super(LinezNode, self).__init__(polyglot, primary, address, name)
        self.ip_address = None  # Initialize to None

    def start(self):
        # Load IP address from Parameters
        self.load_ip_address()

    def load_ip_address(self):
        self.ip_address = Parameters.get('ip_address')
        if not self.ip_address:
            LOGGER.error("No IP address specified in the configuration. Please set it in PG3.")
        else:
            self.ip_address = f"http://{self.ip_address}/sensors"
            LOGGER.info(f"Using server IP: {self.ip_address}")

    def query(self, command=None):
        LOGGER.info('Query command received. Resetting values and re-polling...')
        self.setDriver('GV0', 0, True, True)  # Reset HeartBeat
        self.setDriver('GV2', 0, True, True)  # Reset Grid Power
        self.setDriver('GV3', 0, True, True)  # Reset Solar Power
        self.setDriver('GV4', 0, True, True)  # Reset Building Power
        self.setDriver('GV5', 0, True, True)  # Reset Power A
        self.setDriver('GV6', 0, True, True)  # Reset Power B
        self.setDriver('GV7', 0, True, True)  # Reset Power AB
        self.setDriver('GV8', 0, True, True)  # Reset Power C
        self.setDriver('GV9', 0, True, True)  # Reset Power D
        self.setDriver('GV10', 0, True, True)  # Reset Power CD
        self.setDriver('GV11', 0, True, True)  # Reset Voltage A
        self.setDriver('GV12', 0, True, True)  # Reset Voltage B
        self.setDriver('GV13', 0, True, True)  # Reset Voltage AB
        self.setDriver('GV14', 0, True, True)  # Reset Current A
        self.setDriver('GV15', 0, True, True)  # Reset Current B
        self.setDriver('GV16', 0, True, True)  # Reset Current C
        self.setDriver('GV17', 0, True, True)  # Reset Current D
        self.setDriver('GV18', 0, True, True)  # Reset Power Factor
        self.setDriver('GV19', 0, True, True)  # Reset Frequency
        time.sleep(5)
        self.poll('shortPoll')

    def poll(self, polltype):
        if 'shortPoll' in polltype:
            if not self.ip_address:
                LOGGER.error("No IP address specified. Cannot perform polling.")
                return
            
            try:
                updates = {}
                current_heartbeat = self.getDriver('GV0')
                new_heartbeat = -1 if current_heartbeat == 1 else 1
                updates['GV0'] = new_heartbeat

                response = requests.get(self.ip_address)
                data = response.json()

                node_id = list(data.keys())[0]
                serial_number = ''.join(filter(str.isdigit, node_id))
                if int(serial_number) != self.getDriver('GV1'):
                    updates['GV1'] = int(serial_number)

                meter_data = data.get(node_id, {}).get('meter', [{}])[0].get('measure', {})
                power_total = meter_data.get('bldg_power')
                solar_power = meter_data.get('solar_power')
                bldg_power = meter_data.get('power_total')
                power_a = meter_data.get('power_a')
                power_b = meter_data.get('power_b')
                power_ab = meter_data.get('power_ab')
                power_c = meter_data.get('power_c')
                power_d = meter_data.get('power_d')
                power_cd = meter_data.get('power_cd')
                voltage_an = meter_data.get('voltage_an')
                voltage_bn = meter_data.get('voltage_bn')
                voltage_ab = meter_data.get('voltage_ab')
                current_a = meter_data.get('current_a')
                current_b = meter_data.get('current_b')
                current_c = meter_data.get('current_c')
                current_d = meter_data.get('current_d')
                power_factor = meter_data.get('power_factor_total')
                frequency = meter_data.get('frequency')

                if power_total is not None and power_total != self.getDriver('GV2'):
                    updates['GV2'] = power_total
                if solar_power is not None and solar_power != self.getDriver('GV3'):
                    updates['GV3'] = solar_power
                if bldg_power is not None and bldg_power != self.getDriver('GV4'):
                    updates['GV4'] = bldg_power
                if power_a is not None and power_a != self.getDriver('GV5'):
                    updates['GV5'] = power_a
                if power_b is not None and power_b != self.getDriver('GV6'):
                    updates['GV6'] = power_b
                if power_ab is not None and power_ab != self.getDriver('GV7'):
                    updates['GV7'] = power_ab
                if power_c is not None and power_c != self.getDriver('GV8'):
                    updates['GV8'] = power_c
                if power_d is not None and power_d != self.getDriver('GV9'):
                    updates['GV9'] = power_d
                if power_cd is not None and power_cd != self.getDriver('GV10'):
                    updates['GV10'] = power_cd
                if voltage_an is not None and voltage_an != self.getDriver('GV11'):
                    updates['GV11'] = voltage_an
                if voltage_bn is not None and voltage_bn != self.getDriver('GV12'):
                    updates['GV12'] = voltage_bn
                if voltage_ab is not None and voltage_ab != self.getDriver('GV13'):
                    updates['GV13'] = voltage_ab
                if current_a is not None and current_a != self.getDriver('GV14'):
                    updates['GV14'] = current_a
                if current_b is not None and current_b != self.getDriver('GV15'):
                    updates['GV15'] = current_b
                if current_c is not None and current_c != self.getDriver('GV16'):
                    updates['GV16'] = current_c
                if current_d is not None and current_d != self.getDriver('GV17'):
                    updates['GV17'] = current_d
                if power_factor is not None and power_factor != self.getDriver('GV18'):
                    updates['GV18'] = power_factor
                if frequency is not None and frequency != self.getDriver('GV19'):
                    updates['GV19'] = frequency

                self.batch_update_drivers(updates)

            except Exception as e:
                LOGGER.error(f"Failed to poll data: {e}")

    def batch_update_drivers(self, updates):
        for driver, value in updates.items():
            self.setDriver(driver, value, report=True, force=True)

    commands = {'QUERY': query}

if __name__ == "__main__":
    try:
        polyglot = udi_interface.Interface([])
        polyglot.start('1.0.1')

        Parameters = Custom(polyglot, 'customparams')

        # Initialize custom parameters with default key
        def init_custom_params():
            if 'ip_address' not in Parameters:
                Parameters['ip_address'] = ''
                LOGGER.info('Initialized ip_address key in custom parameters.')

        def on_custom_params(params):
            Parameters.load(params)
            node.load_ip_address()  # Reload IP address when parameters change

        polyglot.subscribe(polyglot.CUSTOMPARAMS, on_custom_params)
        polyglot.subscribe(polyglot.ADDNODEDONE, lambda data: n_queue.append(data['address']))
        polyglot.subscribe(polyglot.STOP, lambda: polyglot.stop())
        polyglot.subscribe(polyglot.POLL, lambda polltype: polyglot.getNodes()['my_address'].poll(polltype))

        polyglot.ready()
        polyglot.setCustomParamsDoc()
        polyglot.updateProfile()

        node = LinezNode(polyglot, 'my_address', 'my_address', 'Linez')
        polyglot.addNode(node)
        while len(n_queue) == 0:
            time.sleep(0.1)
        n_queue.pop()

        init_custom_params()  # Initialize custom parameters
        node.start()  # Call the start method to read the IP address

        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)

