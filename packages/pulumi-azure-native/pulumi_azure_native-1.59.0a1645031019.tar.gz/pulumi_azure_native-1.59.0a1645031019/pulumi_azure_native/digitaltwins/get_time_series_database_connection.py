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
    'GetTimeSeriesDatabaseConnectionResult',
    'AwaitableGetTimeSeriesDatabaseConnectionResult',
    'get_time_series_database_connection',
    'get_time_series_database_connection_output',
]

@pulumi.output_type
class GetTimeSeriesDatabaseConnectionResult:
    """
    Describes a time series database connection resource.
    """
    def __init__(__self__, id=None, name=None, properties=None, system_data=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if properties and not isinstance(properties, dict):
            raise TypeError("Expected argument 'properties' to be a dict")
        pulumi.set(__self__, "properties", properties)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Extension resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> 'outputs.AzureDataExplorerConnectionPropertiesResponse':
        """
        Properties of a specific time series database connection.
        """
        return pulumi.get(self, "properties")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetTimeSeriesDatabaseConnectionResult(GetTimeSeriesDatabaseConnectionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetTimeSeriesDatabaseConnectionResult(
            id=self.id,
            name=self.name,
            properties=self.properties,
            system_data=self.system_data,
            type=self.type)


def get_time_series_database_connection(resource_group_name: Optional[str] = None,
                                        resource_name: Optional[str] = None,
                                        time_series_database_connection_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetTimeSeriesDatabaseConnectionResult:
    """
    Describes a time series database connection resource.
    API Version: 2021-06-30-preview.


    :param str resource_group_name: The name of the resource group that contains the DigitalTwinsInstance.
    :param str resource_name: The name of the DigitalTwinsInstance.
    :param str time_series_database_connection_name: Name of time series database connection.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    __args__['timeSeriesDatabaseConnectionName'] = time_series_database_connection_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:digitaltwins:getTimeSeriesDatabaseConnection', __args__, opts=opts, typ=GetTimeSeriesDatabaseConnectionResult).value

    return AwaitableGetTimeSeriesDatabaseConnectionResult(
        id=__ret__.id,
        name=__ret__.name,
        properties=__ret__.properties,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_time_series_database_connection)
def get_time_series_database_connection_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                               resource_name: Optional[pulumi.Input[str]] = None,
                                               time_series_database_connection_name: Optional[pulumi.Input[str]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetTimeSeriesDatabaseConnectionResult]:
    """
    Describes a time series database connection resource.
    API Version: 2021-06-30-preview.


    :param str resource_group_name: The name of the resource group that contains the DigitalTwinsInstance.
    :param str resource_name: The name of the DigitalTwinsInstance.
    :param str time_series_database_connection_name: Name of time series database connection.
    """
    ...
