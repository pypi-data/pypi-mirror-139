# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'ListMonitorMonitoredResourcesResult',
    'AwaitableListMonitorMonitoredResourcesResult',
    'list_monitor_monitored_resources',
    'list_monitor_monitored_resources_output',
]

@pulumi.output_type
class ListMonitorMonitoredResourcesResult:
    """
    Response of a list operation.
    """
    def __init__(__self__, next_link=None, value=None):
        if next_link and not isinstance(next_link, str):
            raise TypeError("Expected argument 'next_link' to be a str")
        pulumi.set(__self__, "next_link", next_link)
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="nextLink")
    def next_link(self) -> Optional[str]:
        """
        Link to the next set of results, if any.
        """
        return pulumi.get(self, "next_link")

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.MonitoredResourceResponse']]:
        """
        Results of a list operation.
        """
        return pulumi.get(self, "value")


class AwaitableListMonitorMonitoredResourcesResult(ListMonitorMonitoredResourcesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListMonitorMonitoredResourcesResult(
            next_link=self.next_link,
            value=self.value)


def list_monitor_monitored_resources(monitor_name: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListMonitorMonitoredResourcesResult:
    """
    Response of a list operation.


    :param str monitor_name: Monitor resource name
    :param str resource_group_name: The name of the resource group to which the Datadog resource belongs.
    """
    __args__ = dict()
    __args__['monitorName'] = monitor_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datadog/v20200201preview:listMonitorMonitoredResources', __args__, opts=opts, typ=ListMonitorMonitoredResourcesResult).value

    return AwaitableListMonitorMonitoredResourcesResult(
        next_link=__ret__.next_link,
        value=__ret__.value)


@_utilities.lift_output_func(list_monitor_monitored_resources)
def list_monitor_monitored_resources_output(monitor_name: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListMonitorMonitoredResourcesResult]:
    """
    Response of a list operation.


    :param str monitor_name: Monitor resource name
    :param str resource_group_name: The name of the resource group to which the Datadog resource belongs.
    """
    ...
