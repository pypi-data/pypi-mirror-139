# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'ComputeType',
    'ResourceIdentityType',
]


class ComputeType(str, Enum):
    """
    The type of compute
    """
    AKS = "AKS"
    BATCH_AI = "BatchAI"
    DATA_FACTORY = "DataFactory"
    VIRTUAL_MACHINE = "VirtualMachine"
    HD_INSIGHT = "HDInsight"


class ResourceIdentityType(str, Enum):
    """
    The identity type.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
