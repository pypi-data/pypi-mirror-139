# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetWorkloadNetworkVMGroupResult',
    'AwaitableGetWorkloadNetworkVMGroupResult',
    'get_workload_network_vm_group',
    'get_workload_network_vm_group_output',
]

@pulumi.output_type
class GetWorkloadNetworkVMGroupResult:
    """
    NSX VM Group
    """
    def __init__(__self__, display_name=None, id=None, members=None, name=None, provisioning_state=None, revision=None, status=None, type=None):
        if display_name and not isinstance(display_name, str):
            raise TypeError("Expected argument 'display_name' to be a str")
        pulumi.set(__self__, "display_name", display_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if members and not isinstance(members, list):
            raise TypeError("Expected argument 'members' to be a list")
        pulumi.set(__self__, "members", members)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if revision and not isinstance(revision, float):
            raise TypeError("Expected argument 'revision' to be a float")
        pulumi.set(__self__, "revision", revision)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        Display name of the VM group.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def members(self) -> Optional[Sequence[str]]:
        """
        Virtual machine members of this group.
        """
        return pulumi.get(self, "members")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def revision(self) -> Optional[float]:
        """
        NSX revision number.
        """
        return pulumi.get(self, "revision")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        VM Group status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetWorkloadNetworkVMGroupResult(GetWorkloadNetworkVMGroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkloadNetworkVMGroupResult(
            display_name=self.display_name,
            id=self.id,
            members=self.members,
            name=self.name,
            provisioning_state=self.provisioning_state,
            revision=self.revision,
            status=self.status,
            type=self.type)


def get_workload_network_vm_group(private_cloud_name: Optional[str] = None,
                                  resource_group_name: Optional[str] = None,
                                  vm_group_id: Optional[str] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkloadNetworkVMGroupResult:
    """
    NSX VM Group
    API Version: 2020-07-17-preview.


    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str vm_group_id: NSX VM Group identifier. Generally the same as the VM Group's display name
    """
    __args__ = dict()
    __args__['privateCloudName'] = private_cloud_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['vmGroupId'] = vm_group_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:avs:getWorkloadNetworkVMGroup', __args__, opts=opts, typ=GetWorkloadNetworkVMGroupResult).value

    return AwaitableGetWorkloadNetworkVMGroupResult(
        display_name=__ret__.display_name,
        id=__ret__.id,
        members=__ret__.members,
        name=__ret__.name,
        provisioning_state=__ret__.provisioning_state,
        revision=__ret__.revision,
        status=__ret__.status,
        type=__ret__.type)


@_utilities.lift_output_func(get_workload_network_vm_group)
def get_workload_network_vm_group_output(private_cloud_name: Optional[pulumi.Input[str]] = None,
                                         resource_group_name: Optional[pulumi.Input[str]] = None,
                                         vm_group_id: Optional[pulumi.Input[str]] = None,
                                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkloadNetworkVMGroupResult]:
    """
    NSX VM Group
    API Version: 2020-07-17-preview.


    :param str private_cloud_name: Name of the private cloud
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str vm_group_id: NSX VM Group identifier. Generally the same as the VM Group's display name
    """
    ...
