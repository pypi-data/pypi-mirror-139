# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from ._enums import *

__all__ = [
    'ConfigDiagnosticsValidatorResultIssueArgs',
    'ConfigDiagnosticsValidatorResultArgs',
    'ConfigDiagnosticsArgs',
    'DomainSecuritySettingsArgs',
    'ForestTrustArgs',
    'LdapsSettingsArgs',
    'NotificationSettingsArgs',
    'ReplicaSetArgs',
    'ResourceForestSettingsArgs',
]

@pulumi.input_type
class ConfigDiagnosticsValidatorResultIssueArgs:
    def __init__(__self__, *,
                 description_params: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 id: Optional[pulumi.Input[str]] = None):
        """
        Specific issue for a particular config diagnostics validator
        :param pulumi.Input[Sequence[pulumi.Input[str]]] description_params: List of domain resource property name or values used to compose a rich description.
        :param pulumi.Input[str] id: Validation issue identifier.
        """
        if description_params is not None:
            pulumi.set(__self__, "description_params", description_params)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="descriptionParams")
    def description_params(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        List of domain resource property name or values used to compose a rich description.
        """
        return pulumi.get(self, "description_params")

    @description_params.setter
    def description_params(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "description_params", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Validation issue identifier.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class ConfigDiagnosticsValidatorResultArgs:
    def __init__(__self__, *,
                 issues: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultIssueArgs']]]] = None,
                 replica_set_subnet_display_name: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[Union[str, 'Status']]] = None,
                 validator_id: Optional[pulumi.Input[str]] = None):
        """
        Config Diagnostics validator result data
        :param pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultIssueArgs']]] issues: List of resource config validation issues.
        :param pulumi.Input[str] replica_set_subnet_display_name: Replica set location and subnet name
        :param pulumi.Input[Union[str, 'Status']] status: Status for individual validator after running diagnostics.
        :param pulumi.Input[str] validator_id: Validator identifier
        """
        if issues is not None:
            pulumi.set(__self__, "issues", issues)
        if replica_set_subnet_display_name is not None:
            pulumi.set(__self__, "replica_set_subnet_display_name", replica_set_subnet_display_name)
        if status is None:
            status = 'None'
        if status is not None:
            pulumi.set(__self__, "status", status)
        if validator_id is not None:
            pulumi.set(__self__, "validator_id", validator_id)

    @property
    @pulumi.getter
    def issues(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultIssueArgs']]]]:
        """
        List of resource config validation issues.
        """
        return pulumi.get(self, "issues")

    @issues.setter
    def issues(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultIssueArgs']]]]):
        pulumi.set(self, "issues", value)

    @property
    @pulumi.getter(name="replicaSetSubnetDisplayName")
    def replica_set_subnet_display_name(self) -> Optional[pulumi.Input[str]]:
        """
        Replica set location and subnet name
        """
        return pulumi.get(self, "replica_set_subnet_display_name")

    @replica_set_subnet_display_name.setter
    def replica_set_subnet_display_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "replica_set_subnet_display_name", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[Union[str, 'Status']]]:
        """
        Status for individual validator after running diagnostics.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[Union[str, 'Status']]]):
        pulumi.set(self, "status", value)

    @property
    @pulumi.getter(name="validatorId")
    def validator_id(self) -> Optional[pulumi.Input[str]]:
        """
        Validator identifier
        """
        return pulumi.get(self, "validator_id")

    @validator_id.setter
    def validator_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "validator_id", value)


