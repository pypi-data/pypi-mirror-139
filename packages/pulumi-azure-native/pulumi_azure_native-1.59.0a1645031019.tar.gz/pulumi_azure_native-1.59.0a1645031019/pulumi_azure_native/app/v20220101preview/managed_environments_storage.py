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

__all__ = ['ManagedEnvironmentsStorageArgs', 'ManagedEnvironmentsStorage']

@pulumi.input_type
class ManagedEnvironmentsStorageArgs:
    def __init__(__self__, *,
                 env_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['ManagedEnvironmentStoragePropertiesArgs']] = None):
        """
        The set of arguments for constructing a ManagedEnvironmentsStorage resource.
        :param pulumi.Input[str] env_name: Name of the Environment.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] name: Name of the storage.
        :param pulumi.Input['ManagedEnvironmentStoragePropertiesArgs'] properties: Storage properties
        """
        pulumi.set(__self__, "env_name", env_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="envName")
    def env_name(self) -> pulumi.Input[str]:
        """
        Name of the Environment.
        """
        return pulumi.get(self, "env_name")

    @env_name.setter
    def env_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "env_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the storage.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['ManagedEnvironmentStoragePropertiesArgs']]:
        """
        Storage properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['ManagedEnvironmentStoragePropertiesArgs']]):
        pulumi.set(self, "properties", value)


class ManagedEnvironmentsStorage(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ManagedEnvironmentStoragePropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Storage resource for managedEnvironment.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] env_name: Name of the Environment.
        :param pulumi.Input[str] name: Name of the storage.
        :param pulumi.Input[pulumi.InputType['ManagedEnvironmentStoragePropertiesArgs']] properties: Storage properties
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ManagedEnvironmentsStorageArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Storage resource for managedEnvironment.

        :param str resource_name: The name of the resource.
        :param ManagedEnvironmentsStorageArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ManagedEnvironmentsStorageArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 env_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ManagedEnvironmentStoragePropertiesArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ManagedEnvironmentsStorageArgs.__new__(ManagedEnvironmentsStorageArgs)

            if env_name is None and not opts.urn:
                raise TypeError("Missing required property 'env_name'")
            __props__.__dict__["env_name"] = env_name
            __props__.__dict__["name"] = name
            __props__.__dict__["properties"] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:app:ManagedEnvironmentsStorage")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedEnvironmentsStorage, __self__).__init__(
            'azure-native:app/v20220101preview:ManagedEnvironmentsStorage',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedEnvironmentsStorage':
        """
        Get an existing ManagedEnvironmentsStorage resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ManagedEnvironmentsStorageArgs.__new__(ManagedEnvironmentsStorageArgs)

        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["type"] = None
        return ManagedEnvironmentsStorage(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ManagedEnvironmentStorageResponseProperties']:
        """
        Storage properties
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

