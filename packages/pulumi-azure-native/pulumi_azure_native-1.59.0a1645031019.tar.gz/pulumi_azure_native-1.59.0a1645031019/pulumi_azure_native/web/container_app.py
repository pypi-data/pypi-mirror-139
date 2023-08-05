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

__all__ = ['ContainerAppArgs', 'ContainerApp']

@pulumi.input_type
class ContainerAppArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 configuration: Optional[pulumi.Input['ConfigurationArgs']] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template: Optional[pulumi.Input['TemplateArgs']] = None):
        """
        The set of arguments for constructing a ContainerApp resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input['ConfigurationArgs'] configuration: Non versioned Container App configuration properties.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] kube_environment_id: Resource ID of the Container App's KubeEnvironment.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the Container App.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input['TemplateArgs'] template: Container App versioned application definition.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if configuration is not None:
            pulumi.set(__self__, "configuration", configuration)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if kube_environment_id is not None:
            pulumi.set(__self__, "kube_environment_id", kube_environment_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if template is not None:
            pulumi.set(__self__, "template", template)

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
    def configuration(self) -> Optional[pulumi.Input['ConfigurationArgs']]:
        """
        Non versioned Container App configuration properties.
        """
        return pulumi.get(self, "configuration")

    @configuration.setter
    def configuration(self, value: Optional[pulumi.Input['ConfigurationArgs']]):
        pulumi.set(self, "configuration", value)

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
    @pulumi.getter(name="kubeEnvironmentId")
    def kube_environment_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource ID of the Container App's KubeEnvironment.
        """
        return pulumi.get(self, "kube_environment_id")

    @kube_environment_id.setter
    def kube_environment_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kube_environment_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Container App.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

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
    @pulumi.getter
    def template(self) -> Optional[pulumi.Input['TemplateArgs']]:
        """
        Container App versioned application definition.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Optional[pulumi.Input['TemplateArgs']]):
        pulumi.set(self, "template", value)


class ContainerApp(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['ConfigurationArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template: Optional[pulumi.Input[pulumi.InputType['TemplateArgs']]] = None,
                 __props__=None):
        """
        Container App.
        API Version: 2021-03-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ConfigurationArgs']] configuration: Non versioned Container App configuration properties.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] kube_environment_id: Resource ID of the Container App's KubeEnvironment.
        :param pulumi.Input[str] location: Resource Location.
        :param pulumi.Input[str] name: Name of the Container App.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[pulumi.InputType['TemplateArgs']] template: Container App versioned application definition.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerAppArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Container App.
        API Version: 2021-03-01.

        :param str resource_name: The name of the resource.
        :param ContainerAppArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerAppArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configuration: Optional[pulumi.Input[pulumi.InputType['ConfigurationArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 kube_environment_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 template: Optional[pulumi.Input[pulumi.InputType['TemplateArgs']]] = None,
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
            __props__ = ContainerAppArgs.__new__(ContainerAppArgs)

            __props__.__dict__["configuration"] = configuration
            __props__.__dict__["kind"] = kind
            __props__.__dict__["kube_environment_id"] = kube_environment_id
            __props__.__dict__["location"] = location
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["template"] = template
            __props__.__dict__["latest_revision_fqdn"] = None
            __props__.__dict__["latest_revision_name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web/v20210301:ContainerApp")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ContainerApp, __self__).__init__(
            'azure-native:web:ContainerApp',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ContainerApp':
        """
        Get an existing ContainerApp resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = ContainerAppArgs.__new__(ContainerAppArgs)

        __props__.__dict__["configuration"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["kube_environment_id"] = None
        __props__.__dict__["latest_revision_fqdn"] = None
        __props__.__dict__["latest_revision_name"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["template"] = None
        __props__.__dict__["type"] = None
        return ContainerApp(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def configuration(self) -> pulumi.Output[Optional['outputs.ConfigurationResponse']]:
        """
        Non versioned Container App configuration properties.
        """
        return pulumi.get(self, "configuration")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="kubeEnvironmentId")
    def kube_environment_id(self) -> pulumi.Output[Optional[str]]:
        """
        Resource ID of the Container App's KubeEnvironment.
        """
        return pulumi.get(self, "kube_environment_id")

    @property
    @pulumi.getter(name="latestRevisionFqdn")
    def latest_revision_fqdn(self) -> pulumi.Output[str]:
        """
        Fully Qualified Domain Name of the latest revision of the Container App.
        """
        return pulumi.get(self, "latest_revision_fqdn")

    @property
    @pulumi.getter(name="latestRevisionName")
    def latest_revision_name(self) -> pulumi.Output[str]:
        """
        Name of the latest revision of the Container App.
        """
        return pulumi.get(self, "latest_revision_name")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource Location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Provisioning state of the Container App.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def template(self) -> pulumi.Output[Optional['outputs.TemplateResponse']]:
        """
        Container App versioned application definition.
        """
        return pulumi.get(self, "template")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

