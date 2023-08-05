# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'ListOpenShiftClusterCredentialsResult',
    'AwaitableListOpenShiftClusterCredentialsResult',
    'list_open_shift_cluster_credentials',
    'list_open_shift_cluster_credentials_output',
]

@pulumi.output_type
class ListOpenShiftClusterCredentialsResult:
    """
    OpenShiftClusterCredentials represents an OpenShift cluster's credentials
    """
    def __init__(__self__, kubeadmin_password=None, kubeadmin_username=None):
        if kubeadmin_password and not isinstance(kubeadmin_password, str):
            raise TypeError("Expected argument 'kubeadmin_password' to be a str")
        pulumi.set(__self__, "kubeadmin_password", kubeadmin_password)
        if kubeadmin_username and not isinstance(kubeadmin_username, str):
            raise TypeError("Expected argument 'kubeadmin_username' to be a str")
        pulumi.set(__self__, "kubeadmin_username", kubeadmin_username)

    @property
    @pulumi.getter(name="kubeadminPassword")
    def kubeadmin_password(self) -> Optional[str]:
        """
        The password for the kubeadmin user
        """
        return pulumi.get(self, "kubeadmin_password")

    @property
    @pulumi.getter(name="kubeadminUsername")
    def kubeadmin_username(self) -> Optional[str]:
        """
        The username for the kubeadmin user
        """
        return pulumi.get(self, "kubeadmin_username")


class AwaitableListOpenShiftClusterCredentialsResult(ListOpenShiftClusterCredentialsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListOpenShiftClusterCredentialsResult(
            kubeadmin_password=self.kubeadmin_password,
            kubeadmin_username=self.kubeadmin_username)


def list_open_shift_cluster_credentials(resource_group_name: Optional[str] = None,
                                        resource_name: Optional[str] = None,
                                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListOpenShiftClusterCredentialsResult:
    """
    OpenShiftClusterCredentials represents an OpenShift cluster's credentials
    API Version: 2020-04-30.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the OpenShift cluster resource.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['resourceName'] = resource_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:redhatopenshift:listOpenShiftClusterCredentials', __args__, opts=opts, typ=ListOpenShiftClusterCredentialsResult).value

    return AwaitableListOpenShiftClusterCredentialsResult(
        kubeadmin_password=__ret__.kubeadmin_password,
        kubeadmin_username=__ret__.kubeadmin_username)


@_utilities.lift_output_func(list_open_shift_cluster_credentials)
def list_open_shift_cluster_credentials_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                                               resource_name: Optional[pulumi.Input[str]] = None,
                                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListOpenShiftClusterCredentialsResult]:
    """
    OpenShiftClusterCredentials represents an OpenShift cluster's credentials
    API Version: 2020-04-30.


    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    :param str resource_name: The name of the OpenShift cluster resource.
    """
    ...
