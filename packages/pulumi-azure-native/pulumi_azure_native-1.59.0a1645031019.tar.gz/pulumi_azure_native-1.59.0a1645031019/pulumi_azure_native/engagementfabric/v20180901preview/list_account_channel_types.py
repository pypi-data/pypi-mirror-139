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
    'ListAccountChannelTypesResult',
    'AwaitableListAccountChannelTypesResult',
    'list_account_channel_types',
    'list_account_channel_types_output',
]

@pulumi.output_type
class ListAccountChannelTypesResult:
    """
    List of the EngagementFabric channel descriptions
    """
    def __init__(__self__, value=None):
        if value and not isinstance(value, list):
            raise TypeError("Expected argument 'value' to be a list")
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[Sequence['outputs.ChannelTypeDescriptionResponse']]:
        """
        Channel descriptions
        """
        return pulumi.get(self, "value")


class AwaitableListAccountChannelTypesResult(ListAccountChannelTypesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListAccountChannelTypesResult(
            value=self.value)


def list_account_channel_types(account_name: Optional[str] = None,
                               resource_group_name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListAccountChannelTypesResult:
    """
    List of the EngagementFabric channel descriptions


    :param str account_name: Account Name
    :param str resource_group_name: Resource Group Name
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:engagementfabric/v20180901preview:listAccountChannelTypes', __args__, opts=opts, typ=ListAccountChannelTypesResult).value

    return AwaitableListAccountChannelTypesResult(
        value=__ret__.value)


@_utilities.lift_output_func(list_account_channel_types)
def list_account_channel_types_output(account_name: Optional[pulumi.Input[str]] = None,
                                      resource_group_name: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListAccountChannelTypesResult]:
    """
    List of the EngagementFabric channel descriptions


    :param str account_name: Account Name
    :param str resource_group_name: Resource Group Name
    """
    ...