@pulumi.input_type
class ConfigDiagnosticsArgs:
    def __init__(__self__, *,
                 last_executed: Optional[pulumi.Input[str]] = None,
                 validator_results: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultArgs']]]] = None):
        """
        Configuration Diagnostics
        :param pulumi.Input[str] last_executed: Last domain configuration diagnostics DateTime
        :param pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultArgs']]] validator_results: List of Configuration Diagnostics validator results.
        """
        if last_executed is not None:
            pulumi.set(__self__, "last_executed", last_executed)
        if validator_results is not None:
            pulumi.set(__self__, "validator_results", validator_results)

    @property
    @pulumi.getter(name="lastExecuted")
    def last_executed(self) -> Optional[pulumi.Input[str]]:
        """
        Last domain configuration diagnostics DateTime
        """
        return pulumi.get(self, "last_executed")

    @last_executed.setter
    def last_executed(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "last_executed", value)

    @property
    @pulumi.getter(name="validatorResults")
    def validator_results(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultArgs']]]]:
        """
        List of Configuration Diagnostics validator results.
        """
        return pulumi.get(self, "validator_results")

    @validator_results.setter
    def validator_results(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigDiagnosticsValidatorResultArgs']]]]):
        pulumi.set(self, "validator_results", value)


@pulumi.input_type
class DomainSecuritySettingsArgs:
    def __init__(__self__, *,
                 kerberos_armoring: Optional[pulumi.Input[Union[str, 'KerberosArmoring']]] = None,
                 kerberos_rc4_encryption: Optional[pulumi.Input[Union[str, 'KerberosRc4Encryption']]] = None,
                 ntlm_v1: Optional[pulumi.Input[Union[str, 'NtlmV1']]] = None,
                 sync_kerberos_passwords: Optional[pulumi.Input[Union[str, 'SyncKerberosPasswords']]] = None,
                 sync_ntlm_passwords: Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]] = None,
                 sync_on_prem_passwords: Optional[pulumi.Input[Union[str, 'SyncOnPremPasswords']]] = None,
                 tls_v1: Optional[pulumi.Input[Union[str, 'TlsV1']]] = None):
        """
        Domain Security Settings
        :param pulumi.Input[Union[str, 'KerberosArmoring']] kerberos_armoring: A flag to determine whether or not KerberosArmoring is enabled or disabled.
        :param pulumi.Input[Union[str, 'KerberosRc4Encryption']] kerberos_rc4_encryption: A flag to determine whether or not KerberosRc4Encryption is enabled or disabled.
        :param pulumi.Input[Union[str, 'NtlmV1']] ntlm_v1: A flag to determine whether or not NtlmV1 is enabled or disabled.
        :param pulumi.Input[Union[str, 'SyncKerberosPasswords']] sync_kerberos_passwords: A flag to determine whether or not SyncKerberosPasswords is enabled or disabled.
        :param pulumi.Input[Union[str, 'SyncNtlmPasswords']] sync_ntlm_passwords: A flag to determine whether or not SyncNtlmPasswords is enabled or disabled.
        :param pulumi.Input[Union[str, 'SyncOnPremPasswords']] sync_on_prem_passwords: A flag to determine whether or not SyncOnPremPasswords is enabled or disabled.
        :param pulumi.Input[Union[str, 'TlsV1']] tls_v1: A flag to determine whether or not TlsV1 is enabled or disabled.
        """
        if kerberos_armoring is None:
            kerberos_armoring = 'Disabled'
        if kerberos_armoring is not None:
            pulumi.set(__self__, "kerberos_armoring", kerberos_armoring)
        if kerberos_rc4_encryption is None:
            kerberos_rc4_encryption = 'Enabled'
        if kerberos_rc4_encryption is not None:
            pulumi.set(__self__, "kerberos_rc4_encryption", kerberos_rc4_encryption)
        if ntlm_v1 is None:
            ntlm_v1 = 'Enabled'
        if ntlm_v1 is not None:
            pulumi.set(__self__, "ntlm_v1", ntlm_v1)
        if sync_kerberos_passwords is None:
            sync_kerberos_passwords = 'Enabled'
        if sync_kerberos_passwords is not None:
            pulumi.set(__self__, "sync_kerberos_passwords", sync_kerberos_passwords)
        if sync_ntlm_passwords is None:
            sync_ntlm_passwords = 'Enabled'
        if sync_ntlm_passwords is not None:
            pulumi.set(__self__, "sync_ntlm_passwords", sync_ntlm_passwords)
        if sync_on_prem_passwords is None:
            sync_on_prem_passwords = 'Enabled'
        if sync_on_prem_passwords is not None:
            pulumi.set(__self__, "sync_on_prem_passwords", sync_on_prem_passwords)
        if tls_v1 is None:
            tls_v1 = 'Enabled'
        if tls_v1 is not None:
            pulumi.set(__self__, "tls_v1", tls_v1)

    @property
    @pulumi.getter(name="kerberosArmoring")
    def kerberos_armoring(self) -> Optional[pulumi.Input[Union[str, 'KerberosArmoring']]]:
        """
        A flag to determine whether or not KerberosArmoring is enabled or disabled.
        """
        return pulumi.get(self, "kerberos_armoring")

    @kerberos_armoring.setter
    def kerberos_armoring(self, value: Optional[pulumi.Input[Union[str, 'KerberosArmoring']]]):
        pulumi.set(self, "kerberos_armoring", value)

    @property
    @pulumi.getter(name="kerberosRc4Encryption")
    def kerberos_rc4_encryption(self) -> Optional[pulumi.Input[Union[str, 'KerberosRc4Encryption']]]:
        """
        A flag to determine whether or not KerberosRc4Encryption is enabled or disabled.
        """
        return pulumi.get(self, "kerberos_rc4_encryption")

    @kerberos_rc4_encryption.setter
    def kerberos_rc4_encryption(self, value: Optional[pulumi.Input[Union[str, 'KerberosRc4Encryption']]]):
        pulumi.set(self, "kerberos_rc4_encryption", value)

    @property
    @pulumi.getter(name="ntlmV1")
    def ntlm_v1(self) -> Optional[pulumi.Input[Union[str, 'NtlmV1']]]:
        """
        A flag to determine whether or not NtlmV1 is enabled or disabled.
        """
        return pulumi.get(self, "ntlm_v1")

    @ntlm_v1.setter
    def ntlm_v1(self, value: Optional[pulumi.Input[Union[str, 'NtlmV1']]]):
        pulumi.set(self, "ntlm_v1", value)

    @property
    @pulumi.getter(name="syncKerberosPasswords")
    def sync_kerberos_passwords(self) -> Optional[pulumi.Input[Union[str, 'SyncKerberosPasswords']]]:
        """
        A flag to determine whether or not SyncKerberosPasswords is enabled or disabled.
        """
        return pulumi.get(self, "sync_kerberos_passwords")

    @sync_kerberos_passwords.setter
    def sync_kerberos_passwords(self, value: Optional[pulumi.Input[Union[str, 'SyncKerberosPasswords']]]):
        pulumi.set(self, "sync_kerberos_passwords", value)

    @property
    @pulumi.getter(name="syncNtlmPasswords")
    def sync_ntlm_passwords(self) -> Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]]:
        """
        A flag to determine whether or not SyncNtlmPasswords is enabled or disabled.
        """
        return pulumi.get(self, "sync_ntlm_passwords")

    @sync_ntlm_passwords.setter
    def sync_ntlm_passwords(self, value: Optional[pulumi.Input[Union[str, 'SyncNtlmPasswords']]]):
        pulumi.set(self, "sync_ntlm_passwords", value)

    @property
    @pulumi.getter(name="syncOnPremPasswords")
    def sync_on_prem_passwords(self) -> Optional[pulumi.Input[Union[str, 'SyncOnPremPasswords']]]:
        """
        A flag to determine whether or not SyncOnPremPasswords is enabled or disabled.
        """
        return pulumi.get(self, "sync_on_prem_passwords")

    @sync_on_prem_passwords.setter
    def sync_on_prem_passwords(self, value: Optional[pulumi.Input[Union[str, 'SyncOnPremPasswords']]]):
        pulumi.set(self, "sync_on_prem_passwords", value)

    @property
    @pulumi.getter(name="tlsV1")
    def tls_v1(self) -> Optional[pulumi.Input[Union[str, 'TlsV1']]]:
        """
        A flag to determine whether or not TlsV1 is enabled or disabled.
        """
        return pulumi.get(self, "tls_v1")

    @tls_v1.setter
    def tls_v1(self, value: Optional[pulumi.Input[Union[str, 'TlsV1']]]):
        pulumi.set(self, "tls_v1", value)


