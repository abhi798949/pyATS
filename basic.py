from pyats.topology import loader

tb = loader.load('testbed.yaml')

device = tb.devices['R2']

device.connect()

# Issue 'show version' command and print the output
device.execute('show version')

config_command = [
               'interface GigabitEthernet0/0/0/2',
               'ipv4 address 192.168.1.7 255.255.255.0',
               'no shutdown',
               'exit',
               'commit',
               'control-plane',
               'management-plane',
               'inband interface all allow all',
               'exit',
               'exit',
               'commit',
               'router ospf 1',
               'router-id 1.1.1.1',
               'address-family ipv4 unicast',
               'area 0',
               'interface GigabitEthernet 0/0/0/2',
               'network point-to-point',
               'exit',
               'commit'
]
device.configure(config_command)

device.execute('show ip interface brief')
device.execute('show ospf database')
(device.disconnect())