# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetIpGroupResult',
    'AwaitableGetIpGroupResult',
    'get_ip_group',
    'get_ip_group_output',
]

@pulumi.output_type
class GetIpGroupResult:
    """
    The IpGroups resource information.
    """
    def __init__(__self__, etag=None, firewalls=None, id=None, ip_addresses=None, location=None, name=None, provisioning_state=None, tags=None, type=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if firewalls and not isinstance(firewalls, list):
            raise TypeError("Expected argument 'firewalls' to be a list")
        pulumi.set(__self__, "firewalls", firewalls)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_addresses and not isinstance(ip_addresses, list):
            raise TypeError("Expected argument 'ip_addresses' to be a list")
        pulumi.set(__self__, "ip_addresses", ip_addresses)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def firewalls(self) -> Sequence['outputs.SubResourceResponse']:
        """
        List of references to Azure resources that this IpGroups is associated with.
        """
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[Sequence[str]]:
        """
        IpAddresses/IpAddressPrefixes in the IpGroups resource.
        """
        return pulumi.get(self, "ip_addresses")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the IpGroups resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetIpGroupResult(GetIpGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetIpGroupResult(
            etag=self.etag,
            firewalls=self.firewalls,
            id=self.id,
            ip_addresses=self.ip_addresses,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            tags=self.tags,
            type=self.type)


def get_ip_group(expand: Optional[str] = None,
                 ip_groups_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetIpGroupResult:
    """
    The IpGroups resource information.


    :param str expand: Expands resourceIds (of Firewalls/Network Security Groups etc.) back referenced by the IpGroups resource.
    :param str ip_groups_name: The name of the ipGroups.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['ipGroupsName'] = ip_groups_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20200301:getIpGroup', __args__, opts=opts, typ=GetIpGroupResult).value

    return AwaitableGetIpGroupResult(
        etag=__ret__.etag,
        firewalls=__ret__.firewalls,
        id=__ret__.id,
        ip_addresses=__ret__.ip_addresses,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_ip_group)
def get_ip_group_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                        ip_groups_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetIpGroupResult]:
    """
    The IpGroups resource information.


    :param str expand: Expands resourceIds (of Firewalls/Network Security Groups etc.) back referenced by the IpGroups resource.
    :param str ip_groups_name: The name of the ipGroups.
    :param str resource_group_name: The name of the resource group.
    """
    ...
