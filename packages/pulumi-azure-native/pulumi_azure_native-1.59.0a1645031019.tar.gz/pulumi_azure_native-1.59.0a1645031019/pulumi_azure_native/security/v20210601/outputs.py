# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._enums import *

__all__ = [
    'AssessmentLinksResponse',
    'AssessmentStatusResponseResponse',
    'AzureResourceDetailsResponse',
    'OnPremiseResourceDetailsResponse',
    'OnPremiseSqlResourceDetailsResponse',
    'SecurityAssessmentMetadataPartnerDataResponse',
    'SecurityAssessmentMetadataPropertiesResponse',
    'SecurityAssessmentMetadataPropertiesResponseResponsePublishDates',
    'SecurityAssessmentPartnerDataResponse',
]

@pulumi.output_type
class AssessmentLinksResponse(dict):
    """
    Links relevant to the assessment
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "azurePortalUri":
            suggest = "azure_portal_uri"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssessmentLinksResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssessmentLinksResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssessmentLinksResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 azure_portal_uri: str):
        """
        Links relevant to the assessment
        :param str azure_portal_uri: Link to assessment in Azure Portal
        """
        pulumi.set(__self__, "azure_portal_uri", azure_portal_uri)

    @property
    @pulumi.getter(name="azurePortalUri")
    def azure_portal_uri(self) -> str:
        """
        Link to assessment in Azure Portal
        """
        return pulumi.get(self, "azure_portal_uri")


@pulumi.output_type
class AssessmentStatusResponseResponse(dict):
    """
    The result of the assessment
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "firstEvaluationDate":
            suggest = "first_evaluation_date"
        elif key == "statusChangeDate":
            suggest = "status_change_date"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssessmentStatusResponseResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssessmentStatusResponseResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssessmentStatusResponseResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 code: str,
                 first_evaluation_date: str,
                 status_change_date: str,
                 cause: Optional[str] = None,
                 description: Optional[str] = None):
        """
        The result of the assessment
        :param str code: Programmatic code for the status of the assessment
        :param str first_evaluation_date: The time that the assessment was created and first evaluated. Returned as UTC time in ISO 8601 format
        :param str status_change_date: The time that the status of the assessment last changed. Returned as UTC time in ISO 8601 format
        :param str cause: Programmatic code for the cause of the assessment status
        :param str description: Human readable description of the assessment status
        """
        pulumi.set(__self__, "code", code)
        pulumi.set(__self__, "first_evaluation_date", first_evaluation_date)
        pulumi.set(__self__, "status_change_date", status_change_date)
        if cause is not None:
            pulumi.set(__self__, "cause", cause)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def code(self) -> str:
        """
        Programmatic code for the status of the assessment
        """
        return pulumi.get(self, "code")

    @property
    @pulumi.getter(name="firstEvaluationDate")
    def first_evaluation_date(self) -> str:
        """
        The time that the assessment was created and first evaluated. Returned as UTC time in ISO 8601 format
        """
        return pulumi.get(self, "first_evaluation_date")

    @property
    @pulumi.getter(name="statusChangeDate")
    def status_change_date(self) -> str:
        """
        The time that the status of the assessment last changed. Returned as UTC time in ISO 8601 format
        """
        return pulumi.get(self, "status_change_date")

    @property
    @pulumi.getter
    def cause(self) -> Optional[str]:
        """
        Programmatic code for the cause of the assessment status
        """
        return pulumi.get(self, "cause")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Human readable description of the assessment status
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class AzureResourceDetailsResponse(dict):
    """
    Details of the Azure resource that was assessed
    """
    def __init__(__self__, *,
                 id: str,
                 source: str):
        """
        Details of the Azure resource that was assessed
        :param str id: Azure resource Id of the assessed resource
        :param str source: The platform where the assessed resource resides
               Expected value is 'Azure'.
        """
        pulumi.set(__self__, "id", id)
        pulumi.set(__self__, "source", 'Azure')

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Azure resource Id of the assessed resource
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        The platform where the assessed resource resides
        Expected value is 'Azure'.
        """
        return pulumi.get(self, "source")


@pulumi.output_type
class OnPremiseResourceDetailsResponse(dict):
    """
    Details of the On Premise resource that was assessed
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "machineName":
            suggest = "machine_name"
        elif key == "sourceComputerId":
            suggest = "source_computer_id"
        elif key == "workspaceId":
            suggest = "workspace_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OnPremiseResourceDetailsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OnPremiseResourceDetailsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OnPremiseResourceDetailsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 machine_name: str,
                 source: str,
                 source_computer_id: str,
                 vmuuid: str,
                 workspace_id: str):
        """
        Details of the On Premise resource that was assessed
        :param str machine_name: The name of the machine
        :param str source: The platform where the assessed resource resides
               Expected value is 'OnPremise'.
        :param str source_computer_id: The oms agent Id installed on the machine
        :param str vmuuid: The unique Id of the machine
        :param str workspace_id: Azure resource Id of the workspace the machine is attached to
        """
        pulumi.set(__self__, "machine_name", machine_name)
        pulumi.set(__self__, "source", 'OnPremise')
        pulumi.set(__self__, "source_computer_id", source_computer_id)
        pulumi.set(__self__, "vmuuid", vmuuid)
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="machineName")
    def machine_name(self) -> str:
        """
        The name of the machine
        """
        return pulumi.get(self, "machine_name")

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        The platform where the assessed resource resides
        Expected value is 'OnPremise'.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="sourceComputerId")
    def source_computer_id(self) -> str:
        """
        The oms agent Id installed on the machine
        """
        return pulumi.get(self, "source_computer_id")

    @property
    @pulumi.getter
    def vmuuid(self) -> str:
        """
        The unique Id of the machine
        """
        return pulumi.get(self, "vmuuid")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        Azure resource Id of the workspace the machine is attached to
        """
        return pulumi.get(self, "workspace_id")


@pulumi.output_type
class OnPremiseSqlResourceDetailsResponse(dict):
    """
    Details of the On Premise Sql resource that was assessed
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "databaseName":
            suggest = "database_name"
        elif key == "machineName":
            suggest = "machine_name"
        elif key == "serverName":
            suggest = "server_name"
        elif key == "sourceComputerId":
            suggest = "source_computer_id"
        elif key == "workspaceId":
            suggest = "workspace_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OnPremiseSqlResourceDetailsResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OnPremiseSqlResourceDetailsResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OnPremiseSqlResourceDetailsResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 database_name: str,
                 machine_name: str,
                 server_name: str,
                 source: str,
                 source_computer_id: str,
                 vmuuid: str,
                 workspace_id: str):
        """
        Details of the On Premise Sql resource that was assessed
        :param str database_name: The Sql database name installed on the machine
        :param str machine_name: The name of the machine
        :param str server_name: The Sql server name installed on the machine
        :param str source: The platform where the assessed resource resides
               Expected value is 'OnPremiseSql'.
        :param str source_computer_id: The oms agent Id installed on the machine
        :param str vmuuid: The unique Id of the machine
        :param str workspace_id: Azure resource Id of the workspace the machine is attached to
        """
        pulumi.set(__self__, "database_name", database_name)
        pulumi.set(__self__, "machine_name", machine_name)
        pulumi.set(__self__, "server_name", server_name)
        pulumi.set(__self__, "source", 'OnPremiseSql')
        pulumi.set(__self__, "source_computer_id", source_computer_id)
        pulumi.set(__self__, "vmuuid", vmuuid)
        pulumi.set(__self__, "workspace_id", workspace_id)

    @property
    @pulumi.getter(name="databaseName")
    def database_name(self) -> str:
        """
        The Sql database name installed on the machine
        """
        return pulumi.get(self, "database_name")

    @property
    @pulumi.getter(name="machineName")
    def machine_name(self) -> str:
        """
        The name of the machine
        """
        return pulumi.get(self, "machine_name")

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> str:
        """
        The Sql server name installed on the machine
        """
        return pulumi.get(self, "server_name")

    @property
    @pulumi.getter
    def source(self) -> str:
        """
        The platform where the assessed resource resides
        Expected value is 'OnPremiseSql'.
        """
        return pulumi.get(self, "source")

    @property
    @pulumi.getter(name="sourceComputerId")
    def source_computer_id(self) -> str:
        """
        The oms agent Id installed on the machine
        """
        return pulumi.get(self, "source_computer_id")

    @property
    @pulumi.getter
    def vmuuid(self) -> str:
        """
        The unique Id of the machine
        """
        return pulumi.get(self, "vmuuid")

    @property
    @pulumi.getter(name="workspaceId")
    def workspace_id(self) -> str:
        """
        Azure resource Id of the workspace the machine is attached to
        """
        return pulumi.get(self, "workspace_id")


