# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'BackupManagementType',
    'ProtectionStatus',
    'WorkloadItemType',
]


class BackupManagementType(str, Enum):
    """
    Type of backup management for the backed up item.
    """
    INVALID = "Invalid"
    AZURE_IAAS_VM = "AzureIaasVM"
    MAB = "MAB"
    DPM = "DPM"
    AZURE_BACKUP_SERVER = "AzureBackupServer"
    AZURE_SQL = "AzureSql"
    AZURE_STORAGE = "AzureStorage"
    AZURE_WORKLOAD = "AzureWorkload"
    DEFAULT_BACKUP = "DefaultBackup"


class ProtectionStatus(str, Enum):
    """
    Backup state of this backup item.
    """
    INVALID = "Invalid"
    NOT_PROTECTED = "NotProtected"
    PROTECTING = "Protecting"
    PROTECTED = "Protected"
    PROTECTION_FAILED = "ProtectionFailed"


class WorkloadItemType(str, Enum):
    """
    Workload item type of the item for which intent is to be set
    """
    INVALID = "Invalid"
    SQL_INSTANCE = "SQLInstance"
    SQL_DATA_BASE = "SQLDataBase"
    SAP_HANA_SYSTEM = "SAPHanaSystem"
    SAP_HANA_DATABASE = "SAPHanaDatabase"
    SAPASE_SYSTEM = "SAPAseSystem"
    SAPASE_DATABASE = "SAPAseDatabase"
