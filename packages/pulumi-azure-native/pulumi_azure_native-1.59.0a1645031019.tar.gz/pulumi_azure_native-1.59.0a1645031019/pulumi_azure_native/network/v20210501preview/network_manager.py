# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['NetworkManagerArgs', 'NetworkManager']

@pulumi.input_type
class NetworkManagerArgs:
    def __init__(__self__, *,
                 network_manager_scope_accesses: pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]],
                 network_manager_scopes: pulumi.Input['NetworkManagerPropertiesNetworkManagerScopesArgs'],
                 resource_group_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a NetworkManager resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]] network_manager_scope_accesses: Scope Access.
        :param pulumi.Input['NetworkManagerPropertiesNetworkManagerScopesArgs'] network_manager_scopes: Scope of Network Manager.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] description: A description of the network manager.
        :param pulumi.Input[str] display_name: A friendly name for the network manager.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_manager_name: The name of the network manager.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        pulumi.set(__self__, "network_manager_scope_accesses", network_manager_scope_accesses)
        pulumi.set(__self__, "network_manager_scopes", network_manager_scopes)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if network_manager_name is not None:
            pulumi.set(__self__, "network_manager_name", network_manager_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="networkManagerScopeAccesses")
    def network_manager_scope_accesses(self) -> pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]]:
        """
        Scope Access.
        """
        return pulumi.get(self, "network_manager_scope_accesses")

    @network_manager_scope_accesses.setter
    def network_manager_scope_accesses(self, value: pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]]):
        pulumi.set(self, "network_manager_scope_accesses", value)

    @property
    @pulumi.getter(name="networkManagerScopes")
    def network_manager_scopes(self) -> pulumi.Input['NetworkManagerPropertiesNetworkManagerScopesArgs']:
        """
        Scope of Network Manager.
        """
        return pulumi.get(self, "network_manager_scopes")

    @network_manager_scopes.setter
    def network_manager_scopes(self, value: pulumi.Input['NetworkManagerPropertiesNetworkManagerScopesArgs']):
        pulumi.set(self, "network_manager_scopes", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        A description of the network manager.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[pulumi.Input[str]]:
        """
        A friendly name for the network manager.
        """
        return pulumi.get(self, "display_name")

    @display_name.setter
    def display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="networkManagerName")
    def network_manager_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the network manager.
        """
        return pulumi.get(self, "network_manager_name")

    @network_manager_name.setter
    def network_manager_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_manager_name", value)

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


class NetworkManager(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_name: Optional[pulumi.Input[str]] = None,
                 network_manager_scope_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]]] = None,
                 network_manager_scopes: Optional[pulumi.Input[pulumi.InputType['NetworkManagerPropertiesNetworkManagerScopesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The Managed Network resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: A description of the network manager.
        :param pulumi.Input[str] display_name: A friendly name for the network manager.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] network_manager_name: The name of the network manager.
        :param pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]] network_manager_scope_accesses: Scope Access.
        :param pulumi.Input[pulumi.InputType['NetworkManagerPropertiesNetworkManagerScopesArgs']] network_manager_scopes: Scope of Network Manager.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkManagerArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The Managed Network resource

        :param str resource_name: The name of the resource.
        :param NetworkManagerArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkManagerArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 network_manager_name: Optional[pulumi.Input[str]] = None,
                 network_manager_scope_accesses: Optional[pulumi.Input[Sequence[pulumi.Input[Union[str, 'ConfigurationType']]]]] = None,
                 network_manager_scopes: Optional[pulumi.Input[pulumi.InputType['NetworkManagerPropertiesNetworkManagerScopesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkManagerArgs.__new__(NetworkManagerArgs)

            __props__.__dict__["description"] = description
            __props__.__dict__["display_name"] = display_name
            __props__.__dict__["id"] = id
            __props__.__dict__["location"] = location
            __props__.__dict__["network_manager_name"] = network_manager_name
            if network_manager_scope_accesses is None and not opts.urn:
                raise TypeError("Missing required property 'network_manager_scope_accesses'")
            __props__.__dict__["network_manager_scope_accesses"] = network_manager_scope_accesses
            if network_manager_scopes is None and not opts.urn:
                raise TypeError("Missing required property 'network_manager_scopes'")
            __props__.__dict__["network_manager_scopes"] = network_manager_scopes
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:network:NetworkManager"), pulumi.Alias(type_="azure-native:network/v20210201preview:NetworkManager")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NetworkManager, __self__).__init__(
            'azure-native:network/v20210501preview:NetworkManager',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NetworkManager':
        """
        Get an existing NetworkManager resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = NetworkManagerArgs.__new__(NetworkManagerArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["display_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["network_manager_scope_accesses"] = None
        __props__.__dict__["network_manager_scopes"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return NetworkManager(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description of the network manager.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        A friendly name for the network manager.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkManagerScopeAccesses")
    def network_manager_scope_accesses(self) -> pulumi.Output[Sequence[str]]:
        """
        Scope Access.
        """
        return pulumi.get(self, "network_manager_scope_accesses")

    @property
    @pulumi.getter(name="networkManagerScopes")
    def network_manager_scopes(self) -> pulumi.Output['outputs.NetworkManagerPropertiesResponseNetworkManagerScopes']:
        """
        Scope of Network Manager.
        """
        return pulumi.get(self, "network_manager_scopes")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the scope assignment resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata related to this resource.
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
        Resource type.
        """
        return pulumi.get(self, "type")

