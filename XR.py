from pyats.topology import loader

# Load the testbed
tb = loader.load('testbed.yaml')
device = tb.devices['R2']

def configure_interface():
    """Configure the GigabitEthernet interface."""
    commands = [
        'interface GigabitEthernet0/0/0/2',
        'ipv4 address 192.168.1.7 255.255.255.0',
        'no shutdown',
        'exit',
        'commit'
    ]
    device.configure(commands)
    print("\n--- Interface Configuration Complete ---")

def configure_control_plane():
    """Configure control-plane and management-plane."""
    commands = [
        'control-plane',
        'management-plane',
        'inband interface all allow all',
        'exit',
        'exit',
        'commit'
    ]
    device.configure(commands)
    print("\n--- Control Plane Configuration Complete ---")

def configure_ospf():
    """Configure OSPF settings."""
    commands = [
        'router ospf 1',
        'router-id 1.1.1.1',
        'address-family ipv4 unicast',
        'area 0',
        'interface GigabitEthernet0/0/0/2',
        'network point-to-point',
        'exit',
        'segment-routing mpls',
        'area 0',
        'exit',
        'address-family ipv4 unicast',
        'area 0',
        'interface GigabitEthernet0/0/0/2',
        'exit',
        'router ospf 1',
        'address-family ipv4 unicast',
        'area 0',
        'interface loopback 0',
        'prefix-sid index 1',
        'commit'
    ]
    device.configure(commands)
    print("\n--- OSPF Configuration Complete ---")

def verify_configuration():
    """Verify the applied configurations."""
    print("\n--- Verifying Interface Configuration ---")
    print(device.execute('show ip interface brief'))

    print("\n--- Verifying OSPF Configuration ---")
    print(device.execute('show ospf database'))


# Main Execution
# Connect to the device
device.connect()

# Show version for validation
print("\n--- Device Information ---")
print(device.execute('show version'))

# Apply configurations
configure_interface()
configure_control_plane()
configure_ospf()

# Verify configurations
verify_configuration()

# Disconnect from the device
device.disconnect()
print("\n--- Disconnected from Device ---")