@pulumi.output_type
class SecurityAssessmentMetadataPartnerDataResponse(dict):
    """
    Describes the partner that created the assessment
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "partnerName":
            suggest = "partner_name"
        elif key == "productName":
            suggest = "product_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityAssessmentMetadataPartnerDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityAssessmentMetadataPartnerDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityAssessmentMetadataPartnerDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 partner_name: str,
                 secret: str,
                 product_name: Optional[str] = None):
        """
        Describes the partner that created the assessment
        :param str partner_name: Name of the company of the partner
        :param str secret: Secret to authenticate the partner and verify it created the assessment - write only
        :param str product_name: Name of the product of the partner that created the assessment
        """
        pulumi.set(__self__, "partner_name", partner_name)
        pulumi.set(__self__, "secret", secret)
        if product_name is not None:
            pulumi.set(__self__, "product_name", product_name)

    @property
    @pulumi.getter(name="partnerName")
    def partner_name(self) -> str:
        """
        Name of the company of the partner
        """
        return pulumi.get(self, "partner_name")

    @property
    @pulumi.getter
    def secret(self) -> str:
        """
        Secret to authenticate the partner and verify it created the assessment - write only
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter(name="productName")
    def product_name(self) -> Optional[str]:
        """
        Name of the product of the partner that created the assessment
        """
        return pulumi.get(self, "product_name")


