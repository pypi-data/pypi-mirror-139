# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetguestDiagnosticsSettingResult',
    'AwaitableGetguestDiagnosticsSettingResult',
    'getguest_diagnostics_setting',
    'getguest_diagnostics_setting_output',
]

@pulumi.output_type
class GetguestDiagnosticsSettingResult:
    """
    Virtual machine guest diagnostics settings resource.
    """
    def __init__(__self__, data_sources=None, id=None, location=None, name=None, os_type=None, proxy_setting=None, tags=None, type=None):
        if data_sources and not isinstance(data_sources, list):
            raise TypeError("Expected argument 'data_sources' to be a list")
        pulumi.set(__self__, "data_sources", data_sources)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if os_type and not isinstance(os_type, str):
            raise TypeError("Expected argument 'os_type' to be a str")
        pulumi.set(__self__, "os_type", os_type)
        if proxy_setting and not isinstance(proxy_setting, str):
            raise TypeError("Expected argument 'proxy_setting' to be a str")
        pulumi.set(__self__, "proxy_setting", proxy_setting)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="dataSources")
    def data_sources(self) -> Optional[Sequence['outputs.DataSourceResponse']]:
        """
        the array of data source object which are configured to collect and send data
        """
        return pulumi.get(self, "data_sources")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Azure resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[str]:
        """
        Operating system type for the configuration
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="proxySetting")
    def proxy_setting(self) -> Optional[str]:
        return pulumi.get(self, "proxy_setting")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Azure resource type
        """
        return pulumi.get(self, "type")


class AwaitableGetguestDiagnosticsSettingResult(GetguestDiagnosticsSettingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetguestDiagnosticsSettingResult(
            data_sources=self.data_sources,
            id=self.id,
            location=self.location,
            name=self.name,
            os_type=self.os_type,
            proxy_setting=self.proxy_setting,
            tags=self.tags,
            type=self.type)


def getguest_diagnostics_setting(diagnostic_settings_name: Optional[str] = None,
                                 resource_group_name: Optional[str] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetguestDiagnosticsSettingResult:
    """
    Virtual machine guest diagnostics settings resource.
    API Version: 2018-06-01-preview.


    :param str diagnostic_settings_name: The name of the diagnostic setting.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['diagnosticSettingsName'] = diagnostic_settings_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:insights:getguestDiagnosticsSetting', __args__, opts=opts, typ=GetguestDiagnosticsSettingResult).value

    return AwaitableGetguestDiagnosticsSettingResult(
        data_sources=__ret__.data_sources,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        os_type=__ret__.os_type,
        proxy_setting=__ret__.proxy_setting,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(getguest_diagnostics_setting)
def getguest_diagnostics_setting_output(diagnostic_settings_name: Optional[pulumi.Input[str]] = None,
                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetguestDiagnosticsSettingResult]:
    """
    Virtual machine guest diagnostics settings resource.
    API Version: 2018-06-01-preview.


    :param str diagnostic_settings_name: The name of the diagnostic setting.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
