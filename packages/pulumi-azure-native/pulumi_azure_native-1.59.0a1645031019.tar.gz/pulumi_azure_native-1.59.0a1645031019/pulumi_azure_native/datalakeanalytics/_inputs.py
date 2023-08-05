# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'AddDataLakeStoreWithAccountParametersArgs',
    'AddStorageAccountWithAccountParametersArgs',
    'CreateComputePolicyWithAccountParametersArgs',
    'CreateFirewallRuleWithAccountParametersArgs',
]

@pulumi.input_type
class AddDataLakeStoreWithAccountParametersArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 suffix: Optional[pulumi.Input[str]] = None):
        """
        The parameters used to add a new Data Lake Store account while creating a new Data Lake Analytics account.
        :param pulumi.Input[str] name: The unique name of the Data Lake Store account to add.
        :param pulumi.Input[str] suffix: The optional suffix for the Data Lake Store account.
        """
        pulumi.set(__self__, "name", name)
        if suffix is not None:
            pulumi.set(__self__, "suffix", suffix)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the Data Lake Store account to add.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def suffix(self) -> Optional[pulumi.Input[str]]:
        """
        The optional suffix for the Data Lake Store account.
        """
        return pulumi.get(self, "suffix")

    @suffix.setter
    def suffix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "suffix", value)


@pulumi.input_type
class AddStorageAccountWithAccountParametersArgs:
    def __init__(__self__, *,
                 access_key: pulumi.Input[str],
                 name: pulumi.Input[str],
                 suffix: Optional[pulumi.Input[str]] = None):
        """
        The parameters used to add a new Azure Storage account while creating a new Data Lake Analytics account.
        :param pulumi.Input[str] access_key: The access key associated with this Azure Storage account that will be used to connect to it.
        :param pulumi.Input[str] name: The unique name of the Azure Storage account to add.
        :param pulumi.Input[str] suffix: The optional suffix for the storage account.
        """
        pulumi.set(__self__, "access_key", access_key)
        pulumi.set(__self__, "name", name)
        if suffix is None:
            suffix = 'azuredatalakestore.net'
        if suffix is not None:
            pulumi.set(__self__, "suffix", suffix)

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> pulumi.Input[str]:
        """
        The access key associated with this Azure Storage account that will be used to connect to it.
        """
        return pulumi.get(self, "access_key")

    @access_key.setter
    def access_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_key", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the Azure Storage account to add.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def suffix(self) -> Optional[pulumi.Input[str]]:
        """
        The optional suffix for the storage account.
        """
        return pulumi.get(self, "suffix")

    @suffix.setter
    def suffix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "suffix", value)


@pulumi.input_type
class CreateComputePolicyWithAccountParametersArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 object_id: pulumi.Input[str],
                 object_type: pulumi.Input[Union[str, 'AADObjectType']],
                 max_degree_of_parallelism_per_job: Optional[pulumi.Input[int]] = None,
                 min_priority_per_job: Optional[pulumi.Input[int]] = None):
        """
        The parameters used to create a new compute policy while creating a new Data Lake Analytics account.
        :param pulumi.Input[str] name: The unique name of the compute policy to create.
        :param pulumi.Input[str] object_id: The AAD object identifier for the entity to create a policy for.
        :param pulumi.Input[Union[str, 'AADObjectType']] object_type: The type of AAD object the object identifier refers to.
        :param pulumi.Input[int] max_degree_of_parallelism_per_job: The maximum degree of parallelism per job this user can use to submit jobs. This property, the min priority per job property, or both must be passed.
        :param pulumi.Input[int] min_priority_per_job: The minimum priority per job this user can use to submit jobs. This property, the max degree of parallelism per job property, or both must be passed.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "object_id", object_id)
        pulumi.set(__self__, "object_type", object_type)
        if max_degree_of_parallelism_per_job is not None:
            pulumi.set(__self__, "max_degree_of_parallelism_per_job", max_degree_of_parallelism_per_job)
        if min_priority_per_job is not None:
            pulumi.set(__self__, "min_priority_per_job", min_priority_per_job)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the compute policy to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> pulumi.Input[str]:
        """
        The AAD object identifier for the entity to create a policy for.
        """
        return pulumi.get(self, "object_id")

    @object_id.setter
    def object_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "object_id", value)

    @property
    @pulumi.getter(name="objectType")
    def object_type(self) -> pulumi.Input[Union[str, 'AADObjectType']]:
        """
        The type of AAD object the object identifier refers to.
        """
        return pulumi.get(self, "object_type")

    @object_type.setter
    def object_type(self, value: pulumi.Input[Union[str, 'AADObjectType']]):
        pulumi.set(self, "object_type", value)

    @property
    @pulumi.getter(name="maxDegreeOfParallelismPerJob")
    def max_degree_of_parallelism_per_job(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum degree of parallelism per job this user can use to submit jobs. This property, the min priority per job property, or both must be passed.
        """
        return pulumi.get(self, "max_degree_of_parallelism_per_job")

    @max_degree_of_parallelism_per_job.setter
    def max_degree_of_parallelism_per_job(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_degree_of_parallelism_per_job", value)

    @property
    @pulumi.getter(name="minPriorityPerJob")
    def min_priority_per_job(self) -> Optional[pulumi.Input[int]]:
        """
        The minimum priority per job this user can use to submit jobs. This property, the max degree of parallelism per job property, or both must be passed.
        """
        return pulumi.get(self, "min_priority_per_job")

    @min_priority_per_job.setter
    def min_priority_per_job(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_priority_per_job", value)


@pulumi.input_type
class CreateFirewallRuleWithAccountParametersArgs:
    def __init__(__self__, *,
                 end_ip_address: pulumi.Input[str],
                 name: pulumi.Input[str],
                 start_ip_address: pulumi.Input[str]):
        """
        The parameters used to create a new firewall rule while creating a new Data Lake Analytics account.
        :param pulumi.Input[str] end_ip_address: The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        :param pulumi.Input[str] name: The unique name of the firewall rule to create.
        :param pulumi.Input[str] start_ip_address: The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        pulumi.set(__self__, "end_ip_address", end_ip_address)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "start_ip_address", start_ip_address)

    @property
    @pulumi.getter(name="endIpAddress")
    def end_ip_address(self) -> pulumi.Input[str]:
        """
        The end IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        return pulumi.get(self, "end_ip_address")

    @end_ip_address.setter
    def end_ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "end_ip_address", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the firewall rule to create.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="startIpAddress")
    def start_ip_address(self) -> pulumi.Input[str]:
        """
        The start IP address for the firewall rule. This can be either ipv4 or ipv6. Start and End should be in the same protocol.
        """
        return pulumi.get(self, "start_ip_address")

    @start_ip_address.setter
    def start_ip_address(self, value: pulumi.Input[str]):
        pulumi.set(self, "start_ip_address", value)


