# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'GetLoggerResult',
    'AwaitableGetLoggerResult',
    'get_logger',
    'get_logger_output',
]

@pulumi.output_type
class GetLoggerResult:
    """
    Logger details.
    """
    def __init__(__self__, credentials=None, description=None, id=None, is_buffered=None, logger_type=None, name=None, resource_id=None, type=None):
        if credentials and not isinstance(credentials, dict):
            raise TypeError("Expected argument 'credentials' to be a dict")
        pulumi.set(__self__, "credentials", credentials)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_buffered and not isinstance(is_buffered, bool):
            raise TypeError("Expected argument 'is_buffered' to be a bool")
        pulumi.set(__self__, "is_buffered", is_buffered)
        if logger_type and not isinstance(logger_type, str):
            raise TypeError("Expected argument 'logger_type' to be a str")
        pulumi.set(__self__, "logger_type", logger_type)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def credentials(self) -> Optional[Mapping[str, str]]:
        """
        The name and SendRule connection string of the event hub for azureEventHub logger.
        Instrumentation key for applicationInsights logger.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Logger description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isBuffered")
    def is_buffered(self) -> Optional[bool]:
        """
        Whether records are buffered in the logger before publishing. Default is assumed to be true.
        """
        return pulumi.get(self, "is_buffered")

    @property
    @pulumi.getter(name="loggerType")
    def logger_type(self) -> str:
        """
        Logger type.
        """
        return pulumi.get(self, "logger_type")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        Azure Resource Id of a log target (either Azure Event Hub resource or Azure Application Insights resource).
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetLoggerResult(GetLoggerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoggerResult(
            credentials=self.credentials,
            description=self.description,
            id=self.id,
            is_buffered=self.is_buffered,
            logger_type=self.logger_type,
            name=self.name,
            resource_id=self.resource_id,
            type=self.type)


def get_logger(logger_id: Optional[str] = None,
               resource_group_name: Optional[str] = None,
               service_name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoggerResult:
    """
    Logger details.


    :param str logger_id: Logger identifier. Must be unique in the API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    __args__ = dict()
    __args__['loggerId'] = logger_id
    __args__['resourceGroupName'] = resource_group_name
    __args__['serviceName'] = service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:apimanagement/v20210801:getLogger', __args__, opts=opts, typ=GetLoggerResult).value

    return AwaitableGetLoggerResult(
        credentials=__ret__.credentials,
        description=__ret__.description,
        id=__ret__.id,
        is_buffered=__ret__.is_buffered,
        logger_type=__ret__.logger_type,
        name=__ret__.name,
        resource_id=__ret__.resource_id,
        type=__ret__.type)


@_utilities.lift_output_func(get_logger)
def get_logger_output(logger_id: Optional[pulumi.Input[str]] = None,
                      resource_group_name: Optional[pulumi.Input[str]] = None,
                      service_name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLoggerResult]:
    """
    Logger details.


    :param str logger_id: Logger identifier. Must be unique in the API Management service instance.
    :param str resource_group_name: The name of the resource group.
    :param str service_name: The name of the API Management service.
    """
    ...