@pulumi.input_type
class ForestTrustArgs:
    def __init__(__self__, *,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 remote_dns_ips: Optional[pulumi.Input[str]] = None,
                 trust_direction: Optional[pulumi.Input[str]] = None,
                 trust_password: Optional[pulumi.Input[str]] = None,
                 trusted_domain_fqdn: Optional[pulumi.Input[str]] = None):
        """
        Forest Trust Setting
        :param pulumi.Input[str] friendly_name: Friendly Name
        :param pulumi.Input[str] remote_dns_ips: Remote Dns ips
        :param pulumi.Input[str] trust_direction: Trust Direction
        :param pulumi.Input[str] trust_password: Trust Password
        :param pulumi.Input[str] trusted_domain_fqdn: Trusted Domain FQDN
        """
        if friendly_name is not None:
            pulumi.set(__self__, "friendly_name", friendly_name)
        if remote_dns_ips is not None:
            pulumi.set(__self__, "remote_dns_ips", remote_dns_ips)
        if trust_direction is not None:
            pulumi.set(__self__, "trust_direction", trust_direction)
        if trust_password is not None:
            pulumi.set(__self__, "trust_password", trust_password)
        if trusted_domain_fqdn is not None:
            pulumi.set(__self__, "trusted_domain_fqdn", trusted_domain_fqdn)

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> Optional[pulumi.Input[str]]:
        """
        Friendly Name
        """
        return pulumi.get(self, "friendly_name")

    @friendly_name.setter
    def friendly_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "friendly_name", value)

    @property
    @pulumi.getter(name="remoteDnsIps")
    def remote_dns_ips(self) -> Optional[pulumi.Input[str]]:
        """
        Remote Dns ips
        """
        return pulumi.get(self, "remote_dns_ips")

    @remote_dns_ips.setter
    def remote_dns_ips(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "remote_dns_ips", value)

    @property
    @pulumi.getter(name="trustDirection")
    def trust_direction(self) -> Optional[pulumi.Input[str]]:
        """
        Trust Direction
        """
        return pulumi.get(self, "trust_direction")

    @trust_direction.setter
    def trust_direction(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_direction", value)

    @property
    @pulumi.getter(name="trustPassword")
    def trust_password(self) -> Optional[pulumi.Input[str]]:
        """
        Trust Password
        """
        return pulumi.get(self, "trust_password")

    @trust_password.setter
    def trust_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trust_password", value)

    @property
    @pulumi.getter(name="trustedDomainFqdn")
    def trusted_domain_fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        Trusted Domain FQDN
        """
        return pulumi.get(self, "trusted_domain_fqdn")

    @trusted_domain_fqdn.setter
    def trusted_domain_fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trusted_domain_fqdn", value)


@pulumi.input_type
class LdapsSettingsArgs:
    def __init__(__self__, *,
                 external_access: Optional[pulumi.Input[Union[str, 'ExternalAccess']]] = None,
                 ldaps: Optional[pulumi.Input[Union[str, 'Ldaps']]] = None,
                 pfx_certificate: Optional[pulumi.Input[str]] = None,
                 pfx_certificate_password: Optional[pulumi.Input[str]] = None):
        """
        Secure LDAP Settings
        :param pulumi.Input[Union[str, 'ExternalAccess']] external_access: A flag to determine whether or not Secure LDAP access over the internet is enabled or disabled.
        :param pulumi.Input[Union[str, 'Ldaps']] ldaps: A flag to determine whether or not Secure LDAP is enabled or disabled.
        :param pulumi.Input[str] pfx_certificate: The certificate required to configure Secure LDAP. The parameter passed here should be a base64encoded representation of the certificate pfx file.
        :param pulumi.Input[str] pfx_certificate_password: The password to decrypt the provided Secure LDAP certificate pfx file.
        """
        if external_access is None:
            external_access = 'Disabled'
        if external_access is not None:
            pulumi.set(__self__, "external_access", external_access)
        if ldaps is None:
            ldaps = 'Disabled'
        if ldaps is not None:
            pulumi.set(__self__, "ldaps", ldaps)
        if pfx_certificate is not None:
            pulumi.set(__self__, "pfx_certificate", pfx_certificate)
        if pfx_certificate_password is not None:
            pulumi.set(__self__, "pfx_certificate_password", pfx_certificate_password)

    @property
    @pulumi.getter(name="externalAccess")
    def external_access(self) -> Optional[pulumi.Input[Union[str, 'ExternalAccess']]]:
        """
        A flag to determine whether or not Secure LDAP access over the internet is enabled or disabled.
        """
        return pulumi.get(self, "external_access")

    @external_access.setter
    def external_access(self, value: Optional[pulumi.Input[Union[str, 'ExternalAccess']]]):
        pulumi.set(self, "external_access", value)

    @property
    @pulumi.getter
    def ldaps(self) -> Optional[pulumi.Input[Union[str, 'Ldaps']]]:
        """
        A flag to determine whether or not Secure LDAP is enabled or disabled.
        """
        return pulumi.get(self, "ldaps")

    @ldaps.setter
    def ldaps(self, value: Optional[pulumi.Input[Union[str, 'Ldaps']]]):
        pulumi.set(self, "ldaps", value)

    @property
    @pulumi.getter(name="pfxCertificate")
    def pfx_certificate(self) -> Optional[pulumi.Input[str]]:
        """
        The certificate required to configure Secure LDAP. The parameter passed here should be a base64encoded representation of the certificate pfx file.
        """
        return pulumi.get(self, "pfx_certificate")

    @pfx_certificate.setter
    def pfx_certificate(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_certificate", value)

    @property
    @pulumi.getter(name="pfxCertificatePassword")
    def pfx_certificate_password(self) -> Optional[pulumi.Input[str]]:
        """
        The password to decrypt the provided Secure LDAP certificate pfx file.
        """
        return pulumi.get(self, "pfx_certificate_password")

    @pfx_certificate_password.setter
    def pfx_certificate_password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "pfx_certificate_password", value)


@pulumi.input_type
class NotificationSettingsArgs:
    def __init__(__self__, *,
                 additional_recipients: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 notify_dc_admins: Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]] = None,
                 notify_global_admins: Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]] = None):
        """
        Settings for notification
        :param pulumi.Input[Sequence[pulumi.Input[str]]] additional_recipients: The list of additional recipients
        :param pulumi.Input[Union[str, 'NotifyDcAdmins']] notify_dc_admins: Should domain controller admins be notified
        :param pulumi.Input[Union[str, 'NotifyGlobalAdmins']] notify_global_admins: Should global admins be notified
        """
        if additional_recipients is not None:
            pulumi.set(__self__, "additional_recipients", additional_recipients)
        if notify_dc_admins is not None:
            pulumi.set(__self__, "notify_dc_admins", notify_dc_admins)
        if notify_global_admins is not None:
            pulumi.set(__self__, "notify_global_admins", notify_global_admins)

    @property
    @pulumi.getter(name="additionalRecipients")
    def additional_recipients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The list of additional recipients
        """
        return pulumi.get(self, "additional_recipients")

    @additional_recipients.setter
    def additional_recipients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "additional_recipients", value)

    @property
    @pulumi.getter(name="notifyDcAdmins")
    def notify_dc_admins(self) -> Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]]:
        """
        Should domain controller admins be notified
        """
        return pulumi.get(self, "notify_dc_admins")

    @notify_dc_admins.setter
    def notify_dc_admins(self, value: Optional[pulumi.Input[Union[str, 'NotifyDcAdmins']]]):
        pulumi.set(self, "notify_dc_admins", value)

    @property
    @pulumi.getter(name="notifyGlobalAdmins")
    def notify_global_admins(self) -> Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]]:
        """
        Should global admins be notified
        """
        return pulumi.get(self, "notify_global_admins")

    @notify_global_admins.setter
    def notify_global_admins(self, value: Optional[pulumi.Input[Union[str, 'NotifyGlobalAdmins']]]):
        pulumi.set(self, "notify_global_admins", value)


