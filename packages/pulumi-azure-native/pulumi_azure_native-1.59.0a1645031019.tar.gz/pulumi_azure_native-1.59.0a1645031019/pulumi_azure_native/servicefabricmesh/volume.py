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
from ._inputs import *

__all__ = ['VolumeArgs', 'Volume']

@pulumi.input_type
class VolumeArgs:
    def __init__(__self__, *,
                 provider: pulumi.Input[Union[str, 'VolumeProvider']],
                 resource_group_name: pulumi.Input[str],
                 azure_file_parameters: Optional[pulumi.Input['VolumeProviderParametersAzureFileArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_resource_name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Volume resource.
        :param pulumi.Input[Union[str, 'VolumeProvider']] provider: Provider of the volume.
        :param pulumi.Input[str] resource_group_name: Azure resource group name
        :param pulumi.Input['VolumeProviderParametersAzureFileArgs'] azure_file_parameters: This type describes a volume provided by an Azure Files file share.
        :param pulumi.Input[str] description: User readable description of the volume.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] volume_resource_name: The identity of the volume.
        """
        pulumi.set(__self__, "provider", provider)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if azure_file_parameters is not None:
            pulumi.set(__self__, "azure_file_parameters", azure_file_parameters)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if volume_resource_name is not None:
            pulumi.set(__self__, "volume_resource_name", volume_resource_name)

    @property
    @pulumi.getter
    def provider(self) -> pulumi.Input[Union[str, 'VolumeProvider']]:
        """
        Provider of the volume.
        """
        return pulumi.get(self, "provider")

    @provider.setter
    def provider(self, value: pulumi.Input[Union[str, 'VolumeProvider']]):
        pulumi.set(self, "provider", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Azure resource group name
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="azureFileParameters")
    def azure_file_parameters(self) -> Optional[pulumi.Input['VolumeProviderParametersAzureFileArgs']]:
        """
        This type describes a volume provided by an Azure Files file share.
        """
        return pulumi.get(self, "azure_file_parameters")

    @azure_file_parameters.setter
    def azure_file_parameters(self, value: Optional[pulumi.Input['VolumeProviderParametersAzureFileArgs']]):
        pulumi.set(self, "azure_file_parameters", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User readable description of the volume.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

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
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="volumeResourceName")
    def volume_resource_name(self) -> Optional[pulumi.Input[str]]:
        """
        The identity of the volume.
        """
        return pulumi.get(self, "volume_resource_name")

    @volume_resource_name.setter
    def volume_resource_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "volume_resource_name", value)


class Volume(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azure_file_parameters: Optional[pulumi.Input[pulumi.InputType['VolumeProviderParametersAzureFileArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provider: Optional[pulumi.Input[Union[str, 'VolumeProvider']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_resource_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        This type describes a volume resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['VolumeProviderParametersAzureFileArgs']] azure_file_parameters: This type describes a volume provided by an Azure Files file share.
        :param pulumi.Input[str] description: User readable description of the volume.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'VolumeProvider']] provider: Provider of the volume.
        :param pulumi.Input[str] resource_group_name: Azure resource group name
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] volume_resource_name: The identity of the volume.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VolumeArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        This type describes a volume resource.
        API Version: 2018-09-01-preview.

        :param str resource_name: The name of the resource.
        :param VolumeArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VolumeArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 azure_file_parameters: Optional[pulumi.Input[pulumi.InputType['VolumeProviderParametersAzureFileArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 provider: Optional[pulumi.Input[Union[str, 'VolumeProvider']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_resource_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = VolumeArgs.__new__(VolumeArgs)

            __props__.__dict__["azure_file_parameters"] = azure_file_parameters
            __props__.__dict__["description"] = description
            __props__.__dict__["location"] = location
            if provider is None and not opts.urn:
                raise TypeError("Missing required property 'provider'")
            __props__.__dict__["provider"] = provider
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["volume_resource_name"] = volume_resource_name
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["status"] = None
            __props__.__dict__["status_details"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:servicefabricmesh/v20180701preview:Volume"), pulumi.Alias(type_="azure-native:servicefabricmesh/v20180901preview:Volume")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Volume, __self__).__init__(
            'azure-native:servicefabricmesh:Volume',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Volume':
        """
        Get an existing Volume resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VolumeArgs.__new__(VolumeArgs)

        __props__.__dict__["azure_file_parameters"] = None
        __props__.__dict__["description"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provider"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["status"] = None
        __props__.__dict__["status_details"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return Volume(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="azureFileParameters")
    def azure_file_parameters(self) -> pulumi.Output[Optional['outputs.VolumeProviderParametersAzureFileResponse']]:
        """
        This type describes a volume provided by an Azure Files file share.
        """
        return pulumi.get(self, "azure_file_parameters")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        User readable description of the volume.
        """
        return pulumi.get(self, "description")

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
    @pulumi.getter
    def provider(self) -> pulumi.Output[str]:
        """
        Provider of the volume.
        """
        return pulumi.get(self, "provider")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the volume.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> pulumi.Output[str]:
        """
        Gives additional information about the current status of the volume.
        """
        return pulumi.get(self, "status_details")

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
        The type of the resource. Ex- Microsoft.Compute/virtualMachines or Microsoft.Storage/storageAccounts.
        """
        return pulumi.get(self, "type")

