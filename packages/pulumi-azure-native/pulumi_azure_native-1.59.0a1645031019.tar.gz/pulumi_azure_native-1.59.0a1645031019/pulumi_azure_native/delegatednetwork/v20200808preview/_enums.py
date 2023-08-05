# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'OrchestratorKind',
    'ResourceIdentityType',
]


class OrchestratorKind(str, Enum):
    """
    The kind of workbook. Choices are user and shared.
    """
    KUBERNETES = "Kubernetes"


class ResourceIdentityType(str, Enum):
    """
    The type of identity used for orchestrator cluster. Type 'SystemAssigned' will use an implicitly created identity orchestrator clusters
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    NONE = "None"
