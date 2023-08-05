# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'PublicNetworkAccess',
    'Status',
    'Type',
]


class PublicNetworkAccess(str, Enum):
    """
    Gets or sets the public network access.
    """
    NOT_SPECIFIED = "NotSpecified"
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class Status(str, Enum):
    """
    The status.
    """
    UNKNOWN = "Unknown"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"


class Type(str, Enum):
    """
    Identity Type
    """
    NONE = "None"
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
