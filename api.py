from functools import wraps

import requests

import models


class HTTPAuthenticationError(requests.HTTPError):
    """Failed to login"""


def raise_authentication_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _response = func(*args, **kwargs)
        if 'code' in _response and _response['code'] == 401:
            raise HTTPAuthenticationError

        return _response

    return wrapper


def do_get_request(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        url = self.base_route + func(self, *args, **kwargs)
        _response = requests.get(url)
        _response.raise_for_status()

        return _response

    return wrapper


def apply_model(model, json_data):
    return model(**json_data)


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

        return _response.json()

    @raise_authentication_error
    def do_get_request(self, url, data=None):
        response = requests.get(self.base_route + url, data=data)
        response.raise_for_status()

        return response.json()

    def xqnetwork_pppoe_status(self) -> models.PPOEStatus:
        return apply_model(
            models.PPOEStatus,
            self.do_get_request("/xqnetwork/pppoe_status")
        )

    def xqnetwork_wifi_detail_all(self) -> models.WiFiDetails:
        return apply_model(
            models.WiFiDetails,
            self.do_get_request("/xqnetwork/wifi_detail_all")
        )

    def xqnetwork_get_miscan_switch(self):
        return self.do_get_request("/xqnetwork/get_miscan_switch")

    def xqnetwork_wan_info(self):
        return self.do_get_request("/xqnetwork/wan_info")

    def xqnetwork_wifi_macfilter_info(self):
        return self.do_get_request("/xqnetwork/wifi_macfilter_info")

    def xqnetwork_lan_dhcp(self):
        return self.do_get_request("/xqnetwork/lan_dhcp")

    def xqnetwork_lan_info(self):
        return self.do_get_request("/xqnetwork/lan_info")

    def xqnetwork_macbind_info(self):
        return self.do_get_request("/xqnetwork/macbind_info")

    def xqnetwork_dmz(self):
        return self.do_get_request("/xqnetwork/dmz")

    def xqnetwork_portforward(self):
        return self.do_get_request("/xqnetwork/portforward")

    def misystem_devicelist(self):
        return self.do_get_request("/misystem/devicelist")

    def misystem_newstatus(self):
        return self.do_get_request("/misystem/newstatus")

    def misystem_sys_time(self):
        return self.do_get_request("/misystem/sys_time")

    def misystem_qos_info(self):
        return self.do_get_request("/misystem/qos_info")

    def misystem_smartvpn_info(self):
        """
        :return: {
            "info": {
                "status": 0,
                "mode": 1,
                "ulist": [
                    "10.1.0.26",
                    "10.1.0.33",
                    "10.5.20.38",
                    "10.1.0.1",
                    "10.5.8.191",
                    "10.1.0.47"
                ],
                "switch": 1
            },
            "code": 0
        }
        """
        return self.do_get_request("/misystem/smartvpn_info")

    @raise_authentication_error
    def misystem_smartvpn_info(self, service_url, opt=0):
        """
        Add new entry to Traffic by service list
        :param service_url: web url/ip that you want to be access by vpn
        :param opt: 0 or 1, 0 to add and use 1 to delete
        :return: {"code":0}
        """
        url = self.base_route + "/misystem/smartvpn_url"
        response = requests.post(url, data={
            url: service_url,
            opt: opt
        })

        response.raise_for_status()

        return response

    def misystem_smartvpn_switch(self, mode):
        """
        Switch between "Traffic by service" (1) or "Traffic by device" (2)
        :param mode: 1 or 2
        :return:
        """
        return f"/misystem/smartvpn_switch?enable=1&mode={mode}"

    def misystem_mi_vpn_info(self):
        return self.do_get_request("/misystem/mi_vpn_info")

    def misystem_router_name(self):
        return self.do_get_request("/misystem/router_name")

    def misystem_topo_graph(self):
        return self.do_get_request("/misystem/topo_graph")

    def misystem_status(self):
        return self.do_get_request("/misystem/status")

    def misystem_active(self):
        return self.do_get_request("/misystem/active")

    def misystem_bandwidth_test(self):
        return self.do_get_request("/misystem/bandwidth_test?history=0")

    def misystem_set_band(self):
        return self.do_get_request("/misystem/set_band")

    def xqdatacenter_request(self):
        return self.do_get_request("/xqdatacenter/request")

    def xqsystem_reboot(self):
        return self.do_get_request("/xqsystem/reboot?client=web")

    def xqsystem_shutdown(self):
        return self.do_get_request("/xqsystem/shutdown")

    def xqsystem_country_code(self):
        return self.do_get_request("/xqsystem/country_code")

    def xqsystem_vpn(self):
        return self.do_get_request("/xqsystem/vpn")

    def xqsystem_get_location(self):
        return self.do_get_request("/xqsystem/get_location")

    def xqsystem_get_languages(self):
        return self.do_get_request("/xqsystem/get_languages")

    def xqsystem_vpn_status(self) -> models.VPNStatusResponse:
        """
        Returns VPN Connection status
        """
        return apply_model(
            models.VPNStatusResponse,
            self.do_get_request("/xqsystem/vpn_status")
        )

    def xqsystem_vpn_switch(self):
        return self.do_get_request("/xqsystem/vpn_switch?conn=0&id=37e62effeeba92ec6a34afcab2287196")

    def misns_wifi_share_info(self):
        return self.do_get_request("/misns/wifi_share_info")

    def xqnetdetect_netupspeed(self):
        return self.do_get_request("/xqnetdetect/netupspeed")
