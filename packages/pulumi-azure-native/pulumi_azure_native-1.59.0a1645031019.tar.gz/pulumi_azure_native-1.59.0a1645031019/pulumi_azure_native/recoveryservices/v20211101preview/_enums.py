# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'InfrastructureEncryptionState',
    'ResourceIdentityType',
    'SkuName',
]


class InfrastructureEncryptionState(str, Enum):
    """
    Enabling/Disabling the Double Encryption state
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ResourceIdentityType(str, Enum):
    """
    The type of managed identity used. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user-assigned identities. The type 'None' will remove any identities.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    NONE = "None"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"


class SkuName(str, Enum):
    """
    The Sku name.
    """
    STANDARD = "Standard"
    RS0 = "RS0"
