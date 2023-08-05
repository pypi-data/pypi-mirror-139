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
    'GetSecurityPolicyResult',
    'AwaitableGetSecurityPolicyResult',
    'get_security_policy',
    'get_security_policy_output',
]

@pulumi.output_type
class GetSecurityPolicyResult:
    """
    SecurityPolicy association for AzureFrontDoor profile
    """
    def __init__(__self__, deployment_status=None, id=None, name=None, parameters=None, profile_name=None, provisioning_state=None, system_data=None, type=None):
        if deployment_status and not isinstance(deployment_status, str):
            raise TypeError("Expected argument 'deployment_status' to be a str")
        pulumi.set(__self__, "deployment_status", deployment_status)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if parameters and not isinstance(parameters, dict):
            raise TypeError("Expected argument 'parameters' to be a dict")
        pulumi.set(__self__, "parameters", parameters)
        if profile_name and not isinstance(profile_name, str):
            raise TypeError("Expected argument 'profile_name' to be a str")
        pulumi.set(__self__, "profile_name", profile_name)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if system_data and not isinstance(system_data, dict):
            raise TypeError("Expected argument 'system_data' to be a dict")
        pulumi.set(__self__, "system_data", system_data)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> str:
        return pulumi.get(self, "deployment_status")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> Optional['outputs.SecurityPolicyWebApplicationFirewallParametersResponse']:
        """
        object which contains security policy parameters
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="profileName")
    def profile_name(self) -> str:
        """
        The name of the profile which holds the security policy.
        """
        return pulumi.get(self, "profile_name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Provisioning status
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Read only system data
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetSecurityPolicyResult(GetSecurityPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityPolicyResult(
            deployment_status=self.deployment_status,
            id=self.id,
            name=self.name,
            parameters=self.parameters,
            profile_name=self.profile_name,
            provisioning_state=self.provisioning_state,
            system_data=self.system_data,
            type=self.type)


def get_security_policy(profile_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        security_policy_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityPolicyResult:
    """
    SecurityPolicy association for AzureFrontDoor profile


    :param str profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str security_policy_name: Name of the security policy under the profile.
    """
    __args__ = dict()
    __args__['profileName'] = profile_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['securityPolicyName'] = security_policy_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:cdn/v20210601:getSecurityPolicy', __args__, opts=opts, typ=GetSecurityPolicyResult).value

    return AwaitableGetSecurityPolicyResult(
        deployment_status=__ret__.deployment_status,
        id=__ret__.id,
        name=__ret__.name,
        parameters=__ret__.parameters,
        profile_name=__ret__.profile_name,
        provisioning_state=__ret__.provisioning_state,
        system_data=__ret__.system_data,
        type=__ret__.type)


@_utilities.lift_output_func(get_security_policy)
def get_security_policy_output(profile_name: Optional[pulumi.Input[str]] = None,
                               resource_group_name: Optional[pulumi.Input[str]] = None,
                               security_policy_name: Optional[pulumi.Input[str]] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetSecurityPolicyResult]:
    """
    SecurityPolicy association for AzureFrontDoor profile


    :param str profile_name: Name of the Azure Front Door Standard or Azure Front Door Premium profile which is unique within the resource group.
    :param str resource_group_name: Name of the Resource group within the Azure subscription.
    :param str security_policy_name: Name of the security policy under the profile.
    """
    ...
