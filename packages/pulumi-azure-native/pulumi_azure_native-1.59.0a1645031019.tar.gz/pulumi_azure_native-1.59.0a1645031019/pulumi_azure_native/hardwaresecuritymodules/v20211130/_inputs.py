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
    'ApiEntityReferenceArgs',
    'NetworkInterfaceArgs',
    'NetworkProfileArgs',
    'SkuArgs',
]

@pulumi.input_type
class ApiEntityReferenceArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None):
        """
        The API entity reference.
        :param pulumi.Input[str] id: The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ARM resource id in the form of /subscriptions/{SubscriptionId}/resourceGroups/{ResourceGroupName}/...
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class NetworkInterfaceArgs:
    def __init__(__self__, *,
                 private_ip_address: Optional[pulumi.Input[str]] = None):
        """
        The network interface definition.
        :param pulumi.Input[str] private_ip_address: Private Ip address of the interface
        """
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Private Ip address of the interface
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)


@pulumi.input_type
class NetworkProfileArgs:
    def __init__(__self__, *,
                 network_interfaces: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfaceArgs']]]] = None,
                 subnet: Optional[pulumi.Input['ApiEntityReferenceArgs']] = None):
        """
        The network profile definition.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkInterfaceArgs']]] network_interfaces: Specifies the list of resource Ids for the network interfaces associated with the dedicated HSM.
        :param pulumi.Input['ApiEntityReferenceArgs'] subnet: Specifies the identifier of the subnet.
        """
        if network_interfaces is not None:
            pulumi.set(__self__, "network_interfaces", network_interfaces)
        if subnet is not None:
            pulumi.set(__self__, "subnet", subnet)

    @property
    @pulumi.getter(name="networkInterfaces")
    def network_interfaces(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfaceArgs']]]]:
        """
        Specifies the list of resource Ids for the network interfaces associated with the dedicated HSM.
        """
        return pulumi.get(self, "network_interfaces")

    @network_interfaces.setter
    def network_interfaces(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkInterfaceArgs']]]]):
        pulumi.set(self, "network_interfaces", value)

    @property
    @pulumi.getter
    def subnet(self) -> Optional[pulumi.Input['ApiEntityReferenceArgs']]:
        """
        Specifies the identifier of the subnet.
        """
        return pulumi.get(self, "subnet")

    @subnet.setter
    def subnet(self, value: Optional[pulumi.Input['ApiEntityReferenceArgs']]):
        pulumi.set(self, "subnet", value)


@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[Union[str, 'SkuName']]] = None):
        """
        SKU of the dedicated HSM
        :param pulumi.Input[Union[str, 'SkuName']] name: SKU of the dedicated HSM
        """
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'SkuName']]]:
        """
        SKU of the dedicated HSM
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'SkuName']]]):
        pulumi.set(self, "name", value)


