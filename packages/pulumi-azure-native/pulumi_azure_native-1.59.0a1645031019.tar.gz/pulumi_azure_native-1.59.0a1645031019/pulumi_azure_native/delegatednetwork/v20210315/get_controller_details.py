# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetControllerDetailsResult',
    'AwaitableGetControllerDetailsResult',
    'get_controller_details',
    'get_controller_details_output',
]

@pulumi.output_type
class GetControllerDetailsResult:
    """
    Represents an instance of a DNC controller.
    """
    def __init__(__self__, dnc_app_id=None, dnc_endpoint=None, dnc_tenant_id=None, id=None, location=None, name=None, provisioning_state=None, resource_guid=None, tags=None, type=None):
        if dnc_app_id and not isinstance(dnc_app_id, str):
            raise TypeError("Expected argument 'dnc_app_id' to be a str")
        pulumi.set(__self__, "dnc_app_id", dnc_app_id)
        if dnc_endpoint and not isinstance(dnc_endpoint, str):
            raise TypeError("Expected argument 'dnc_endpoint' to be a str")
        pulumi.set(__self__, "dnc_endpoint", dnc_endpoint)
        if dnc_tenant_id and not isinstance(dnc_tenant_id, str):
            raise TypeError("Expected argument 'dnc_tenant_id' to be a str")
        pulumi.set(__self__, "dnc_tenant_id", dnc_tenant_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_guid and not isinstance(resource_guid, str):
            raise TypeError("Expected argument 'resource_guid' to be a str")
        pulumi.set(__self__, "resource_guid", resource_guid)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dncAppId")
    def dnc_app_id(self) -> str:
        """
        dnc application id should be used by customer to authenticate with dnc gateway.
        """
        return pulumi.get(self, "dnc_app_id")

    @property
    @pulumi.getter(name="dncEndpoint")
    def dnc_endpoint(self) -> str:
        """
        dnc endpoint url that customers can use to connect to
        """
        return pulumi.get(self, "dnc_endpoint")

    @property
    @pulumi.getter(name="dncTenantId")
    def dnc_tenant_id(self) -> str:
        """
        tenant id of dnc application id
        """
        return pulumi.get(self, "dnc_tenant_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        An identifier that represents the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Location of the resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The current state of dnc controller resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGuid")
    def resource_guid(self) -> str:
        """
        Resource guid.
        """
        return pulumi.get(self, "resource_guid")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetControllerDetailsResult(GetControllerDetailsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetControllerDetailsResult(
            dnc_app_id=self.dnc_app_id,
            dnc_endpoint=self.dnc_endpoint,
            dnc_tenant_id=self.dnc_tenant_id,
            id=self.id,
            location=self.location,
            name=self.name,
            provisioning_state=self.provisioning_state,
            resource_guid=self.resource_guid,
            tags=self.tags,
            type=self.type)


def get_controller_details(resource_group_name: Optional[str] = None,
                           resource_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetControllerDetailsResult:
    """
    Represents an instance of a DNC controller.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the resource. It must be a minimum of 3 characters, and a maximum of 63.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:delegatednetwork/v20210315:getControllerDetails', __args__, opts=opts, typ=GetControllerDetailsResult).value

    return AwaitableGetControllerDetailsResult(
        dnc_app_id=__ret__.dnc_app_id,
        dnc_endpoint=__ret__.dnc_endpoint,
        dnc_tenant_id=__ret__.dnc_tenant_id,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        resource_guid=__ret__.resource_guid,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_controller_details)
def get_controller_details_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                  resource_name: Optional[pulumi.Input[str]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetControllerDetailsResult]:
    """
    Represents an instance of a DNC controller.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the resource. It must be a minimum of 3 characters, and a maximum of 63.
    """
    ...
