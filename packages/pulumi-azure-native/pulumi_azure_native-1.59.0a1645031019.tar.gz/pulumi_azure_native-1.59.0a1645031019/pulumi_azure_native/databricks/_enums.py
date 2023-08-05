# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'KeySource',
    'PrivateLinkServiceConnectionStatus',
]


class KeySource(str, Enum):
    """
    The encryption keySource (provider). Possible values (case-insensitive):  Default, Microsoft.Keyvault
    """
    DEFAULT = "Default"
    MICROSOFT_KEYVAULT = "Microsoft.Keyvault"


class PrivateLinkServiceConnectionStatus(str, Enum):
    """
    The status of a private endpoint connection
    """
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    DISCONNECTED = "Disconnected"
