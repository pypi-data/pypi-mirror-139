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

__all__ = ['WebAppAuthSettingsV2SlotArgs', 'WebAppAuthSettingsV2Slot']

@pulumi.input_type
class WebAppAuthSettingsV2SlotArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 slot: pulumi.Input[str],
                 global_validation: Optional[pulumi.Input['GlobalValidationArgs']] = None,
                 http_settings: Optional[pulumi.Input['HttpSettingsArgs']] = None,
                 identity_providers: Optional[pulumi.Input['IdentityProvidersArgs']] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input['LoginArgs']] = None,
                 platform: Optional[pulumi.Input['AuthPlatformArgs']] = None):
        """
        The set of arguments for constructing a WebAppAuthSettingsV2Slot resource.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
        :param pulumi.Input[str] kind: Kind of resource.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "slot", slot)
        if global_validation is not None:
            pulumi.set(__self__, "global_validation", global_validation)
        if http_settings is not None:
            pulumi.set(__self__, "http_settings", http_settings)
        if identity_providers is not None:
            pulumi.set(__self__, "identity_providers", identity_providers)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if login is not None:
            pulumi.set(__self__, "login", login)
        if platform is not None:
            pulumi.set(__self__, "platform", platform)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of web app.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def slot(self) -> pulumi.Input[str]:
        """
        Name of web app slot. If not specified then will default to production slot.
        """
        return pulumi.get(self, "slot")

    @slot.setter
    def slot(self, value: pulumi.Input[str]):
        pulumi.set(self, "slot", value)

    @property
    @pulumi.getter(name="globalValidation")
    def global_validation(self) -> Optional[pulumi.Input['GlobalValidationArgs']]:
        return pulumi.get(self, "global_validation")

    @global_validation.setter
    def global_validation(self, value: Optional[pulumi.Input['GlobalValidationArgs']]):
        pulumi.set(self, "global_validation", value)

    @property
    @pulumi.getter(name="httpSettings")
    def http_settings(self) -> Optional[pulumi.Input['HttpSettingsArgs']]:
        return pulumi.get(self, "http_settings")

    @http_settings.setter
    def http_settings(self, value: Optional[pulumi.Input['HttpSettingsArgs']]):
        pulumi.set(self, "http_settings", value)

    @property
    @pulumi.getter(name="identityProviders")
    def identity_providers(self) -> Optional[pulumi.Input['IdentityProvidersArgs']]:
        return pulumi.get(self, "identity_providers")

    @identity_providers.setter
    def identity_providers(self, value: Optional[pulumi.Input['IdentityProvidersArgs']]):
        pulumi.set(self, "identity_providers", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def login(self) -> Optional[pulumi.Input['LoginArgs']]:
        return pulumi.get(self, "login")

    @login.setter
    def login(self, value: Optional[pulumi.Input['LoginArgs']]):
        pulumi.set(self, "login", value)

    @property
    @pulumi.getter
    def platform(self) -> Optional[pulumi.Input['AuthPlatformArgs']]:
        return pulumi.get(self, "platform")

    @platform.setter
    def platform(self, value: Optional[pulumi.Input['AuthPlatformArgs']]):
        pulumi.set(self, "platform", value)


class WebAppAuthSettingsV2Slot(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_validation: Optional[pulumi.Input[pulumi.InputType['GlobalValidationArgs']]] = None,
                 http_settings: Optional[pulumi.Input[pulumi.InputType['HttpSettingsArgs']]] = None,
                 identity_providers: Optional[pulumi.Input[pulumi.InputType['IdentityProvidersArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input[pulumi.InputType['LoginArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[pulumi.InputType['AuthPlatformArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a WebAppAuthSettingsV2Slot resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of web app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of web app slot. If not specified then will default to production slot.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebAppAuthSettingsV2SlotArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a WebAppAuthSettingsV2Slot resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param WebAppAuthSettingsV2SlotArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppAuthSettingsV2SlotArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 global_validation: Optional[pulumi.Input[pulumi.InputType['GlobalValidationArgs']]] = None,
                 http_settings: Optional[pulumi.Input[pulumi.InputType['HttpSettingsArgs']]] = None,
                 identity_providers: Optional[pulumi.Input[pulumi.InputType['IdentityProvidersArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 login: Optional[pulumi.Input[pulumi.InputType['LoginArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 platform: Optional[pulumi.Input[pulumi.InputType['AuthPlatformArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
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
            __props__ = WebAppAuthSettingsV2SlotArgs.__new__(WebAppAuthSettingsV2SlotArgs)

            __props__.__dict__["global_validation"] = global_validation
            __props__.__dict__["http_settings"] = http_settings
            __props__.__dict__["identity_providers"] = identity_providers
            __props__.__dict__["kind"] = kind
            __props__.__dict__["login"] = login
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            __props__.__dict__["platform"] = platform
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__.__dict__["slot"] = slot
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20200901:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20201001:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20201201:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20210101:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20210115:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20210201:WebAppAuthSettingsV2Slot"), pulumi.Alias(type_="azure-native:web/v20210301:WebAppAuthSettingsV2Slot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppAuthSettingsV2Slot, __self__).__init__(
            'azure-native:web/v20200601:WebAppAuthSettingsV2Slot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppAuthSettingsV2Slot':
        """
        Get an existing WebAppAuthSettingsV2Slot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebAppAuthSettingsV2SlotArgs.__new__(WebAppAuthSettingsV2SlotArgs)

        __props__.__dict__["global_validation"] = None
        __props__.__dict__["http_settings"] = None
        __props__.__dict__["identity_providers"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["login"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["platform"] = None
        __props__.__dict__["type"] = None
        return WebAppAuthSettingsV2Slot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="globalValidation")
    def global_validation(self) -> pulumi.Output[Optional['outputs.GlobalValidationResponse']]:
        return pulumi.get(self, "global_validation")

    @property
    @pulumi.getter(name="httpSettings")
    def http_settings(self) -> pulumi.Output[Optional['outputs.HttpSettingsResponse']]:
        return pulumi.get(self, "http_settings")

    @property
    @pulumi.getter(name="identityProviders")
    def identity_providers(self) -> pulumi.Output[Optional['outputs.IdentityProvidersResponse']]:
        return pulumi.get(self, "identity_providers")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def login(self) -> pulumi.Output[Optional['outputs.LoginResponse']]:
        return pulumi.get(self, "login")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> pulumi.Output[Optional['outputs.AuthPlatformResponse']]:
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

