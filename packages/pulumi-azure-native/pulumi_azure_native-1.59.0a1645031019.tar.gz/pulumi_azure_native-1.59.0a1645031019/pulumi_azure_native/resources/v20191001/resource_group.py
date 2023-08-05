# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = ['ResourceGroupArgs', 'ResourceGroup']

@pulumi.input_type
class ResourceGroupArgs:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_by: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a ResourceGroup resource.
        :param pulumi.Input[str] location: The location of the resource group. It cannot be changed after the resource group has been created. It must be one of the supported Azure locations.
        :param pulumi.Input[str] managed_by: The ID of the resource that manages this resource group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to create or update. Can include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags attached to the resource group.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if managed_by is not None:
            pulumi.set(__self__, "managed_by", managed_by)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource group. It cannot be changed after the resource group has been created. It must be one of the supported Azure locations.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the resource that manages this resource group.
        """
        return pulumi.get(self, "managed_by")

    @managed_by.setter
    def managed_by(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "managed_by", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource group to create or update. Can include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags attached to the resource group.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class ResourceGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_by: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Resource group information.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] location: The location of the resource group. It cannot be changed after the resource group has been created. It must be one of the supported Azure locations.
        :param pulumi.Input[str] managed_by: The ID of the resource that manages this resource group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group to create or update. Can include alphanumeric, underscore, parentheses, hyphen, period (except at end), and Unicode characters that match the allowed characters.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags attached to the resource group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[ResourceGroupArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource group information.

        :param str resource_name: The name of the resource.
        :param ResourceGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ResourceGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 managed_by: Optional[pulumi.Input[str]] = None,
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
            __props__ = ResourceGroupArgs.__new__(ResourceGroupArgs)

            __props__.__dict__["location"] = location
            __props__.__dict__["managed_by"] = managed_by
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["properties"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:resources:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20151101:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20160201:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20160701:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20160901:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20170510:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20180201:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20180501:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20190301:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20190501:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20190510:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20190701:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20190801:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20200601:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20200801:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20201001:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20210101:ResourceGroup"), pulumi.Alias(type_="azure-native:resources/v20210401:ResourceGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ResourceGroup, __self__).__init__(
            'azure-native:resources/v20191001:ResourceGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ResourceGroup':
        """
        Get an existing ResourceGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ResourceGroupArgs.__new__(ResourceGroupArgs)

        __props__.__dict__["location"] = None
        __props__.__dict__["managed_by"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["properties"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return ResourceGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource group. It cannot be changed after the resource group has been created. It must be one of the supported Azure locations.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="managedBy")
    def managed_by(self) -> pulumi.Output[Optional[str]]:
        """
        The ID of the resource that manages this resource group.
        """
        return pulumi.get(self, "managed_by")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output['outputs.ResourceGroupPropertiesResponse']:
        """
        The resource group properties.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The tags attached to the resource group.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource group.
        """
        return pulumi.get(self, "type")

