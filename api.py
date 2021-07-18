from functools import wraps

import requests


class HTTPAuthenticationError(requests.HTTPError):
    """Failed to login"""


def raise_authentication_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _response = func(*args, **kwargs)
        if 'code' in _response.json() and _response.json()['code'] == 401:
            raise HTTPAuthenticationError
        else:
            return _response.json()

    return wrapper


def do_get_request(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        url = self.base_route + func(self, *args, **kwargs)
        _response = requests.get(url)
        _response.raise_for_status()

        return _response

    return wrapper


class MiRouterAPI:
    _token = None

    def __init__(self, password, host='http://192.168.31.1'):
        self.host = host
        self.password = password

    @property
    def base_route(self):
        return f"{self.host}/cgi-bin/luci/;stok={self.token}/api"

    @property
    def token(self):
        if not self._token:
            self._token = self._get_token()['token']

        return self._token

    @raise_authentication_error
    def _get_token(self):
        url = f"{self.host}/cgi-bin/luci/api/xqsystem/login"
        data = {
            'username': 'admin',
            'password': self.password
        }

        _response = requests.post(url, data=data)
        _response.raise_for_status()

        return _response

    @raise_authentication_error
    @do_get_request
    def xqnetwork_pppoe_status(self):
        return "/xqnetwork/pppoe_status"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_wifi_detail_all(self):
        return "/xqnetwork/wifi_detail_all"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_get_miscan_switch(self):
        return "/xqnetwork/get_miscan_switch"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_wan_info(self):
        return "/xqnetwork/wan_info"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_wifi_macfilter_info(self):
        return "/xqnetwork/wifi_macfilter_info"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_lan_dhcp(self):
        return "/xqnetwork/lan_dhcp"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_lan_info(self):
        return "/xqnetwork/lan_info"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_macbind_info(self):
        return "/xqnetwork/macbind_info"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_dmz(self):
        return "/xqnetwork/dmz"

    @raise_authentication_error
    @do_get_request
    def xqnetwork_portforward(self):
        return "/xqnetwork/portforward"

    @raise_authentication_error
    @do_get_request
    def misystem_devicelist(self):
        return "/misystem/devicelist"

    @raise_authentication_error
    @do_get_request
    def misystem_newstatus(self):
        return "/misystem/newstatus"

    @raise_authentication_error
    @do_get_request
    def misystem_sys_time(self):
        return "/misystem/sys_time"

    @raise_authentication_error
    @do_get_request
    def misystem_qos_info(self):
        return "/misystem/qos_info"

    @raise_authentication_error
    @do_get_request
    def misystem_smartvpn_info(self):
        return "/misystem/smartvpn_info"

    @raise_authentication_error
    @do_get_request
    def misystem_mi_vpn_info(self):
        return "/misystem/mi_vpn_info"

    @raise_authentication_error
    @do_get_request
    def misystem_router_name(self):
        return "/misystem/router_name"

    @raise_authentication_error
    @do_get_request
    def misystem_topo_graph(self):
        return "/misystem/topo_graph"

    @raise_authentication_error
    @do_get_request
    def misystem_status(self):
        return "/misystem/status"

    @raise_authentication_error
    @do_get_request
    def misystem_active(self):
        return "/misystem/active"

    @raise_authentication_error
    @do_get_request
    def misystem_bandwidth_test(self):
        return "/misystem/bandwidth_test?history=0"

    @raise_authentication_error
    @do_get_request
    def misystem_set_band(self):
        return "/misystem/set_band"

    @raise_authentication_error
    @do_get_request
    def xqdatacenter_request(self):
        return "/xqdatacenter/request"

    @raise_authentication_error
    @do_get_request
    def xqsystem_reboot(self):
        return "/xqsystem/reboot?client=web"

    @raise_authentication_error
    @do_get_request
    def xqsystem_shutdown(self):
        return "/xqsystem/shutdown"

    @raise_authentication_error
    @do_get_request
    def xqsystem_country_code(self):
        return "/xqsystem/country_code"

    @raise_authentication_error
    @do_get_request
    def xqsystem_vpn(self):
        return "/xqsystem/vpn"

    @raise_authentication_error
    @do_get_request
    def xqsystem_get_location(self):
        return "/xqsystem/get_location"

    @raise_authentication_error
    @do_get_request
    def xqsystem_get_languages(self):
        return "/xqsystem/get_languages"

    @raise_authentication_error
    @do_get_request
    def xqsystem_vpn_status(self):
        return "/xqsystem/vpn_status"

    @raise_authentication_error
    @do_get_request
    def xqsystem_vpn_switch(self):
        return "/xqsystem/vpn_switch?conn=0&id=37e62effeeba92ec6a34afcab2287196"

    @raise_authentication_error
    @do_get_request
    def misns_wifi_share_info(self):
        return "/misns/wifi_share_info"

    @raise_authentication_error
    @do_get_request
    def xqnetdetect_netupspeed(self):
        return "/xqnetdetect/netupspeed"

