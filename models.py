from enum import Enum
from typing import List

from pydantic import BaseModel, validator, root_validator


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
    mask: str
    address: str


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
