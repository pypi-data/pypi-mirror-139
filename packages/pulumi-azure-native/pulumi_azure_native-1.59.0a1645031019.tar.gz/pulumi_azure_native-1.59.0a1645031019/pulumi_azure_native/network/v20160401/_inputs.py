# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ARecordArgs',
    'AaaaRecordArgs',
    'CnameRecordArgs',
    'MxRecordArgs',
    'NsRecordArgs',
    'PtrRecordArgs',
    'SoaRecordArgs',
    'SrvRecordArgs',
    'TxtRecordArgs',
]

@pulumi.input_type
class ARecordArgs:
    def __init__(__self__, *,
                 ipv4_address: Optional[pulumi.Input[str]] = None):
        """
        An A record.
        :param pulumi.Input[str] ipv4_address: The IPv4 address of this A record.
        """
        if ipv4_address is not None:
            pulumi.set(__self__, "ipv4_address", ipv4_address)

    @property
    @pulumi.getter(name="ipv4Address")
    def ipv4_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv4 address of this A record.
        """
        return pulumi.get(self, "ipv4_address")

    @ipv4_address.setter
    def ipv4_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipv4_address", value)


@pulumi.input_type
class AaaaRecordArgs:
    def __init__(__self__, *,
                 ipv6_address: Optional[pulumi.Input[str]] = None):
        """
        An AAAA record.
        :param pulumi.Input[str] ipv6_address: The IPv6 address of this AAAA record.
        """
        if ipv6_address is not None:
            pulumi.set(__self__, "ipv6_address", ipv6_address)

    @property
    @pulumi.getter(name="ipv6Address")
    def ipv6_address(self) -> Optional[pulumi.Input[str]]:
        """
        The IPv6 address of this AAAA record.
        """
        return pulumi.get(self, "ipv6_address")

    @ipv6_address.setter
    def ipv6_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ipv6_address", value)


@pulumi.input_type
class CnameRecordArgs:
    def __init__(__self__, *,
                 cname: Optional[pulumi.Input[str]] = None):
        """
        A CNAME record.
        :param pulumi.Input[str] cname: The canonical name for this CNAME record.
        """
        if cname is not None:
            pulumi.set(__self__, "cname", cname)

    @property
    @pulumi.getter
    def cname(self) -> Optional[pulumi.Input[str]]:
        """
        The canonical name for this CNAME record.
        """
        return pulumi.get(self, "cname")

    @cname.setter
    def cname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cname", value)


@pulumi.input_type
class MxRecordArgs:
    def __init__(__self__, *,
                 exchange: Optional[pulumi.Input[str]] = None,
                 preference: Optional[pulumi.Input[int]] = None):
        """
        An MX record.
        :param pulumi.Input[str] exchange: The domain name of the mail host for this MX record.
        :param pulumi.Input[int] preference: The preference value for this MX record.
        """
        if exchange is not None:
            pulumi.set(__self__, "exchange", exchange)
        if preference is not None:
            pulumi.set(__self__, "preference", preference)

    @property
    @pulumi.getter
    def exchange(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name of the mail host for this MX record.
        """
        return pulumi.get(self, "exchange")

    @exchange.setter
    def exchange(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "exchange", value)

    @property
    @pulumi.getter
    def preference(self) -> Optional[pulumi.Input[int]]:
        """
        The preference value for this MX record.
        """
        return pulumi.get(self, "preference")

    @preference.setter
    def preference(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "preference", value)


@pulumi.input_type
class NsRecordArgs:
    def __init__(__self__, *,
                 nsdname: Optional[pulumi.Input[str]] = None):
        """
        An NS record.
        :param pulumi.Input[str] nsdname: The name server name for this NS record.
        """
        if nsdname is not None:
            pulumi.set(__self__, "nsdname", nsdname)

    @property
    @pulumi.getter
    def nsdname(self) -> Optional[pulumi.Input[str]]:
        """
        The name server name for this NS record.
        """
        return pulumi.get(self, "nsdname")

    @nsdname.setter
    def nsdname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "nsdname", value)


@pulumi.input_type
class PtrRecordArgs:
    def __init__(__self__, *,
                 ptrdname: Optional[pulumi.Input[str]] = None):
        """
        A PTR record.
        :param pulumi.Input[str] ptrdname: The PTR target domain name for this PTR record.
        """
        if ptrdname is not None:
            pulumi.set(__self__, "ptrdname", ptrdname)

    @property
    @pulumi.getter
    def ptrdname(self) -> Optional[pulumi.Input[str]]:
        """
        The PTR target domain name for this PTR record.
        """
        return pulumi.get(self, "ptrdname")

    @ptrdname.setter
    def ptrdname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ptrdname", value)


