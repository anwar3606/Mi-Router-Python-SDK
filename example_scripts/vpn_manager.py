import os

from api import MiRouterAPI
from models import BasicStatus, SmartVPNServiceUpdateFlag, SmartVPNMode

api = MiRouterAPI(os.environ['mi_pass'])

# You can find this using option #3
VPN_ID = '37e62effeeba32ec6a94afcab2287196'


def connect_vpn():
    api.xqsystem_vpn_switch(VPN_ID, BasicStatus.ON)
    show_vpn_status()


def show_vpn_list():
    response = api.xqsystem_vpn()
    print('VPNs Found: ')
    for vpn in response.list:
        print('Name:', vpn.oname, 'ID:', vpn.id)


def show_vpn_status():
    response = api.xqsystem_vpn_status()
    print('VPN Status:', response.status.name)
    print('Up Time:', response.uptime)


def disconnect_vpn():
    api.xqsystem_vpn_switch(VPN_ID, BasicStatus.OFF)
    show_vpn_status()


def add_entry_to_service():
    entry = input('Enter Service IP/Domain: ')
    api.misystem_smartvpn_url(entry, SmartVPNServiceUpdateFlag.ADD)


def delete_entry_to_service():
    entry = input('Enter Service IP/Domain: ')
    api.misystem_smartvpn_url(entry, SmartVPNServiceUpdateFlag.DELETE)


def show_vpn_service_entries():
    response = api.misystem_smartvpn_info()

    print('Whitelist Services: ')
    for item in response.info.ulist:
        print(item)


def disable_auto_connect():
    api.xqsystem_set_vpnauto(BasicStatus.OFF)


def enable_auto_connect():
    api.xqsystem_set_vpnauto(BasicStatus.OFF)


def disable_smart_vpn():
    api.misystem_smartvpn_switch(BasicStatus.OFF, SmartVPNMode.TRAFFIC_BY_SEVICE)


def enable_smart_vpn():
    api.misystem_smartvpn_switch(BasicStatus.ON, SmartVPNMode.TRAFFIC_BY_SEVICE)


def switch_traffic_by_service():
    api.misystem_smartvpn_switch(BasicStatus.ON, SmartVPNMode.TRAFFIC_BY_SEVICE)


def switch_traffic_by_device():
    api.misystem_smartvpn_switch(BasicStatus.ON, SmartVPNMode.TRAFFIC_BY_DEVICE)


if __name__ == '__main__':
    actions = {
        '1': {"prompt": "Connect", "action": connect_vpn},
        '2': {"prompt": "Dis-Connect", "action": disconnect_vpn},

        '3': {"prompt": "Show Status", "action": show_vpn_status},
        '4': {"prompt": "List all vpns", "action": show_vpn_list},

        '5': {"prompt": "Show whitelist services", "action": show_vpn_service_entries},
        '6': {"prompt": "Add entry from whitelist service", "action": add_entry_to_service},
        '7': {"prompt": "Delete entry from whitelist service", "action": delete_entry_to_service},

        '8': {"prompt": "Enable Auto Connect to VPN", "action": enable_auto_connect},
        '9': {"prompt": "Disable Auto Connect to VPN", "action": disable_auto_connect},

        '10': {"prompt": "Enable Smart VPN", "action": enable_smart_vpn},
        '11': {"prompt": "Disable Smart VPN", "action": disable_smart_vpn},

        '12': {"prompt": "Switch Traffic by service", "action": switch_traffic_by_service},
        '13': {"prompt": "Switch Traffic by device", "action": switch_traffic_by_device},
    }
    while True:
        show_vpn_status()
        print()

        for key, value in actions.items():
            print(f"{key}: {value['prompt']}")

        action_selected = actions.get(input('Select Option: '))
        print()

        if not action_selected:
            print('Unknown option selected! Try again!')
        else:
            action_selected['action']()

        print()
