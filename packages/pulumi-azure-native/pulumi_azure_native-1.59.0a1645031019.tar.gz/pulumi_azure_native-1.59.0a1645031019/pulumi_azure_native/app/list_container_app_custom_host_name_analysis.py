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
    'ListContainerAppCustomHostNameAnalysisResult',
    'AwaitableListContainerAppCustomHostNameAnalysisResult',
    'list_container_app_custom_host_name_analysis',
    'list_container_app_custom_host_name_analysis_output',
]

@pulumi.output_type
class ListContainerAppCustomHostNameAnalysisResult:
    """
    Custom domain analysis.
    """
    def __init__(__self__, a_records=None, alternate_c_name_records=None, alternate_txt_records=None, c_name_records=None, conflicting_container_app_resource_id=None, custom_domain_verification_failure_info=None, custom_domain_verification_test=None, has_conflict_on_managed_environment=None, host_name=None, id=None, is_hostname_already_verified=None, name=None, system_data=None, txt_records=None, type=None):
        if a_records and not isinstance(a_records, list):
            raise TypeError("Expected argument 'a_records' to be a list")
        pulumi.set(__self__, "a_records", a_records)
        if alternate_c_name_records and not isinstance(alternate_c_name_records, list):
            raise TypeError("Expected argument 'alternate_c_name_records' to be a list")
        pulumi.set(__self__, "alternate_c_name_records", alternate_c_name_records)
        if alternate_txt_records and not isinstance(alternate_txt_records, list):
            raise TypeError("Expected argument 'alternate_txt_records' to be a list")
        pulumi.set(__self__, "alternate_txt_records", alternate_txt_records)
        if c_name_records and not isinstance(c_name_records, list):
            raise TypeError("Expected argument 'c_name_records' to be a list")
        pulumi.set(__self__, "c_name_records", c_name_records)
        if conflicting_container_app_resource_id and not isinstance(conflicting_container_app_resource_id, str):
            raise TypeError("Expected argument 'conflicting_container_app_resource_id' to be a str")
        pulumi.set(__self__, "conflicting_container_app_resource_id", conflicting_container_app_resource_id)
        if custom_domain_verification_failure_info and not isinstance(custom_domain_verification_failure_info, dict):
            raise TypeError("Expected argument 'custom_domain_verification_failure_info' to be a dict")
        pulumi.set(__self__, "custom_domain_verification_failure_info", custom_domain_verification_failure_info)
        if custom_domain_verification_test and not isinstance(custom_domain_verification_test, str):
            raise TypeError("Expected argument 'custom_domain_verification_test' to be a str")
        pulumi.set(__self__, "custom_domain_verification_test", custom_domain_verification_test)
        if has_conflict_on_managed_environment and not isinstance(has_conflict_on_managed_environment, bool):
            raise TypeError("Expected argument 'has_conflict_on_managed_environment' to be a bool")
        pulumi.set(__self__, "has_conflict_on_managed_environment", has_conflict_on_managed_environment)
        if host_name and not isinstance(host_name, str):
            raise TypeError("Expected argument 'host_name' to be a str")
        pulumi.set(__self__, "host_name", host_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_hostname_already_verified and not isinstance(is_hostname_already_verified, bool):
            raise TypeError("Expected argument 'is_hostname_already_verified' to be a bool")
        pulumi.set(__self__, "is_hostname_already_verified", is_hostname_already_verified)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if txt_records and not isinstance(txt_records, list):
            raise TypeError("Expected argument 'txt_records' to be a list")
        pulumi.set(__self__, "txt_records", txt_records)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="aRecords")
    def a_records(self) -> Optional[Sequence[str]]:
        """
        A records visible for this hostname.
        """
        return pulumi.get(self, "a_records")

    @property
    @pulumi.getter(name="alternateCNameRecords")
    def alternate_c_name_records(self) -> Optional[Sequence[str]]:
        """
        Alternate CName records visible for this hostname.
        """
        return pulumi.get(self, "alternate_c_name_records")

    @property
    @pulumi.getter(name="alternateTxtRecords")
    def alternate_txt_records(self) -> Optional[Sequence[str]]:
        """
        Alternate TXT records visible for this hostname.
        """
        return pulumi.get(self, "alternate_txt_records")

    @property
    @pulumi.getter(name="cNameRecords")
    def c_name_records(self) -> Optional[Sequence[str]]:
        """
        CName records visible for this hostname.
        """
        return pulumi.get(self, "c_name_records")

    @property
    @pulumi.getter(name="conflictingContainerAppResourceId")
    def conflicting_container_app_resource_id(self) -> str:
        """
        Name of the conflicting Container App on the Managed Environment if it's within the same subscription.
        """
        return pulumi.get(self, "conflicting_container_app_resource_id")

    @property
    @pulumi.getter(name="customDomainVerificationFailureInfo")
    def custom_domain_verification_failure_info(self) -> 'outputs.DefaultErrorResponseResponse':
        """
        Raw failure information if DNS verification fails.
        """
        return pulumi.get(self, "custom_domain_verification_failure_info")

    @property
    @pulumi.getter(name="customDomainVerificationTest")
    def custom_domain_verification_test(self) -> str:
        """
        DNS verification test result.
        """
        return pulumi.get(self, "custom_domain_verification_test")

    @property
    @pulumi.getter(name="hasConflictOnManagedEnvironment")
    def has_conflict_on_managed_environment(self) -> bool:
        """
        <code>true</code> if there is a conflict on the Container App's managed environment; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "has_conflict_on_managed_environment")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> str:
        """
        Host name that was analyzed
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isHostnameAlreadyVerified")
    def is_hostname_already_verified(self) -> bool:
        """
        <code>true</code> if hostname is already verified; otherwise, <code>false</code>.
        """
        return pulumi.get(self, "is_hostname_already_verified")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Azure Resource Manager metadata containing createdBy and modifiedBy information.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="txtRecords")
    def txt_records(self) -> Optional[Sequence[str]]:
        """
        TXT records visible for this hostname.
        """
        return pulumi.get(self, "txt_records")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableListContainerAppCustomHostNameAnalysisResult(ListContainerAppCustomHostNameAnalysisResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListContainerAppCustomHostNameAnalysisResult(
            a_records=self.a_records,
            alternate_c_name_records=self.alternate_c_name_records,
            alternate_txt_records=self.alternate_txt_records,
            c_name_records=self.c_name_records,
            conflicting_container_app_resource_id=self.conflicting_container_app_resource_id,
            custom_domain_verification_failure_info=self.custom_domain_verification_failure_info,
            custom_domain_verification_test=self.custom_domain_verification_test,
            has_conflict_on_managed_environment=self.has_conflict_on_managed_environment,
            host_name=self.host_name,
            id=self.id,
            is_hostname_already_verified=self.is_hostname_already_verified,
            name=self.name,
            system_data=self.system_data,
            txt_records=self.txt_records,
            type=self.type)


def list_container_app_custom_host_name_analysis(container_app_name: Optional[str] = None,
                                                 custom_hostname: Optional[str] = None,
                                                 resource_group_name: Optional[str] = None,
                                                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListContainerAppCustomHostNameAnalysisResult:
    """
    Custom domain analysis.
    API Version: 2022-01-01-preview.


    :param str container_app_name: Name of the Container App.
    :param str custom_hostname: Custom hostname.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    __args__ = dict()
    __args__['containerAppName'] = container_app_name
    __args__['customHostname'] = custom_hostname
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:app:listContainerAppCustomHostNameAnalysis', __args__, opts=opts, typ=ListContainerAppCustomHostNameAnalysisResult).value

    return AwaitableListContainerAppCustomHostNameAnalysisResult(
        a_records=__ret__.a_records,
        alternate_c_name_records=__ret__.alternate_c_name_records,
        alternate_txt_records=__ret__.alternate_txt_records,
        c_name_records=__ret__.c_name_records,
        conflicting_container_app_resource_id=__ret__.conflicting_container_app_resource_id,
        custom_domain_verification_failure_info=__ret__.custom_domain_verification_failure_info,
        custom_domain_verification_test=__ret__.custom_domain_verification_test,
        has_conflict_on_managed_environment=__ret__.has_conflict_on_managed_environment,
        host_name=__ret__.host_name,
        id=__ret__.id,
        is_hostname_already_verified=__ret__.is_hostname_already_verified,
        name=__ret__.name,
        system_data=__ret__.system_data,
        txt_records=__ret__.txt_records,
        type=__ret__.type)


@_utilities.lift_output_func(list_container_app_custom_host_name_analysis)
def list_container_app_custom_host_name_analysis_output(container_app_name: Optional[pulumi.Input[str]] = None,
                                                        custom_hostname: Optional[pulumi.Input[Optional[str]]] = None,
                                                        resource_group_name: Optional[pulumi.Input[str]] = None,
                                                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListContainerAppCustomHostNameAnalysisResult]:
    """
    Custom domain analysis.
    API Version: 2022-01-01-preview.


    :param str container_app_name: Name of the Container App.
    :param str custom_hostname: Custom hostname.
    :param str resource_group_name: The name of the resource group. The name is case insensitive.
    """
    ...