@pulumi.output_type
class SecurityAssessmentMetadataPropertiesResponse(dict):
    """
    Describes properties of an assessment metadata.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "assessmentType":
            suggest = "assessment_type"
        elif key == "displayName":
            suggest = "display_name"
        elif key == "policyDefinitionId":
            suggest = "policy_definition_id"
        elif key == "implementationEffort":
            suggest = "implementation_effort"
        elif key == "partnerData":
            suggest = "partner_data"
        elif key == "remediationDescription":
            suggest = "remediation_description"
        elif key == "userImpact":
            suggest = "user_impact"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityAssessmentMetadataPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityAssessmentMetadataPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityAssessmentMetadataPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 assessment_type: str,
                 display_name: str,
                 policy_definition_id: str,
                 severity: str,
                 categories: Optional[Sequence[str]] = None,
                 description: Optional[str] = None,
                 implementation_effort: Optional[str] = None,
                 partner_data: Optional['outputs.SecurityAssessmentMetadataPartnerDataResponse'] = None,
                 preview: Optional[bool] = None,
                 remediation_description: Optional[str] = None,
                 threats: Optional[Sequence[str]] = None,
                 user_impact: Optional[str] = None):
        """
        Describes properties of an assessment metadata.
        :param str assessment_type: BuiltIn if the assessment based on built-in Azure Policy definition, Custom if the assessment based on custom Azure Policy definition
        :param str display_name: User friendly display name of the assessment
        :param str policy_definition_id: Azure resource ID of the policy definition that turns this assessment calculation on
        :param str severity: The severity level of the assessment
        :param str description: Human readable description of the assessment
        :param str implementation_effort: The implementation effort required to remediate this assessment
        :param 'SecurityAssessmentMetadataPartnerDataResponse' partner_data: Describes the partner that created the assessment
        :param bool preview: True if this assessment is in preview release status
        :param str remediation_description: Human readable description of what you should do to mitigate this security issue
        :param str user_impact: The user impact of the assessment
        """
        pulumi.set(__self__, "assessment_type", assessment_type)
        pulumi.set(__self__, "display_name", display_name)
        pulumi.set(__self__, "policy_definition_id", policy_definition_id)
        pulumi.set(__self__, "severity", severity)
        if categories is not None:
            pulumi.set(__self__, "categories", categories)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if implementation_effort is not None:
            pulumi.set(__self__, "implementation_effort", implementation_effort)
        if partner_data is not None:
            pulumi.set(__self__, "partner_data", partner_data)
        if preview is not None:
            pulumi.set(__self__, "preview", preview)
        if remediation_description is not None:
            pulumi.set(__self__, "remediation_description", remediation_description)
        if threats is not None:
            pulumi.set(__self__, "threats", threats)
        if user_impact is not None:
            pulumi.set(__self__, "user_impact", user_impact)

    @property
    @pulumi.getter(name="assessmentType")
    def assessment_type(self) -> str:
        """
        BuiltIn if the assessment based on built-in Azure Policy definition, Custom if the assessment based on custom Azure Policy definition
        """
        return pulumi.get(self, "assessment_type")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> str:
        """
        User friendly display name of the assessment
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="policyDefinitionId")
    def policy_definition_id(self) -> str:
        """
        Azure resource ID of the policy definition that turns this assessment calculation on
        """
        return pulumi.get(self, "policy_definition_id")

    @property
    @pulumi.getter
    def severity(self) -> str:
        """
        The severity level of the assessment
        """
        return pulumi.get(self, "severity")

    @property
    @pulumi.getter
    def categories(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "categories")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Human readable description of the assessment
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="implementationEffort")
    def implementation_effort(self) -> Optional[str]:
        """
        The implementation effort required to remediate this assessment
        """
        return pulumi.get(self, "implementation_effort")

    @property
    @pulumi.getter(name="partnerData")
    def partner_data(self) -> Optional['outputs.SecurityAssessmentMetadataPartnerDataResponse']:
        """
        Describes the partner that created the assessment
        """
        return pulumi.get(self, "partner_data")

    @property
    @pulumi.getter
    def preview(self) -> Optional[bool]:
        """
        True if this assessment is in preview release status
        """
        return pulumi.get(self, "preview")

    @property
    @pulumi.getter(name="remediationDescription")
    def remediation_description(self) -> Optional[str]:
        """
        Human readable description of what you should do to mitigate this security issue
        """
        return pulumi.get(self, "remediation_description")

    @property
    @pulumi.getter
    def threats(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "threats")

    @property
    @pulumi.getter(name="userImpact")
    def user_impact(self) -> Optional[str]:
        """
        The user impact of the assessment
        """
        return pulumi.get(self, "user_impact")


