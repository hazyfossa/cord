import ipaddress as ip
from datetime import datetime

from cord.base_types import UNSET, Struct, Unset

type IPNetwork = ip.IPv4Network | ip.IPv6Network
type IPAdress = ip.IPv4Address | ip.IPv6Address


class IPNet(Struct):
    network: IPNetwork

    @classmethod
    def parse_cidr(cls, cidr: str) -> "IPNet":
        network = ip.ip_network(cidr, strict=False)
        return cls(network=network)

    def __str__(self) -> str:
        return str(self.network)


class LeaseRange(Struct):
    start_ip: IPAdress | Unset = UNSET
    end_ip: IPAdress | Unset = UNSET


class Subnet(Struct):
    subnet: IPNet | Unset = UNSET
    gateway: IPAdress | Unset = UNSET
    # NOTE: don't know why this specific one can be None instead of Unset
    lease_range: LeaseRange | None | Unset = UNSET


class Network(Struct):
    name: str | Unset = UNSET
    id: str | Unset = UNSET
    driver: str | Unset = UNSET
    network_interface: str | Unset = UNSET
    created: datetime | Unset = UNSET
    subnets: list[Subnet] | Unset = UNSET

    ipv6_enabled: bool = False  # TODO: Correct?
    internal: bool = False
    dns_enabled: bool = False

    labels: dict[str, str] | Unset = UNSET
    options: dict[str, str] | Unset = UNSET
    ipam_options: dict[str, str] | Unset = UNSET


class NetAddress(Struct):
    subnet: IPNet | Unset = UNSET
    gateway: IPAdress | Unset = UNSET


class NetInterface(Struct):
    networks: list[NetAddress] | Unset = UNSET
    # Represented as a string (e.g., "00:1A:2B:3C:4D:5E")
    mac_address: str | Unset = UNSET


class StatusBlock(Struct):
    interfaces: dict[str, NetInterface] | Unset = UNSET
    dns_server_ips: list[IPAdress] | Unset = UNSET
    dns_search_domains: list[str] | Unset = UNSET


class PerNetworkOptions(Struct):
    interface_name: str

    static_ips: list[IPAdress] | Unset = UNSET
    aliases: list[str] | Unset = UNSET
    # Represented as a string (e.g., "00:1A:2B:3C:4D:5E")
    static_mac: str | Unset = UNSET


class PortMapping(Struct):
    container_port: int

    host_port: int | Unset = UNSET
    host_ip: str | Unset = UNSET
    range: int | Unset = UNSET
    protocol: str | Unset = UNSET


class NetworkOptions(Struct):
    container_id: str | Unset = UNSET
    container_name: str | Unset = UNSET
    port_mappings: list[PortMapping] | Unset = UNSET
    networks: dict[str, PerNetworkOptions] | Unset = UNSET
