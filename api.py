import json
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

    @raise_authentication_error
    def do_post_request(self, url, data=None):
        response = requests.post(self.base_route + url, data=data)
        response.raise_for_status()

        try:
            return response.json()
        except json.JSONDecodeError:
            return response.text

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

    def xqnetwork_wan_info(self) -> models.WANDetails:
        return apply_model(
            models.WANDetails,
            self.do_get_request("/xqnetwork/wan_info")
        )

    def xqnetwork_wifi_macfilter_info(self) -> models.MacFilterInfo:
        return apply_model(
            models.MacFilterInfo,
            self.do_get_request("/xqnetwork/wifi_macfilter_info")
        )

    def xqnetwork_lan_dhcp(self) -> models.LanDHCPDetails:
        return apply_model(
            models.LanDHCPDetails,
            self.do_get_request("/xqnetwork/lan_dhcp")
        )

    def xqnetwork_lan_info(self) -> models.LanInfoDetails:
        return apply_model(
            models.LanInfoDetails,
            self.do_get_request("/xqnetwork/lan_info")
        )

    def xqnetwork_macbind_info(self) -> models.MACBindInfo:
        return apply_model(
            models.MACBindInfo,
            self.do_get_request("/xqnetwork/macbind_info")
        )

    def xqnetwork_dmz(self) -> models.DMZResponse:
        return apply_model(
            models.DMZResponse,
            self.do_get_request("/xqnetwork/dmz")
        )

    def xqnetwork_portforward(self) -> models.PortForwardList:
        return apply_model(
            models.PortForwardList,
            self.do_get_request("/xqnetwork/portforward")
        )

    def misystem_devicelist(self) -> models.DeviceListResponse:
        return apply_model(
            models.DeviceListResponse,
            self.do_get_request("/misystem/devicelist")
        )

    def misystem_newstatus(self) -> models.NewStatusResponse:
        return apply_model(
            models.NewStatusResponse,
            self.do_get_request("/misystem/newstatus")
        )

    def misystem_sys_time(self) -> models.TimeResponse:
        return apply_model(
            models.TimeResponse,
            self.do_get_request("/misystem/sys_time")
        )

    def misystem_qos_info(self) -> models.QoSInfo:
        return apply_model(
            models.QoSInfo,
            self.do_get_request("/misystem/qos_info")
        )

    def misystem_smartvpn_info(self) -> models.SmartVPNInfoResponse:
        return apply_model(
            models.SmartVPNInfoResponse,
            self.do_get_request("/misystem/smartvpn_info")
        )

    @raise_authentication_error
    def misystem_smartvpn_url(
            self,
            service_url: str,
            opt: models.SmartVPNServiceUpdateFlag = models.SmartVPNServiceUpdateFlag.ADD
    ) -> models.BasicCodeResponse:
        """
        Add new entry to Traffic by service list
        :param service_url: web url/ip that you want to be access by vpn
        :param opt: 0 or 1, 0 to add and use 1 to delete
        :return: {"code":0}
        """
        return apply_model(
            models.BasicCodeResponse,
            self.do_post_request("/misystem/smartvpn_url", data={
                "url": service_url,
                "opt": opt.value
            })
        )

    def misystem_smartvpn_switch(self, mode: models.SmartVPNMode) -> models.SmartVPNInfo:
        """
        Switch between "Traffic by service" (1) or "Traffic by device" (2)
        :param mode: 1 or 2
        :return:
        """
        return apply_model(
            models.SmartVPNInfo,
            self.do_get_request(f"/misystem/smartvpn_switch?enable=1&mode={mode}")
        )

    def misystem_mi_vpn_info(self) -> models.BasicStatusResponse:
        return apply_model(
            models.BasicStatusResponse,
            self.do_get_request("/misystem/mi_vpn_info")
        )

    def xqsystem_vpn(self) -> models.VPNResponse:
        return apply_model(
            models.VPNResponse,
            self.do_get_request("/xqsystem/vpn")
        )

    def xqsystem_vpn_status(self) -> models.VPNStatusResponse:
        """
        Returns VPN Connection status
        """
        return apply_model(
            models.VPNStatusResponse,
            self.do_get_request("/xqsystem/vpn_status")
        )

    def xqsystem_vpn_switch(self, id: str, connect: models.BasicStatus) -> models.BasicCodeResponse:
        """
        Connectes to a vpn profile with the id params
        :param id:
        :param connect:
        :return:
        """
        return apply_model(
            models.BasicCodeResponse,
            self.do_get_request(f"/xqsystem/vpn_switch?conn={connect.value}&id={id}")
        )

    def xqsystem_vpn_set_vpn(
            self,
            name: str,
            proto: models.VPNProto,
            server: str,
            username: str,
            password: str
    ) -> None:
        """
        Creates a new vpn profile/service
        :param name:
        :param proto:
        :param server:
        :param username:
        :param password:
        :return:
        """
        data = models.VPNItem(
            oname=name,
            proto=proto,
            server=server,
            username=username,
            password=password
        )
        return self.do_post_request("/misystem/smartvpn_url", data=data.dict())

    def misystem_router_name(self):
        return apply_model(
            models.RouterName,
            self.do_get_request("/misystem/router_name")
        )

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

    def xqsystem_get_location(self):
        return self.do_get_request("/xqsystem/get_location")

    def xqsystem_get_languages(self):
        return self.do_get_request("/xqsystem/get_languages")

    def misns_wifi_share_info(self):
        return self.do_get_request("/misns/wifi_share_info")

    def xqnetdetect_netupspeed(self):
        return self.do_get_request("/xqnetdetect/netupspeed")