@pulumi.input_type
class SoaRecordArgs:
    def __init__(__self__, *,
                 email: Optional[pulumi.Input[str]] = None,
                 expire_time: Optional[pulumi.Input[float]] = None,
                 host: Optional[pulumi.Input[str]] = None,
                 minimum_ttl: Optional[pulumi.Input[float]] = None,
                 refresh_time: Optional[pulumi.Input[float]] = None,
                 retry_time: Optional[pulumi.Input[float]] = None,
                 serial_number: Optional[pulumi.Input[float]] = None):
        """
        An SOA record.
        :param pulumi.Input[str] email: The email contact for this SOA record.
        :param pulumi.Input[float] expire_time: The expire time for this SOA record.
        :param pulumi.Input[str] host: The domain name of the authoritative name server for this SOA record.
        :param pulumi.Input[float] minimum_ttl: The minimum value for this SOA record. By convention this is used to determine the negative caching duration.
        :param pulumi.Input[float] refresh_time: The refresh value for this SOA record.
        :param pulumi.Input[float] retry_time: The retry time for this SOA record.
        :param pulumi.Input[float] serial_number: The serial number for this SOA record.
        """
        if email is not None:
            pulumi.set(__self__, "email", email)
        if expire_time is not None:
            pulumi.set(__self__, "expire_time", expire_time)
        if host is not None:
            pulumi.set(__self__, "host", host)
        if minimum_ttl is not None:
            pulumi.set(__self__, "minimum_ttl", minimum_ttl)
        if refresh_time is not None:
            pulumi.set(__self__, "refresh_time", refresh_time)
        if retry_time is not None:
            pulumi.set(__self__, "retry_time", retry_time)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        """
        The email contact for this SOA record.
        """
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="expireTime")
    def expire_time(self) -> Optional[pulumi.Input[float]]:
        """
        The expire time for this SOA record.
        """
        return pulumi.get(self, "expire_time")

    @expire_time.setter
    def expire_time(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "expire_time", value)

    @property
    @pulumi.getter
    def host(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name of the authoritative name server for this SOA record.
        """
        return pulumi.get(self, "host")

    @host.setter
    def host(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "host", value)

    @property
    @pulumi.getter(name="minimumTtl")
    def minimum_ttl(self) -> Optional[pulumi.Input[float]]:
        """
        The minimum value for this SOA record. By convention this is used to determine the negative caching duration.
        """
        return pulumi.get(self, "minimum_ttl")

    @minimum_ttl.setter
    def minimum_ttl(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "minimum_ttl", value)

    @property
    @pulumi.getter(name="refreshTime")
    def refresh_time(self) -> Optional[pulumi.Input[float]]:
        """
        The refresh value for this SOA record.
        """
        return pulumi.get(self, "refresh_time")

    @refresh_time.setter
    def refresh_time(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "refresh_time", value)

    @property
    @pulumi.getter(name="retryTime")
    def retry_time(self) -> Optional[pulumi.Input[float]]:
        """
        The retry time for this SOA record.
        """
        return pulumi.get(self, "retry_time")

    @retry_time.setter
    def retry_time(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "retry_time", value)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[pulumi.Input[float]]:
        """
        The serial number for this SOA record.
        """
        return pulumi.get(self, "serial_number")

    @serial_number.setter
    def serial_number(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "serial_number", value)


@pulumi.input_type
class SrvRecordArgs:
    def __init__(__self__, *,
                 port: Optional[pulumi.Input[int]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 weight: Optional[pulumi.Input[int]] = None):
        """
        An SRV record.
        :param pulumi.Input[int] port: The port value for this SRV record.
        :param pulumi.Input[int] priority: The priority value for this SRV record.
        :param pulumi.Input[str] target: The target domain name for this SRV record.
        :param pulumi.Input[int] weight: The weight value for this SRV record.
        """
        if port is not None:
            pulumi.set(__self__, "port", port)
        if priority is not None:
            pulumi.set(__self__, "priority", priority)
        if target is not None:
            pulumi.set(__self__, "target", target)
        if weight is not None:
            pulumi.set(__self__, "weight", weight)

    @property
    @pulumi.getter
    def port(self) -> Optional[pulumi.Input[int]]:
        """
        The port value for this SRV record.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "port", value)

    @property
    @pulumi.getter
    def priority(self) -> Optional[pulumi.Input[int]]:
        """
        The priority value for this SRV record.
        """
        return pulumi.get(self, "priority")

    @priority.setter
    def priority(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "priority", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        The target domain name for this SRV record.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter
    def weight(self) -> Optional[pulumi.Input[int]]:
        """
        The weight value for this SRV record.
        """
        return pulumi.get(self, "weight")

    @weight.setter
    def weight(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weight", value)


@pulumi.input_type
class TxtRecordArgs:
    def __init__(__self__, *,
                 value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        A TXT record.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] value: The text value of this TXT record.
        """
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The text value of this TXT record.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "value", value)


