# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GuestDiagnosticsSettingsAssociationArgs', 'GuestDiagnosticsSettingsAssociation']

@pulumi.input_type
class GuestDiagnosticsSettingsAssociationArgs:
    def __init__(__self__, *,
                 guest_diagnostic_settings_name: pulumi.Input[str],
                 resource_uri: pulumi.Input[str],
                 association_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a GuestDiagnosticsSettingsAssociation resource.
        :param pulumi.Input[str] guest_diagnostic_settings_name: The guest diagnostic settings name.
        :param pulumi.Input[str] resource_uri: The fully qualified ID of the resource, including the resource name and resource type.
        :param pulumi.Input[str] association_name: The name of the diagnostic settings association.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        pulumi.set(__self__, "guest_diagnostic_settings_name", guest_diagnostic_settings_name)
        pulumi.set(__self__, "resource_uri", resource_uri)
        if association_name is not None:
            pulumi.set(__self__, "association_name", association_name)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="guestDiagnosticSettingsName")
    def guest_diagnostic_settings_name(self) -> pulumi.Input[str]:
        """
        The guest diagnostic settings name.
        """
        return pulumi.get(self, "guest_diagnostic_settings_name")

    @guest_diagnostic_settings_name.setter
    def guest_diagnostic_settings_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "guest_diagnostic_settings_name", value)

    @property
    @pulumi.getter(name="resourceUri")
    def resource_uri(self) -> pulumi.Input[str]:
        """
        The fully qualified ID of the resource, including the resource name and resource type.
        """
        return pulumi.get(self, "resource_uri")

    @resource_uri.setter
    def resource_uri(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_uri", value)

    @property
    @pulumi.getter(name="associationName")
    def association_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the diagnostic settings association.
        """
        return pulumi.get(self, "association_name")

    @association_name.setter
    def association_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "association_name", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class GuestDiagnosticsSettingsAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 association_name: Optional[pulumi.Input[str]] = None,
                 guest_diagnostic_settings_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Virtual machine guest diagnostic settings resource.
        API Version: 2018-06-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] association_name: The name of the diagnostic settings association.
        :param pulumi.Input[str] guest_diagnostic_settings_name: The guest diagnostic settings name.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] resource_uri: The fully qualified ID of the resource, including the resource name and resource type.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GuestDiagnosticsSettingsAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Virtual machine guest diagnostic settings resource.
        API Version: 2018-06-01-preview.

        :param str resource_name: The name of the resource.
        :param GuestDiagnosticsSettingsAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GuestDiagnosticsSettingsAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 association_name: Optional[pulumi.Input[str]] = None,
                 guest_diagnostic_settings_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_uri: Optional[pulumi.Input[str]] = None,
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
            __props__ = GuestDiagnosticsSettingsAssociationArgs.__new__(GuestDiagnosticsSettingsAssociationArgs)

            __props__.__dict__["association_name"] = association_name
            if guest_diagnostic_settings_name is None and not opts.urn:
                raise TypeError("Missing required property 'guest_diagnostic_settings_name'")
            __props__.__dict__["guest_diagnostic_settings_name"] = guest_diagnostic_settings_name
            __props__.__dict__["location"] = location
            if resource_uri is None and not opts.urn:
                raise TypeError("Missing required property 'resource_uri'")
            __props__.__dict__["resource_uri"] = resource_uri
            __props__.__dict__["tags"] = tags
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:insights/v20180601preview:GuestDiagnosticsSettingsAssociation")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(GuestDiagnosticsSettingsAssociation, __self__).__init__(
            'azure-native:insights:GuestDiagnosticsSettingsAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'GuestDiagnosticsSettingsAssociation':
        """
        Get an existing GuestDiagnosticsSettingsAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = GuestDiagnosticsSettingsAssociationArgs.__new__(GuestDiagnosticsSettingsAssociationArgs)

        __props__.__dict__["guest_diagnostic_settings_name"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return GuestDiagnosticsSettingsAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="guestDiagnosticSettingsName")
    def guest_diagnostic_settings_name(self) -> pulumi.Output[str]:
        """
        The guest diagnostic settings name.
        """
        return pulumi.get(self, "guest_diagnostic_settings_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")

