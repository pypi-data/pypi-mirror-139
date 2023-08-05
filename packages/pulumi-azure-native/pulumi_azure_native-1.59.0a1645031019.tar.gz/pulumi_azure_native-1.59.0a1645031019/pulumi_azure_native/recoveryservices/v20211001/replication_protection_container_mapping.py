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

__all__ = ['ReplicationProtectionContainerMappingArgs', 'ReplicationProtectionContainerMapping']

@pulumi.input_type
class ReplicationProtectionContainerMappingArgs:
    def __init__(__self__, *,
                 fabric_name: pulumi.Input[str],
                 protection_container_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 resource_name: pulumi.Input[str],
                 mapping_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['CreateProtectionContainerMappingInputPropertiesArgs']] = None):
        """
        The set of arguments for constructing a ReplicationProtectionContainerMapping resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input[str] protection_container_name: Protection container name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name: The name of the recovery services vault.
        :param pulumi.Input[str] mapping_name: Protection container mapping name.
        :param pulumi.Input['CreateProtectionContainerMappingInputPropertiesArgs'] properties: Configure protection input properties.
        """
        pulumi.set(__self__, "fabric_name", fabric_name)
        pulumi.set(__self__, "protection_container_name", protection_container_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "resource_name", resource_name)
        if mapping_name is not None:
            pulumi.set(__self__, "mapping_name", mapping_name)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)

    @property
    @pulumi.getter(name="fabricName")
    def fabric_name(self) -> pulumi.Input[str]:
        """
        Fabric name.
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
    @pulumi.getter(name="mappingName")
    def mapping_name(self) -> Optional[pulumi.Input[str]]:
        """
        Protection container mapping name.
        """
        return pulumi.get(self, "mapping_name")

    @mapping_name.setter
    def mapping_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mapping_name", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['CreateProtectionContainerMappingInputPropertiesArgs']]:
        """
        Configure protection input properties.
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['CreateProtectionContainerMappingInputPropertiesArgs']]):
        pulumi.set(self, "properties", value)


class ReplicationProtectionContainerMapping(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 mapping_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreateProtectionContainerMappingInputPropertiesArgs']]] = None,
                 protection_container_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_name_: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Protection container mapping object.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] fabric_name: Fabric name.
        :param pulumi.Input[str] mapping_name: Protection container mapping name.
        :param pulumi.Input[pulumi.InputType['CreateProtectionContainerMappingInputPropertiesArgs']] properties: Configure protection input properties.
        :param pulumi.Input[str] protection_container_name: Protection container name.
        :param pulumi.Input[str] resource_group_name: The name of the resource group where the recovery services vault is present.
        :param pulumi.Input[str] resource_name_: The name of the recovery services vault.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ReplicationProtectionContainerMappingArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Protection container mapping object.

        :param str resource_name: The name of the resource.
        :param ReplicationProtectionContainerMappingArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ReplicationProtectionContainerMappingArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 fabric_name: Optional[pulumi.Input[str]] = None,
                 mapping_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['CreateProtectionContainerMappingInputPropertiesArgs']]] = None,
                 protection_container_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = ReplicationProtectionContainerMappingArgs.__new__(ReplicationProtectionContainerMappingArgs)

            if fabric_name is None and not opts.urn:
                raise TypeError("Missing required property 'fabric_name'")
            __props__.__dict__["fabric_name"] = fabric_name
            __props__.__dict__["mapping_name"] = mapping_name
            __props__.__dict__["properties"] = properties
            if protection_container_name is None and not opts.urn:
                raise TypeError("Missing required property 'protection_container_name'")
            __props__.__dict__["protection_container_name"] = protection_container_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if resource_name_ is None and not opts.urn:
                raise TypeError("Missing required property 'resource_name_'")
            __props__.__dict__["resource_name"] = resource_name_
            __props__.__dict__["location"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:recoveryservices:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20160810:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20180110:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20180710:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210210:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210301:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210401:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210601:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210701:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20210801:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20211101:ReplicationProtectionContainerMapping"), pulumi.Alias(type_="azure-native:recoveryservices/v20211201:ReplicationProtectionContainerMapping")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ReplicationProtectionContainerMapping, __self__).__init__(
            'azure-native:recoveryservices/v20211001:ReplicationProtectionContainerMapping',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ReplicationProtectionContainerMapping':
        """
        Get an existing ReplicationProtectionContainerMapping resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ReplicationProtectionContainerMappingArgs.__new__(ReplicationProtectionContainerMappingArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["type"] = None
        return ReplicationProtectionContainerMapping(resource_name, opts=opts, __props__=__props__)

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
    def properties(self) -> pulumi.Output['outputs.ProtectionContainerMappingPropertiesResponse']:
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

