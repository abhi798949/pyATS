from pyats.topology import loader

# Load the testbed
tb = loader.load('testbed.yaml')
device = tb.devices['R1']

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

def verify_configuration():
    """Verify the applied configurations."""
    print("\n--- Verifying Interface Configuration ---")
    print(device.execute('show ip interface brief'))


# Main Execution
# Connect to the device
device.connect()

# Show version for validation
print("\n--- Device Information ---")
print(device.execute('show version'))

# Apply configurations
configure_interface()


# Verify configurations
verify_configuration()

# Disconnect from the device
device.disconnect()
print("\n--- Disconnected from Device ---")