@pulumi.input_type
class ReplicaSetArgs:
    def __init__(__self__, *,
                 location: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None):
        """
        Replica Set Definition
        :param pulumi.Input[str] location: Virtual network location
        :param pulumi.Input[str] subnet_id: The name of the virtual network that Domain Services will be deployed on. The id of the subnet that Domain Services will be deployed on. /virtualNetwork/vnetName/subnets/subnetName.
        """
        if location is not None:
            pulumi.set(__self__, "location", location)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Virtual network location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the virtual network that Domain Services will be deployed on. The id of the subnet that Domain Services will be deployed on. /virtualNetwork/vnetName/subnets/subnetName.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)


@pulumi.input_type
class ResourceForestSettingsArgs:
    def __init__(__self__, *,
                 resource_forest: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[Sequence[pulumi.Input['ForestTrustArgs']]]] = None):
        """
        Settings for Resource Forest
        :param pulumi.Input[str] resource_forest: Resource Forest
        :param pulumi.Input[Sequence[pulumi.Input['ForestTrustArgs']]] settings: List of settings for Resource Forest
        """
        if resource_forest is not None:
            pulumi.set(__self__, "resource_forest", resource_forest)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)

    @property
    @pulumi.getter(name="resourceForest")
    def resource_forest(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Forest
        """
        return pulumi.get(self, "resource_forest")

    @resource_forest.setter
    def resource_forest(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_forest", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ForestTrustArgs']]]]:
        """
        List of settings for Resource Forest
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ForestTrustArgs']]]]):
        pulumi.set(self, "settings", value)


