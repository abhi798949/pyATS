from pyats.topology import loader

# Load the testbed
tb = loader.load('testbed.yaml')

# Define device-specific configurations
device_configs = {
    'R1': {
        'interface_ip': '192.168.1.1',
        'subnet_mask': '255.255.255.0',
        'ospf_id': '2.2.2.2',
        #'bgp router_id': '10.1.1.1',
    },
    'R2': {
        'interface_ip': '192.168.1.7',
        'subnet_mask': '255.255.255.0',
        'ospf_id': '1.1.1.1',
        #'bgp router_id': '10.1.1.2',
    },
}

def configure_interface(device, config):
    """Configure the GigabitEthernet interface."""
    commands = [
        f"interface GigabitEthernet0/0/0/0",
        f"ipv4 address {config['interface_ip']} {config['subnet_mask']}",
        "no shutdown",
        "exit",
        "commit",
    ]
    device.configure(commands)
    print(f"\n--- Interface Configuration Complete on {device.name} ---")

def configure_control_plane(device):
    """Configure control-plane and management-plane."""
    commands = [
        "control-plane",
        "management-plane",
        "inband interface all allow all",
        "exit",
        "exit",
        "commit",
    ]
    device.configure(commands)
    print(f"\n--- Control Plane Configuration Complete on {device.name} ---")

def configure_ospf(device, config):
    """Configure OSPF settings."""
    commands = [
        "router ospf 1",
        f"router-id {config['ospf_id']}",
        "address-family ipv4 unicast",
        "area 0",
        "interface GigabitEthernet0/0/0/0",
        "network point-to-point",
        "exit",
        "segment-routing mpls",
        "area 0",
        "exit",
        "address-family ipv4 unicast",
        "area 0",
        "interface GigabitEthernet0/0/0/0",
        "exit",
        "router ospf 1",
        "address-family ipv4 unicast",
        "area 0",
        "interface loopback 0",
        "prefix-sid index 1",
        "commit",
    ]
    device.configure(commands)
    print(f"\n--- OSPF Configuration Complete on {device.name} ---")

def configure_bgp(device, config):
    """Configure OSPF settings."""
    commands = [
        "router bgp 1",
        f"bgp router-id {config['ospf_id']}",
        "address-family ipv4 unicast",
        "exit",
        f"neighbor {config['interface_ip']}",
        "remote-as 1",
        "address-family ipv4 unicast",
        "commit",
    ]
    device.configure(commands)
    print(f"\n--- BGP Configuration Complete on {device.name} ---")

def verify_configuration(device):
    """Verify the applied configurations."""
    print(f"\n--- Verifying Interface Configuration on {device.name} ---")
    print(device.execute("show ip interface brief"))

    print(f"\n--- Verifying OSPF Configuration on {device.name} ---")
    print(device.execute("show run router bgp"))


# Main Execution
for device_name, config in device_configs.items():
    device = tb.devices[device_name]
    print(f"\n--- Connecting to {device_name} ---")
    device.connect()

    # Show version for validation
    print(f"\n--- Device Information for {device_name} ---")
    print(device.execute("show version"))

    # Apply configurations
    configure_interface(device, config)
    configure_control_plane(device)
    configure_ospf(device, config)
    configure_bgp(device, config)
    # Verify configurations
    verify_configuration(device)

    # Disconnect from the device
    device.disconnect()
    print(f"\n--- Disconnected from {device_name} ---")

print("\n--- Configuration and Verification Complete for All Devices ---")
