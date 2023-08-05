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

__all__ = ['ReplicationProtectedItemArgs', 'ReplicationProtectedItem']

@pulumi.input_type
class ReplicationProtectedItemArgs:
    def __init__(__self__, *,
                 fabric_name: pulumi.Input[str],
                 protection_container_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 properties: Optional[pulumi.Input['EnableProtectionInputPropertiesArgs']] = None,
                 replicated_protected_item_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ReplicationProtectedItem resource.
        :param pulumi.Input[str] fabric_name: Name of the fabric.
        :param pulumi.Input[str] protection_container_name: Protection container name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input['EnableProtectionInputPropertiesArgs'] properties: Enable protection input properties.
        :param pulumi.Input[str] replicated_protected_item_name: A name for the replication protected item.
        """
        pulumi.set(__self__, "fabric_name", fabric_name)
        pulumi.set(__self__, "protection_container_name", protection_container_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if replicated_protected_item_name is not None:
            pulumi.set(__self__, "replicated_protected_item_name", replicated_protected_item_name)

    @property
    @pulumi.getter(name="fabricName")
    def fabric_name(self) -> pulumi.Input[str]:
        """
        Name of the fabric.
        """
        return pulumi.get(self, "fabric_name")

    @fabric_name.setter
    def fabric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "fabric_name", value)

    @property
    @pulumi.getter(name="protectionContainerName")
    def protection_container_name(self) -> pulumi.Input[str]:
        """
        Protection container name.
        """
        return pulumi.get(self, "protection_container_name")

    @protection_container_name.setter
    def protection_container_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "protection_container_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group where the recovery services vault is present.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="resourceName")
    def resource_name(self) -> pulumi.Input[str]:
        """
        The name of the recovery services vault.
        """
        return pulumi.get(self, "resource_name")

    @resource_name.setter
    def resource_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['EnableProtectionInputPropertiesArgs']]:
        """
        Enable protection input properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['EnableProtectionInputPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="replicatedProtectedItemName")
    def replicated_protected_item_name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the replication protected item.
        """
        return pulumi.get(self, "replicated_protected_item_name")

    @replicated_protected_item_name.setter
    def replicated_protected_item_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replicated_protected_item_name", value)


class ReplicationProtectedItem(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['EnableProtectionInputPropertiesArgs']]] = None,
                 protection_container_name: Optional[pulumi.Input[str]] = None,
                 replicated_protected_item_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Replication protected item.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fabric_name: Name of the fabric.
        :param pulumi.Input[pulumi.InputType['EnableProtectionInputPropertiesArgs']] properties: Enable protection input properties.
        :param pulumi.Input[str] protection_container_name: Protection container name.
        :param pulumi.Input[str] replicated_protected_item_name: A name for the replication protected item.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationProtectedItemArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Replication protected item.

        :param str resource_name: The name of the resource.
        :param ReplicationProtectedItemArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationProtectedItemArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['EnableProtectionInputPropertiesArgs']]] = None,
                 protection_container_name: Optional[pulumi.Input[str]] = None,
                 replicated_protected_item_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
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
            __props__ = ReplicationProtectedItemArgs.__new__(ReplicationProtectedItemArgs)

            if fabric_name is None and not opts.urn:
                raise TypeError("Missing required property 'fabric_name'")
            __props__.__dict__["fabric_name"] = fabric_name
            __props__.__dict__["properties"] = properties
            if protection_container_name is None and not opts.urn:
                raise TypeError("Missing required property 'protection_container_name'")
            __props__.__dict__["protection_container_name"] = protection_container_name
            __props__.__dict__["replicated_protected_item_name"] = replicated_protected_item_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20160810:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20180110:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20180710:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20211001:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20211101:ReplicationProtectedItem"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ReplicationProtectedItem")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationProtectedItem, __self__).__init__(
            'azure-native:recoveryservices/v20210210:ReplicationProtectedItem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ReplicationProtectedItem':
        """
        Get an existing ReplicationProtectedItem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReplicationProtectedItemArgs.__new__(ReplicationProtectedItemArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ReplicationProtectedItem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ReplicationProtectedItemPropertiesResponse']:
        """
        The custom data.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource Type
        """
        return pulumi.get(self, "type")

