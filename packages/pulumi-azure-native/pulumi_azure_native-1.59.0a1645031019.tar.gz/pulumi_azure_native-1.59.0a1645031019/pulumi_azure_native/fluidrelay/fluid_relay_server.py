# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *

__all__ = ['FluidRelayServerArgs', 'FluidRelayServer']

@pulumi.input_type
class FluidRelayServerArgs:
    def __init__(__self__, *,
                 resource_group: pulumi.Input[str],
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a FluidRelayServer resource.
        :param pulumi.Input[str] resource_group: The resource group containing the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] name: The resource name.
        :param pulumi.Input[Union[str, 'ProvisioningState']] provisioning_state: Provision states for FluidRelay RP
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "resource_group", resource_group)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> pulumi.Input[str]:
        """
        The resource group containing the resource.
        """
        return pulumi.get(self, "resource_group")

    @resource_group.setter
    def resource_group(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[Union[str, 'ProvisioningState']]]:
        """
        Provision states for FluidRelay RP
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[Union[str, 'ProvisioningState']]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class FluidRelayServer(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A FluidRelay Server.
        API Version: 2021-03-12-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[str] name: The resource name.
        :param pulumi.Input[Union[str, 'ProvisioningState']] provisioning_state: Provision states for FluidRelay RP
        :param pulumi.Input[str] resource_group: The resource group containing the resource.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FluidRelayServerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A FluidRelay Server.
        API Version: 2021-03-12-preview.

        :param str resource_name: The name of the resource.
        :param FluidRelayServerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FluidRelayServerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ProvisioningState']]] = None,
                 resource_group: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FluidRelayServerArgs.__new__(FluidRelayServerArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            __props__.__dict__["provisioning_state"] = provisioning_state
            if resource_group is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group'")
            __props__.__dict__["resource_group"] = resource_group
            __props__.__dict__["tags"] = tags
            __props__.__dict__["fluid_relay_endpoints"] = None
            __props__.__dict__["frs_tenant_id"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:fluidrelay/v20210312preview:FluidRelayServer"), pulumi.Alias(type_="azure-native:fluidrelay/v20210615preview:FluidRelayServer"), pulumi.Alias(type_="azure-native:fluidrelay/v20210830preview:FluidRelayServer"), pulumi.Alias(type_="azure-native:fluidrelay/v20210910preview:FluidRelayServer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FluidRelayServer, __self__).__init__(
            'azure-native:fluidrelay:FluidRelayServer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FluidRelayServer':
        """
        Get an existing FluidRelayServer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = FluidRelayServerArgs.__new__(FluidRelayServerArgs)

        __props__.__dict__["fluid_relay_endpoints"] = None
        __props__.__dict__["frs_tenant_id"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return FluidRelayServer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="fluidRelayEndpoints")
    def fluid_relay_endpoints(self) -> pulumi.Output['outputs.FluidRelayEndpointsResponse']:
        """
        The Fluid Relay Service endpoints for this server.
        """
        return pulumi.get(self, "fluid_relay_endpoints")

    @property
    @pulumi.getter(name="frsTenantId")
    def frs_tenant_id(self) -> pulumi.Output[str]:
        """
        The Fluid tenantId for this server
        """
        return pulumi.get(self, "frs_tenant_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provision states for FluidRelay RP
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        System meta data for this resource, including creation and modification information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

