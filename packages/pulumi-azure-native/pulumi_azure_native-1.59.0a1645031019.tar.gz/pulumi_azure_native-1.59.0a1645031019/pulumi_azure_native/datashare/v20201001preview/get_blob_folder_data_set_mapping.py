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
    'GetBlobFolderDataSetMappingResult',
    'AwaitableGetBlobFolderDataSetMappingResult',
    'get_blob_folder_data_set_mapping',
    'get_blob_folder_data_set_mapping_output',
]

@pulumi.output_type
class GetBlobFolderDataSetMappingResult:
    """
    A Blob folder data set mapping.
    """
    def __init__(__self__, container_name=None, data_set_id=None, data_set_mapping_status=None, id=None, kind=None, name=None, prefix=None, provisioning_state=None, resource_group=None, storage_account_name=None, subscription_id=None, system_data=None, type=None):
        if container_name and not isinstance(container_name, str):
            raise TypeError("Expected argument 'container_name' to be a str")
        pulumi.set(__self__, "container_name", container_name)
        if data_set_id and not isinstance(data_set_id, str):
            raise TypeError("Expected argument 'data_set_id' to be a str")
        pulumi.set(__self__, "data_set_id", data_set_id)
        if data_set_mapping_status and not isinstance(data_set_mapping_status, str):
            raise TypeError("Expected argument 'data_set_mapping_status' to be a str")
        pulumi.set(__self__, "data_set_mapping_status", data_set_mapping_status)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if prefix and not isinstance(prefix, str):
            raise TypeError("Expected argument 'prefix' to be a str")
        pulumi.set(__self__, "prefix", prefix)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if resource_group and not isinstance(resource_group, str):
            raise TypeError("Expected argument 'resource_group' to be a str")
        pulumi.set(__self__, "resource_group", resource_group)
        if storage_account_name and not isinstance(storage_account_name, str):
            raise TypeError("Expected argument 'storage_account_name' to be a str")
        pulumi.set(__self__, "storage_account_name", storage_account_name)
        if subscription_id and not isinstance(subscription_id, str):
            raise TypeError("Expected argument 'subscription_id' to be a str")
        pulumi.set(__self__, "subscription_id", subscription_id)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="containerName")
    def container_name(self) -> str:
        """
        Container that has the file path.
        """
        return pulumi.get(self, "container_name")

    @property
    @pulumi.getter(name="dataSetId")
    def data_set_id(self) -> str:
        """
        The id of the source data set.
        """
        return pulumi.get(self, "data_set_id")

    @property
    @pulumi.getter(name="dataSetMappingStatus")
    def data_set_mapping_status(self) -> str:
        """
        Gets the status of the data set mapping.
        """
        return pulumi.get(self, "data_set_mapping_status")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource id of the azure resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> str:
        """
        Kind of data set mapping.
        Expected value is 'BlobFolder'.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the azure resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def prefix(self) -> str:
        """
        Prefix for blob folder
        """
        return pulumi.get(self, "prefix")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning state of the data set mapping.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGroup")
    def resource_group(self) -> str:
        """
        Resource group of storage account.
        """
        return pulumi.get(self, "resource_group")

    @property
    @pulumi.getter(name="storageAccountName")
    def storage_account_name(self) -> str:
        """
        Storage account name of the source data set.
        """
        return pulumi.get(self, "storage_account_name")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> str:
        """
        Subscription id of storage account.
        """
        return pulumi.get(self, "subscription_id")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        System Data of the Azure resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of the azure resource
        """
        return pulumi.get(self, "type")


class AwaitableGetBlobFolderDataSetMappingResult(GetBlobFolderDataSetMappingResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBlobFolderDataSetMappingResult(
            container_name=self.container_name,
            data_set_id=self.data_set_id,
            data_set_mapping_status=self.data_set_mapping_status,
            id=self.id,
            kind=self.kind,
            name=self.name,
            prefix=self.prefix,
            provisioning_state=self.provisioning_state,
            resource_group=self.resource_group,
            storage_account_name=self.storage_account_name,
            subscription_id=self.subscription_id,
            system_data=self.system_data,
            type=self.type)


def get_blob_folder_data_set_mapping(account_name: Optional[str] = None,
                                     data_set_mapping_name: Optional[str] = None,
                                     resource_group_name: Optional[str] = None,
                                     share_subscription_name: Optional[str] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBlobFolderDataSetMappingResult:
    """
    A Blob folder data set mapping.


    :param str account_name: The name of the share account.
    :param str data_set_mapping_name: The name of the dataSetMapping.
    :param str resource_group_name: The resource group name.
    :param str share_subscription_name: The name of the shareSubscription.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['dataSetMappingName'] = data_set_mapping_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['shareSubscriptionName'] = share_subscription_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:datashare/v20201001preview:getBlobFolderDataSetMapping', __args__, opts=opts, typ=GetBlobFolderDataSetMappingResult).value

    return AwaitableGetBlobFolderDataSetMappingResult(
        container_name=__ret__.container_name,
        data_set_id=__ret__.data_set_id,
        data_set_mapping_status=__ret__.data_set_mapping_status,
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        prefix=__ret__.prefix,
        provisioning_state=__ret__.provisioning_state,
        resource_group=__ret__.resource_group,
        storage_account_name=__ret__.storage_account_name,
        subscription_id=__ret__.subscription_id,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_blob_folder_data_set_mapping)
def get_blob_folder_data_set_mapping_output(account_name: Optional[pulumi.Input[str]] = None,
                                            data_set_mapping_name: Optional[pulumi.Input[str]] = None,
                                            resource_group_name: Optional[pulumi.Input[str]] = None,
                                            share_subscription_name: Optional[pulumi.Input[str]] = None,
                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetBlobFolderDataSetMappingResult]:
    """
    A Blob folder data set mapping.


    :param str account_name: The name of the share account.
    :param str data_set_mapping_name: The name of the dataSetMapping.
    :param str resource_group_name: The resource group name.
    :param str share_subscription_name: The name of the shareSubscription.
    """
    ...
