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
    'GetPublicIPPrefixResult',
    'AwaitableGetPublicIPPrefixResult',
    'get_public_ip_prefix',
    'get_public_ip_prefix_output',
]

@pulumi.output_type
class GetPublicIPPrefixResult:
    """
    Public IP prefix resource.
    """
    def __init__(__self__, etag=None, id=None, ip_prefix=None, ip_tags=None, load_balancer_frontend_ip_configuration=None, location=None, name=None, prefix_length=None, provisioning_state=None, public_ip_address_version=None, public_ip_addresses=None, resource_guid=None, sku=None, tags=None, type=None, zones=None):
        if etag and not isinstance(etag, str):
            raise TypeError("Expected argument 'etag' to be a str")
        pulumi.set(__self__, "etag", etag)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_prefix and not isinstance(ip_prefix, str):
            raise TypeError("Expected argument 'ip_prefix' to be a str")
        pulumi.set(__self__, "ip_prefix", ip_prefix)
        if ip_tags and not isinstance(ip_tags, list):
            raise TypeError("Expected argument 'ip_tags' to be a list")
        pulumi.set(__self__, "ip_tags", ip_tags)
        if load_balancer_frontend_ip_configuration and not isinstance(load_balancer_frontend_ip_configuration, dict):
            raise TypeError("Expected argument 'load_balancer_frontend_ip_configuration' to be a dict")
        pulumi.set(__self__, "load_balancer_frontend_ip_configuration", load_balancer_frontend_ip_configuration)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if prefix_length and not isinstance(prefix_length, int):
            raise TypeError("Expected argument 'prefix_length' to be a int")
        pulumi.set(__self__, "prefix_length", prefix_length)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_ip_address_version and not isinstance(public_ip_address_version, str):
            raise TypeError("Expected argument 'public_ip_address_version' to be a str")
        pulumi.set(__self__, "public_ip_address_version", public_ip_address_version)
        if public_ip_addresses and not isinstance(public_ip_addresses, list):
            raise TypeError("Expected argument 'public_ip_addresses' to be a list")
        pulumi.set(__self__, "public_ip_addresses", public_ip_addresses)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if zones and not isinstance(zones, list):
            raise TypeError("Expected argument 'zones' to be a list")
        pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def etag(self) -> str:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipPrefix")
    def ip_prefix(self) -> str:
        """
        The allocated Prefix.
        """
        return pulumi.get(self, "ip_prefix")

    @property
    @pulumi.getter(name="ipTags")
    def ip_tags(self) -> Optional[Sequence['outputs.IpTagResponse']]:
        """
        The list of tags associated with the public IP prefix.
        """
        return pulumi.get(self, "ip_tags")

    @property
    @pulumi.getter(name="loadBalancerFrontendIpConfiguration")
    def load_balancer_frontend_ip_configuration(self) -> 'outputs.SubResourceResponse':
        """
        The reference to load balancer frontend IP configuration associated with the public IP prefix.
        """
        return pulumi.get(self, "load_balancer_frontend_ip_configuration")

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
    @pulumi.getter(name="prefixLength")
    def prefix_length(self) -> Optional[int]:
        """
        The Length of the Public IP Prefix.
        """
        return pulumi.get(self, "prefix_length")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the public IP prefix resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicIPAddressVersion")
    def public_ip_address_version(self) -> Optional[str]:
        """
        The public IP address version.
        """
        return pulumi.get(self, "public_ip_address_version")

    @property
    @pulumi.getter(name="publicIPAddresses")
    def public_ip_addresses(self) -> Sequence['outputs.ReferencedPublicIpAddressResponse']:
        """
        The list of all referenced PublicIPAddresses.
        """
        return pulumi.get(self, "public_ip_addresses")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> str:
        """
        The resource GUID property of the public IP prefix resource.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.PublicIPPrefixSkuResponse']:
        """
        The public IP prefix SKU.
        """
        return pulumi.get(self, "sku")

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

    @property
    @pulumi.getter
    def zones(self) -> Optional[Sequence[str]]:
        """
        A list of availability zones denoting the IP allocated for the resource needs to come from.
        """
        return pulumi.get(self, "zones")


class AwaitableGetPublicIPPrefixResult(GetPublicIPPrefixResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicIPPrefixResult(
            etag=self.etag,
            id=self.id,
            ip_prefix=self.ip_prefix,
            ip_tags=self.ip_tags,
            load_balancer_frontend_ip_configuration=self.load_balancer_frontend_ip_configuration,
            location=self.location,
            name=self.name,
            prefix_length=self.prefix_length,
            provisioning_state=self.provisioning_state,
            public_ip_address_version=self.public_ip_address_version,
            public_ip_addresses=self.public_ip_addresses,
            resource_guid=self.resource_guid,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            zones=self.zones)


def get_public_ip_prefix(expand: Optional[str] = None,
                         public_ip_prefix_name: Optional[str] = None,
                         resource_group_name: Optional[str] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPublicIPPrefixResult:
    """
    Public IP prefix resource.


    :param str expand: Expands referenced resources.
    :param str public_ip_prefix_name: The name of the public IP prefix.
    :param str resource_group_name: The name of the resource group.
    """
    __args__ = dict()
    __args__['expand'] = expand
    __args__['publicIpPrefixName'] = public_ip_prefix_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:network/v20190901:getPublicIPPrefix', __args__, opts=opts, typ=GetPublicIPPrefixResult).value

    return AwaitableGetPublicIPPrefixResult(
        etag=__ret__.etag,
        id=__ret__.id,
        ip_prefix=__ret__.ip_prefix,
        ip_tags=__ret__.ip_tags,
        load_balancer_frontend_ip_configuration=__ret__.load_balancer_frontend_ip_configuration,
        location=__ret__.location,
        name=__ret__.name,
        prefix_length=__ret__.prefix_length,
        provisioning_state=__ret__.provisioning_state,
        public_ip_address_version=__ret__.public_ip_address_version,
        public_ip_addresses=__ret__.public_ip_addresses,
        resource_guid=__ret__.resource_guid,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        zones=__ret__.zones)


@_utilities.lift_output_func(get_public_ip_prefix)
def get_public_ip_prefix_output(expand: Optional[pulumi.Input[Optional[str]]] = None,
                                public_ip_prefix_name: Optional[pulumi.Input[str]] = None,
                                resource_group_name: Optional[pulumi.Input[str]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPublicIPPrefixResult]:
    """
    Public IP prefix resource.


    :param str expand: Expands referenced resources.
    :param str public_ip_prefix_name: The name of the public IP prefix.
    :param str resource_group_name: The name of the resource group.
    """
    ...
