# Mi Router Python SDK

As Xiaomi doesn't have any official SDK of any sorts. This is a hacky solution to work with for now.

This does not include all api endpoint, Only added those apis that came infront of me.

## Usage:

```python
from api import MiRouterAPI

router_api = MiRouterAPI('your_pass')
data = router_api.misystem_status()
```

## List of endpoints used:

```
/misns/wifi_share_info
/misystem/active
/misystem/bandwidth_test?history=0
/misystem/devicelist
/misystem/mi_vpn_info
/misystem/newstatus
/misystem/qos_info
/misystem/router_name
/misystem/set_band
/misystem/smartvpn_info
/misystem/status
/misystem/sys_time
/misystem/topo_graph
/xqdatacenter/request
/xqnetdetect/netupspeed
/xqnetwork/dmz
/xqnetwork/get_miscan_switch
/xqnetwork/lan_dhcp
/xqnetwork/lan_info
/xqnetwork/macbind_info
/xqnetwork/portforward
/xqnetwork/pppoe_status
/xqnetwork/wan_info
/xqnetwork/wifi_detail_all
/xqnetwork/wifi_macfilter_info
/xqsystem/country_code
/xqsystem/get_languages
/xqsystem/get_location
/xqsystem/reboot?client=web
/xqsystem/shutdown
/xqsystem/vpn
/xqsystem/vpn_status
/xqsystem/vpn_switch
```