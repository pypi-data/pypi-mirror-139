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

__all__ = ['SecurityConnectorArgs', 'SecurityConnector']

@pulumi.input_type
class SecurityConnectorArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 cloud_name: Optional[pulumi.Input[Union[str, 'CloudName']]] = None,
                 hierarchy_identifier: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 offerings: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CspmMonitorAwsOfferingArgs', 'DefenderForContainersAwsOfferingArgs', 'DefenderForServersAwsOfferingArgs', 'InformationProtectionAwsOfferingArgs']]]]] = None,
                 organizational_data: Optional[pulumi.Input['SecurityConnectorPropertiesOrganizationalDataArgs']] = None,
                 security_connector_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a SecurityConnector resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[Union[str, 'CloudName']] cloud_name: The multi cloud resource's cloud name.
        :param pulumi.Input[str] hierarchy_identifier: The multi cloud resource identifier (account id in case of AWS connector).
        :param pulumi.Input[str] kind: Kind of the resource
        :param pulumi.Input[str] location: Location where the resource is stored
        :param pulumi.Input[Sequence[pulumi.Input[Union['CspmMonitorAwsOfferingArgs', 'DefenderForContainersAwsOfferingArgs', 'DefenderForServersAwsOfferingArgs', 'InformationProtectionAwsOfferingArgs']]]] offerings: A collection of offerings for the security connector.
        :param pulumi.Input['SecurityConnectorPropertiesOrganizationalDataArgs'] organizational_data: The multi cloud account's organizational data
        :param pulumi.Input[str] security_connector_name: The security connector name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A list of key value pairs that describe the resource.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if cloud_name is not None:
            pulumi.set(__self__, "cloud_name", cloud_name)
        if hierarchy_identifier is not None:
            pulumi.set(__self__, "hierarchy_identifier", hierarchy_identifier)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if offerings is not None:
            pulumi.set(__self__, "offerings", offerings)
        if organizational_data is not None:
            pulumi.set(__self__, "organizational_data", organizational_data)
        if security_connector_name is not None:
            pulumi.set(__self__, "security_connector_name", security_connector_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group within the user's subscription. The name is case insensitive.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="cloudName")
    def cloud_name(self) -> Optional[pulumi.Input[Union[str, 'CloudName']]]:
        """
        The multi cloud resource's cloud name.
        """
        return pulumi.get(self, "cloud_name")

    @cloud_name.setter
    def cloud_name(self, value: Optional[pulumi.Input[Union[str, 'CloudName']]]):
        pulumi.set(self, "cloud_name", value)

    @property
    @pulumi.getter(name="hierarchyIdentifier")
    def hierarchy_identifier(self) -> Optional[pulumi.Input[str]]:
        """
        The multi cloud resource identifier (account id in case of AWS connector).
        """
        return pulumi.get(self, "hierarchy_identifier")

    @hierarchy_identifier.setter
    def hierarchy_identifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hierarchy_identifier", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of the resource
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Location where the resource is stored
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def offerings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[Union['CspmMonitorAwsOfferingArgs', 'DefenderForContainersAwsOfferingArgs', 'DefenderForServersAwsOfferingArgs', 'InformationProtectionAwsOfferingArgs']]]]]:
        """
        A collection of offerings for the security connector.
        """
        return pulumi.get(self, "offerings")

    @offerings.setter
    def offerings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[Union['CspmMonitorAwsOfferingArgs', 'DefenderForContainersAwsOfferingArgs', 'DefenderForServersAwsOfferingArgs', 'InformationProtectionAwsOfferingArgs']]]]]):
        pulumi.set(self, "offerings", value)

    @property
    @pulumi.getter(name="organizationalData")
    def organizational_data(self) -> Optional[pulumi.Input['SecurityConnectorPropertiesOrganizationalDataArgs']]:
        """
        The multi cloud account's organizational data
        """
        return pulumi.get(self, "organizational_data")

    @organizational_data.setter
    def organizational_data(self, value: Optional[pulumi.Input['SecurityConnectorPropertiesOrganizationalDataArgs']]):
        pulumi.set(self, "organizational_data", value)

    @property
    @pulumi.getter(name="securityConnectorName")
    def security_connector_name(self) -> Optional[pulumi.Input[str]]:
        """
        The security connector name.
        """
        return pulumi.get(self, "security_connector_name")

    @security_connector_name.setter
    def security_connector_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_connector_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class SecurityConnector(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_name: Optional[pulumi.Input[Union[str, 'CloudName']]] = None,
                 hierarchy_identifier: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 offerings: Optional[pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['CspmMonitorAwsOfferingArgs'], pulumi.InputType['DefenderForContainersAwsOfferingArgs'], pulumi.InputType['DefenderForServersAwsOfferingArgs'], pulumi.InputType['InformationProtectionAwsOfferingArgs']]]]]] = None,
                 organizational_data: Optional[pulumi.Input[pulumi.InputType['SecurityConnectorPropertiesOrganizationalDataArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_connector_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        The security connector resource.
        API Version: 2021-07-01-preview.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'CloudName']] cloud_name: The multi cloud resource's cloud name.
        :param pulumi.Input[str] hierarchy_identifier: The multi cloud resource identifier (account id in case of AWS connector).
        :param pulumi.Input[str] kind: Kind of the resource
        :param pulumi.Input[str] location: Location where the resource is stored
        :param pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['CspmMonitorAwsOfferingArgs'], pulumi.InputType['DefenderForContainersAwsOfferingArgs'], pulumi.InputType['DefenderForServersAwsOfferingArgs'], pulumi.InputType['InformationProtectionAwsOfferingArgs']]]]] offerings: A collection of offerings for the security connector.
        :param pulumi.Input[pulumi.InputType['SecurityConnectorPropertiesOrganizationalDataArgs']] organizational_data: The multi cloud account's organizational data
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[str] security_connector_name: The security connector name.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A list of key value pairs that describe the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SecurityConnectorArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        The security connector resource.
        API Version: 2021-07-01-preview.

        :param str resource_name: The name of the resource.
        :param SecurityConnectorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SecurityConnectorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cloud_name: Optional[pulumi.Input[Union[str, 'CloudName']]] = None,
                 hierarchy_identifier: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 offerings: Optional[pulumi.Input[Sequence[pulumi.Input[Union[pulumi.InputType['CspmMonitorAwsOfferingArgs'], pulumi.InputType['DefenderForContainersAwsOfferingArgs'], pulumi.InputType['DefenderForServersAwsOfferingArgs'], pulumi.InputType['InformationProtectionAwsOfferingArgs']]]]]] = None,
                 organizational_data: Optional[pulumi.Input[pulumi.InputType['SecurityConnectorPropertiesOrganizationalDataArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_connector_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = SecurityConnectorArgs.__new__(SecurityConnectorArgs)

            __props__.__dict__["cloud_name"] = cloud_name
            __props__.__dict__["hierarchy_identifier"] = hierarchy_identifier
            __props__.__dict__["kind"] = kind
            __props__.__dict__["location"] = location
            __props__.__dict__["offerings"] = offerings
            __props__.__dict__["organizational_data"] = organizational_data
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["security_connector_name"] = security_connector_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["etag"] = None
            __props__.__dict__["name"] = None
            __props__.__dict__["system_data"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:security/v20210701preview:SecurityConnector")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SecurityConnector, __self__).__init__(
            'azure-native:security:SecurityConnector',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SecurityConnector':
        """
        Get an existing SecurityConnector resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = SecurityConnectorArgs.__new__(SecurityConnectorArgs)

        __props__.__dict__["cloud_name"] = None
        __props__.__dict__["etag"] = None
        __props__.__dict__["hierarchy_identifier"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["offerings"] = None
        __props__.__dict__["organizational_data"] = None
        __props__.__dict__["system_data"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        return SecurityConnector(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cloudName")
    def cloud_name(self) -> pulumi.Output[Optional[str]]:
        """
        The multi cloud resource's cloud name.
        """
        return pulumi.get(self, "cloud_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        Entity tag is used for comparing two or more entities from the same requested resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hierarchyIdentifier")
    def hierarchy_identifier(self) -> pulumi.Output[Optional[str]]:
        """
        The multi cloud resource identifier (account id in case of AWS connector).
        """
        return pulumi.get(self, "hierarchy_identifier")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of the resource
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Location where the resource is stored
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def offerings(self) -> pulumi.Output[Optional[Sequence[Any]]]:
        """
        A collection of offerings for the security connector.
        """
        return pulumi.get(self, "offerings")

    @property
    @pulumi.getter(name="organizationalData")
    def organizational_data(self) -> pulumi.Output[Optional['outputs.SecurityConnectorPropertiesResponseOrganizationalData']]:
        """
        The multi cloud account's organizational data
        """
        return pulumi.get(self, "organizational_data")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A list of key value pairs that describe the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

