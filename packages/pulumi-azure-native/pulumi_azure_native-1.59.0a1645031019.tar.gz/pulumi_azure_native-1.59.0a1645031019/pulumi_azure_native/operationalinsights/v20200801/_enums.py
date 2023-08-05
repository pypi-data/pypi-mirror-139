# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ClusterSkuNameEnum',
    'DataSourceKind',
    'IdentityType',
    'LinkedServiceEntityStatus',
    'PublicNetworkAccessType',
    'WorkspaceEntityStatus',
    'WorkspaceSkuNameEnum',
]


class ClusterSkuNameEnum(str, Enum):
    """
    The name of the SKU.
    """
    CAPACITY_RESERVATION = "CapacityReservation"


class DataSourceKind(str, Enum):
    """
    The kind of the DataSource.
    """
    WINDOWS_EVENT = "WindowsEvent"
    WINDOWS_PERFORMANCE_COUNTER = "WindowsPerformanceCounter"
    IIS_LOGS = "IISLogs"
    LINUX_SYSLOG = "LinuxSyslog"
    LINUX_SYSLOG_COLLECTION = "LinuxSyslogCollection"
    LINUX_PERFORMANCE_OBJECT = "LinuxPerformanceObject"
    LINUX_PERFORMANCE_COLLECTION = "LinuxPerformanceCollection"
    CUSTOM_LOG = "CustomLog"
    CUSTOM_LOG_COLLECTION = "CustomLogCollection"
    AZURE_AUDIT_LOG = "AzureAuditLog"
    AZURE_ACTIVITY_LOG = "AzureActivityLog"
    GENERIC_DATA_SOURCE = "GenericDataSource"
    CHANGE_TRACKING_CUSTOM_PATH = "ChangeTrackingCustomPath"
    CHANGE_TRACKING_PATH = "ChangeTrackingPath"
    CHANGE_TRACKING_SERVICES = "ChangeTrackingServices"
    CHANGE_TRACKING_DATA_TYPE_CONFIGURATION = "ChangeTrackingDataTypeConfiguration"
    CHANGE_TRACKING_DEFAULT_REGISTRY = "ChangeTrackingDefaultRegistry"
    CHANGE_TRACKING_REGISTRY = "ChangeTrackingRegistry"
    CHANGE_TRACKING_LINUX_PATH = "ChangeTrackingLinuxPath"
    LINUX_CHANGE_TRACKING_PATH = "LinuxChangeTrackingPath"
    CHANGE_TRACKING_CONTENT_LOCATION = "ChangeTrackingContentLocation"
    WINDOWS_TELEMETRY = "WindowsTelemetry"
    OFFICE365 = "Office365"
    SECURITY_WINDOWS_BASELINE_CONFIGURATION = "SecurityWindowsBaselineConfiguration"
    SECURITY_CENTER_SECURITY_WINDOWS_BASELINE_CONFIGURATION = "SecurityCenterSecurityWindowsBaselineConfiguration"
    SECURITY_EVENT_COLLECTION_CONFIGURATION = "SecurityEventCollectionConfiguration"
    SECURITY_INSIGHTS_SECURITY_EVENT_COLLECTION_CONFIGURATION = "SecurityInsightsSecurityEventCollectionConfiguration"
    IMPORT_COMPUTER_GROUP = "ImportComputerGroup"
    NETWORK_MONITORING = "NetworkMonitoring"
    ITSM = "Itsm"
    DNS_ANALYTICS = "DnsAnalytics"
    APPLICATION_INSIGHTS = "ApplicationInsights"
    SQL_DATA_CLASSIFICATION = "SqlDataClassification"


class IdentityType(str, Enum):
    """
    The identity type.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    NONE = "None"


class LinkedServiceEntityStatus(str, Enum):
    """
    The provisioning state of the linked service.
    """
    SUCCEEDED = "Succeeded"
    DELETING = "Deleting"
    PROVISIONING_ACCOUNT = "ProvisioningAccount"
    UPDATING = "Updating"


class PublicNetworkAccessType(str, Enum):
    """
    The network access type for accessing Log Analytics query.
    """
    ENABLED = "Enabled"
    """
    Enables connectivity to Log Analytics through public DNS.
    """
    DISABLED = "Disabled"
    """
    Disables public connectivity to Log Analytics through public DNS.
    """


class WorkspaceEntityStatus(str, Enum):
    """
    The provisioning state of the workspace.
    """
    CREATING = "Creating"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    CANCELED = "Canceled"
    DELETING = "Deleting"
    PROVISIONING_ACCOUNT = "ProvisioningAccount"
    UPDATING = "Updating"


class WorkspaceSkuNameEnum(str, Enum):
    """
    The name of the SKU.
    """
    FREE = "Free"
    STANDARD = "Standard"
    PREMIUM = "Premium"
    PER_NODE = "PerNode"
    PER_GB2018 = "PerGB2018"
    STANDALONE = "Standalone"
    CAPACITY_RESERVATION = "CapacityReservation"
    LA_CLUSTER = "LACluster"