@pulumi.output_type
class SecurityAssessmentMetadataPropertiesResponseResponsePublishDates(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "gA":
            suggest = "g_a"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityAssessmentMetadataPropertiesResponseResponsePublishDates. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityAssessmentMetadataPropertiesResponseResponsePublishDates.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityAssessmentMetadataPropertiesResponseResponsePublishDates.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 public: str,
                 g_a: Optional[str] = None):
        pulumi.set(__self__, "public", public)
        if g_a is not None:
            pulumi.set(__self__, "g_a", g_a)

    @property
    @pulumi.getter
    def public(self) -> str:
        return pulumi.get(self, "public")

    @property
    @pulumi.getter(name="gA")
    def g_a(self) -> Optional[str]:
        return pulumi.get(self, "g_a")


@pulumi.output_type
class SecurityAssessmentPartnerDataResponse(dict):
    """
    Data regarding 3rd party partner integration
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "partnerName":
            suggest = "partner_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecurityAssessmentPartnerDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecurityAssessmentPartnerDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecurityAssessmentPartnerDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 partner_name: str,
                 secret: str):
        """
        Data regarding 3rd party partner integration
        :param str partner_name: Name of the company of the partner
        :param str secret: secret to authenticate the partner - write only
        """
        pulumi.set(__self__, "partner_name", partner_name)
        pulumi.set(__self__, "secret", secret)

    @property
    @pulumi.getter(name="partnerName")
    def partner_name(self) -> str:
        """
        Name of the company of the partner
        """
        return pulumi.get(self, "partner_name")

    @property
    @pulumi.getter
    def secret(self) -> str:
        """
        secret to authenticate the partner - write only
        """
        return pulumi.get(self, "secret")


