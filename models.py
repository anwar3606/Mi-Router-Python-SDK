from enum import Enum
from ipaddress import IPv4Address
from typing import List, Optional

from pydantic import BaseModel, validator, root_validator, Field


# noinspection PyRedeclaration
class BaseModel(BaseModel):

    @root_validator(pre=True)
    def check_card_number_omitted(cls, values):
        for key in list(values.keys()):
            if values[key] == 'nil':
                values[key] = None

        return values


class ConnectionStatus(Enum):
    Connected = 0
    Dialing = 1
    Couldnt_Connect = 2
    Disconnected = 3
    Off = 4


class VPNStatusResponse(BaseModel):
    code: int
    status: ConnectionStatus
    uptime: int


class IP(BaseModel):
    mask: IPv4Address
    address: IPv4Address


class IPv4(BaseModel):
    mask: IPv4Address
    ip: IPv4Address


class PPOEStatus(BaseModel):
    proto: str
    dns: List[str]
    code: int
    pppoename: str
    peerdns: int
    ip: IP
    password: str
    cdns: List[str]
    status: int
    gw: str


class WiFiChannelInfo(BaseModel):
    bandwidth: int = None
    bandList: List[int]
    channel: int

    @validator('bandwidth')
    def convert_nil(cls, v):
        if v == 'nil':
            return None
        return v


class WiFiEncryptionTypes(str, Enum):
    psk2 = 'psk2'
    mixed_psk = 'mixed-psk'


class WiFiInterfaceInfo(BaseModel):
    ifname: str
    channelInfo: WiFiChannelInfo
    encryption: WiFiEncryptionTypes
    bandwidth: int = None
    kickthreshold: int
    status: int
    mode: str
    ssid: str
    weakthreshold: int
    device: str
    ax: int
    hidden: int
    password: str
    channel: int
    txpwr: str
    weakenable: int
    txbf: int
    signal: int


class WiFiDetails(BaseModel):
    bsd: int
    info: List[WiFiInterfaceInfo]
    code: int


class WANInfoDetails(BaseModel):
    username: str
    ifname: str
    dns: List[str]
    wanType: str
    mru: int
    service: str
    password: str
    peerdns: str


class IPV6Info(BaseModel):
    wanType: str


class WANInfo(BaseModel):
    mac: str
    link: int
    details: WANInfoDetails
    special: int
    dnsAddrs1: str
    status: int
    internet_tag: int
    dnsAddrs: str
    uptime: int
    gateWay: str
    ipv6_info: IPV6Info
    ipv6_show: int
    mtu: int
    ipv4: List[IP]


class WANDetails(BaseModel):
    code: int
    info: WANInfo


class MacFilterDeviceStatistics(BaseModel):
    mac: str
    maxdownloadspeed: int
    upload: int
    upspeed: int
    ip: str
    downspeed: int
    online: int
    dev: str
    maxuploadspeed: int
    download: int


class DeviceList(BaseModel):
    isap: int
    parent: str
    added: int = None
    ip: str
    port: int
    hostname: str
    mac: str
    origin_name: str
    ptype: int
    authority: dict
    company: dict
    push: int
    name: str
    times: int
    type: str
    statistics: MacFilterDeviceStatistics
    ctype: int
    online: int


class MacFilterInfo(BaseModel):
    weblist: List
    flist: List[DeviceList]
    code: int


class LanDHCPInfo(BaseModel):
    leasetime: str
    limit: int
    leasetimeUnit: str
    start: int
    leasetimeNum: int
    lanIp: List[IP]
    ignore: int


class LanDHCPDetails(BaseModel):
    code: int
    info: List[LanDHCPInfo]


class LanInfoInfo(BaseModel):
    mac: str
    uptime: int
    status: int
    dnsAddrs: str
    dnsAddrs1: str
    ipv4: List[IPv4]


class LanInfoDetails(BaseModel):
    code: int
    info: LanInfoInfo
    linkList: List[int]


class MacBindList(BaseModel):
    mac: str
    tag: int
    name: str
    ip: str


class MACBindInfo(BaseModel):
    devicelist: List[DeviceList]
    list: List[MacBindList]
    code: int


class DMZResponse(BaseModel):
    status: int
    lanip: str
    code: int


class PortForwardItem(BaseModel):
    proto: int
    name: str
    ftype: int
    destport: int
    srcport: int
    destip: str


class PortForwardList(BaseModel):
    status: int
    list: List[PortForwardItem]
    code: int


class DeviceListItemIPDetails(BaseModel):
    downspeed: int
    online: int
    active: int
    upspeed: int
    ip: IPv4Address


class DeviceListItemStatistics(BaseModel):
    downspeed: int
    online: int
    upspeed: int


class DeviceListItem(BaseModel):
    mac: str
    oname: str
    isap: int
    parent: str
    authority: dict
    push: int
    online: int
    name: str
    times: int
    ip: List[DeviceListItemIPDetails]
    statistics: DeviceListItemStatistics
    icon: str
    type: int


class DeviceListResponse(BaseModel):
    mac: str
    list: List[DeviceListItem]
    code: int


class NewStatusResponse(BaseModel):
    count: int
    code: int
    hardware: dict
    two_g: dict = Field(..., alias='2g')
    five_g: dict = Field(..., alias='5g')


class Time(BaseModel):
    min: int
    day: int
    index: int
    month: int
    year: int
    sec: int
    hour: int
    timezone: str


class TimeResponse(BaseModel):
    time: Time
    code: int


class QoSInfo(BaseModel):
    band: dict
    code: int
    status: dict
    local: dict
    guest: dict
    list: list


class SmartVPNConnectStatus(Enum):
    CONNECTED = 0
    DISSCONNECTED = 1


class SmartVPNMode(Enum):
    TRAFFIC_BY_DEVICE = 2
    TRAFFIC_BY_SEVICE = 1


class BasicStatus(Enum):
    ON = 1
    OFF = 0


class SmartVPNInfo(BaseModel):
    status: SmartVPNConnectStatus
    mode: SmartVPNMode
    ulist: Optional[List[str]]
    mlist: Optional[List[str]]
    name: Optional[dict]
    switch: BasicStatus


class SmartVPNInfoResponse(BaseModel):
    code: int
    info: SmartVPNInfo


class SmartVPNServiceUpdateFlag(Enum):
    ADD = 0
    DELETE = 1


class BasicCodeResponse(BaseModel):
    code: int


class BasicStatusResponse(BaseModel):
    code: int
    status: int


class VPNProto(str, Enum):
    L2TP = 'l2tp'
    PPOE = 'ppoe'


class VPNItem(BaseModel):
    username: str
    id: str
    password: str
    server: str
    proto: VPNProto


class VPNCurrentItem(VPNItem):
    auto: BasicStatus

    @validator('auto', pre=True)
    def convert_to_int(cls, v):
        return int(v)


class VPNResponse(BaseModel):
    code: int
    list: List[VPNItem]
    current: VPNCurrentItem
