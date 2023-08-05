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
    'FilteringTagResponse',
    'IdentityPropertiesResponse',
    'LogRulesResponse',
    'LogzOrganizationPropertiesResponse',
    'MetricRulesResponse',
    'MetricsTagRulesPropertiesResponse',
    'MonitorPropertiesResponse',
    'MonitoredResourceResponse',
    'MonitoringTagRulesPropertiesResponse',
    'PlanDataResponse',
    'SystemDataResponse',
    'UserInfoResponse',
    'UserRoleResponseResponse',
    'VMResourcesResponse',
]

@pulumi.output_type
class FilteringTagResponse(dict):
    """
    The definition of a filtering tag. Filtering tags are used for capturing resources and include/exclude them from being monitored.
    """
    def __init__(__self__, *,
                 action: Optional[str] = None,
                 name: Optional[str] = None,
                 value: Optional[str] = None):
        """
        The definition of a filtering tag. Filtering tags are used for capturing resources and include/exclude them from being monitored.
        :param str action: Valid actions for a filtering tag. Exclusion takes priority over inclusion.
        :param str name: The name (also known as the key) of the tag.
        :param str value: The value of the tag.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def action(self) -> Optional[str]:
        """
        Valid actions for a filtering tag. Exclusion takes priority over inclusion.
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name (also known as the key) of the tag.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> Optional[str]:
        """
        The value of the tag.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class IdentityPropertiesResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "principalId":
            suggest = "principal_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in IdentityPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        IdentityPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        IdentityPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 principal_id: str,
                 tenant_id: str,
                 type: Optional[str] = None):
        """
        :param str principal_id: The identity ID.
        :param str tenant_id: The tenant ID of resource.
        """
        pulumi.set(__self__, "principal_id", principal_id)
        pulumi.set(__self__, "tenant_id", tenant_id)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="principalId")
    def principal_id(self) -> str:
        """
        The identity ID.
        """
        return pulumi.get(self, "principal_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> str:
        """
        The tenant ID of resource.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")


@pulumi.output_type
class LogRulesResponse(dict):
    """
    Set of rules for sending logs for the Monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "filteringTags":
            suggest = "filtering_tags"
        elif key == "sendAadLogs":
            suggest = "send_aad_logs"
        elif key == "sendActivityLogs":
            suggest = "send_activity_logs"
        elif key == "sendSubscriptionLogs":
            suggest = "send_subscription_logs"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogRulesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogRulesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogRulesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 filtering_tags: Optional[Sequence['outputs.FilteringTagResponse']] = None,
                 send_aad_logs: Optional[bool] = None,
                 send_activity_logs: Optional[bool] = None,
                 send_subscription_logs: Optional[bool] = None):
        """
        Set of rules for sending logs for the Monitor resource.
        :param Sequence['FilteringTagResponse'] filtering_tags: List of filtering tags to be used for capturing logs. This only takes effect if SendActivityLogs flag is enabled. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        :param bool send_aad_logs: Flag specifying if AAD logs should be sent for the Monitor resource.
        :param bool send_activity_logs: Flag specifying if activity logs from Azure resources should be sent for the Monitor resource.
        :param bool send_subscription_logs: Flag specifying if subscription logs should be sent for the Monitor resource.
        """
        if filtering_tags is not None:
            pulumi.set(__self__, "filtering_tags", filtering_tags)
        if send_aad_logs is not None:
            pulumi.set(__self__, "send_aad_logs", send_aad_logs)
        if send_activity_logs is not None:
            pulumi.set(__self__, "send_activity_logs", send_activity_logs)
        if send_subscription_logs is not None:
            pulumi.set(__self__, "send_subscription_logs", send_subscription_logs)

    @property
    @pulumi.getter(name="filteringTags")
    def filtering_tags(self) -> Optional[Sequence['outputs.FilteringTagResponse']]:
        """
        List of filtering tags to be used for capturing logs. This only takes effect if SendActivityLogs flag is enabled. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        """
        return pulumi.get(self, "filtering_tags")

    @property
    @pulumi.getter(name="sendAadLogs")
    def send_aad_logs(self) -> Optional[bool]:
        """
        Flag specifying if AAD logs should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_aad_logs")

    @property
    @pulumi.getter(name="sendActivityLogs")
    def send_activity_logs(self) -> Optional[bool]:
        """
        Flag specifying if activity logs from Azure resources should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_activity_logs")

    @property
    @pulumi.getter(name="sendSubscriptionLogs")
    def send_subscription_logs(self) -> Optional[bool]:
        """
        Flag specifying if subscription logs should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_subscription_logs")


@pulumi.output_type
class LogzOrganizationPropertiesResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "companyName":
            suggest = "company_name"
        elif key == "enterpriseAppId":
            suggest = "enterprise_app_id"
        elif key == "singleSignOnUrl":
            suggest = "single_sign_on_url"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in LogzOrganizationPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        LogzOrganizationPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        LogzOrganizationPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 id: str,
                 company_name: Optional[str] = None,
                 enterprise_app_id: Optional[str] = None,
                 single_sign_on_url: Optional[str] = None):
        """
        :param str id: Id of the Logz organization.
        :param str company_name: Name of the Logz organization.
        :param str enterprise_app_id: The Id of the Enterprise App used for Single sign on.
        :param str single_sign_on_url: The login URL specific to this Logz Organization.
        """
        pulumi.set(__self__, "id", id)
        if company_name is not None:
            pulumi.set(__self__, "company_name", company_name)
        if enterprise_app_id is not None:
            pulumi.set(__self__, "enterprise_app_id", enterprise_app_id)
        if single_sign_on_url is not None:
            pulumi.set(__self__, "single_sign_on_url", single_sign_on_url)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Id of the Logz organization.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="companyName")
    def company_name(self) -> Optional[str]:
        """
        Name of the Logz organization.
        """
        return pulumi.get(self, "company_name")

    @property
    @pulumi.getter(name="enterpriseAppId")
    def enterprise_app_id(self) -> Optional[str]:
        """
        The Id of the Enterprise App used for Single sign on.
        """
        return pulumi.get(self, "enterprise_app_id")

    @property
    @pulumi.getter(name="singleSignOnUrl")
    def single_sign_on_url(self) -> Optional[str]:
        """
        The login URL specific to this Logz Organization.
        """
        return pulumi.get(self, "single_sign_on_url")


@pulumi.output_type
class MetricRulesResponse(dict):
    """
    Set of rules for sending metrics for the Monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "filteringTags":
            suggest = "filtering_tags"
        elif key == "subscriptionId":
            suggest = "subscription_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricRulesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricRulesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricRulesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 filtering_tags: Optional[Sequence['outputs.FilteringTagResponse']] = None,
                 subscription_id: Optional[str] = None):
        """
        Set of rules for sending metrics for the Monitor resource.
        :param Sequence['FilteringTagResponse'] filtering_tags: List of filtering tags to be used for capturing metrics. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        :param str subscription_id: Subscription Id for which filtering tags are applicable
        """
        if filtering_tags is not None:
            pulumi.set(__self__, "filtering_tags", filtering_tags)
        if subscription_id is not None:
            pulumi.set(__self__, "subscription_id", subscription_id)

    @property
    @pulumi.getter(name="filteringTags")
    def filtering_tags(self) -> Optional[Sequence['outputs.FilteringTagResponse']]:
        """
        List of filtering tags to be used for capturing metrics. If empty, all resources will be captured. If only Exclude action is specified, the rules will apply to the list of all available resources. If Include actions are specified, the rules will only include resources with the associated tags.
        """
        return pulumi.get(self, "filtering_tags")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> Optional[str]:
        """
        Subscription Id for which filtering tags are applicable
        """
        return pulumi.get(self, "subscription_id")


@pulumi.output_type
class MetricsTagRulesPropertiesResponse(dict):
    """
    Definition of the properties for a TagRules resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "systemData":
            suggest = "system_data"
        elif key == "metricRules":
            suggest = "metric_rules"
        elif key == "sendMetrics":
            suggest = "send_metrics"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MetricsTagRulesPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MetricsTagRulesPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MetricsTagRulesPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 provisioning_state: str,
                 system_data: 'outputs.SystemDataResponse',
                 metric_rules: Optional[Sequence['outputs.MetricRulesResponse']] = None,
                 send_metrics: Optional[bool] = None):
        """
        Definition of the properties for a TagRules resource.
        :param str provisioning_state: Flag specifying if the resource provisioning state as tracked by ARM.
        :param 'SystemDataResponse' system_data: Metadata pertaining to creation and last modification of the resource.
        :param bool send_metrics: Flag specifying if metrics from Azure resources should be sent for the Monitor resource.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "system_data", system_data)
        if metric_rules is not None:
            pulumi.set(__self__, "metric_rules", metric_rules)
        if send_metrics is not None:
            pulumi.set(__self__, "send_metrics", send_metrics)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Flag specifying if the resource provisioning state as tracked by ARM.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="metricRules")
    def metric_rules(self) -> Optional[Sequence['outputs.MetricRulesResponse']]:
        return pulumi.get(self, "metric_rules")

    @property
    @pulumi.getter(name="sendMetrics")
    def send_metrics(self) -> Optional[bool]:
        """
        Flag specifying if metrics from Azure resources should be sent for the Monitor resource.
        """
        return pulumi.get(self, "send_metrics")


@pulumi.output_type
class MonitorPropertiesResponse(dict):
    """
    Properties specific to the monitor resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "liftrResourceCategory":
            suggest = "liftr_resource_category"
        elif key == "liftrResourcePreference":
            suggest = "liftr_resource_preference"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "logzOrganizationProperties":
            suggest = "logz_organization_properties"
        elif key == "marketplaceSubscriptionStatus":
            suggest = "marketplace_subscription_status"
        elif key == "monitoringStatus":
            suggest = "monitoring_status"
        elif key == "planData":
            suggest = "plan_data"
        elif key == "userInfo":
            suggest = "user_info"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitorPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitorPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitorPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 liftr_resource_category: str,
                 liftr_resource_preference: int,
                 provisioning_state: str,
                 logz_organization_properties: Optional['outputs.LogzOrganizationPropertiesResponse'] = None,
                 marketplace_subscription_status: Optional[str] = None,
                 monitoring_status: Optional[str] = None,
                 plan_data: Optional['outputs.PlanDataResponse'] = None,
                 user_info: Optional['outputs.UserInfoResponse'] = None):
        """
        Properties specific to the monitor resource.
        :param int liftr_resource_preference: The priority of the resource.
        :param str provisioning_state: Flag specifying if the resource provisioning state as tracked by ARM.
        :param str marketplace_subscription_status: Flag specifying the Marketplace Subscription Status of the resource. If payment is not made in time, the resource will go in Suspended state.
        :param str monitoring_status: Flag specifying if the resource monitoring is enabled or disabled.
        """
        pulumi.set(__self__, "liftr_resource_category", liftr_resource_category)
        pulumi.set(__self__, "liftr_resource_preference", liftr_resource_preference)
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if logz_organization_properties is not None:
            pulumi.set(__self__, "logz_organization_properties", logz_organization_properties)
        if marketplace_subscription_status is not None:
            pulumi.set(__self__, "marketplace_subscription_status", marketplace_subscription_status)
        if monitoring_status is not None:
            pulumi.set(__self__, "monitoring_status", monitoring_status)
        if plan_data is not None:
            pulumi.set(__self__, "plan_data", plan_data)
        if user_info is not None:
            pulumi.set(__self__, "user_info", user_info)

    @property
    @pulumi.getter(name="liftrResourceCategory")
    def liftr_resource_category(self) -> str:
        return pulumi.get(self, "liftr_resource_category")

    @property
    @pulumi.getter(name="liftrResourcePreference")
    def liftr_resource_preference(self) -> int:
        """
        The priority of the resource.
        """
        return pulumi.get(self, "liftr_resource_preference")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Flag specifying if the resource provisioning state as tracked by ARM.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="logzOrganizationProperties")
    def logz_organization_properties(self) -> Optional['outputs.LogzOrganizationPropertiesResponse']:
        return pulumi.get(self, "logz_organization_properties")

    @property
    @pulumi.getter(name="marketplaceSubscriptionStatus")
    def marketplace_subscription_status(self) -> Optional[str]:
        """
        Flag specifying the Marketplace Subscription Status of the resource. If payment is not made in time, the resource will go in Suspended state.
        """
        return pulumi.get(self, "marketplace_subscription_status")

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> Optional[str]:
        """
        Flag specifying if the resource monitoring is enabled or disabled.
        """
        return pulumi.get(self, "monitoring_status")

    @property
    @pulumi.getter(name="planData")
    def plan_data(self) -> Optional['outputs.PlanDataResponse']:
        return pulumi.get(self, "plan_data")

    @property
    @pulumi.getter(name="userInfo")
    def user_info(self) -> Optional['outputs.UserInfoResponse']:
        return pulumi.get(self, "user_info")


@pulumi.output_type
class MonitoredResourceResponse(dict):
    """
    The properties of a resource currently being monitored by the Logz monitor resource.
    """
    def __init__(__self__, *,
                 system_data: 'outputs.SystemDataResponse',
                 id: Optional[str] = None,
                 reason_for_logs_status: Optional[str] = None,
                 reason_for_metrics_status: Optional[str] = None,
                 sending_logs: Optional[bool] = None,
                 sending_metrics: Optional[bool] = None):
        """
        The properties of a resource currently being monitored by the Logz monitor resource.
        :param 'SystemDataResponse' system_data: Metadata pertaining to creation and last modification of the resource.
        :param str id: The ARM id of the resource.
        :param str reason_for_logs_status: Reason for why the resource is sending logs (or why it is not sending).
        :param str reason_for_metrics_status: Reason for why the resource is sending metrics (or why it is not sending).
        :param bool sending_logs: Flag indicating if resource is sending logs to Logz.
        :param bool sending_metrics: Flag indicating if resource is sending metrics to Logz.
        """
        pulumi.set(__self__, "system_data", system_data)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if reason_for_logs_status is not None:
            pulumi.set(__self__, "reason_for_logs_status", reason_for_logs_status)
        if reason_for_metrics_status is not None:
            pulumi.set(__self__, "reason_for_metrics_status", reason_for_metrics_status)
        if sending_logs is not None:
            pulumi.set(__self__, "sending_logs", sending_logs)
        if sending_metrics is not None:
            pulumi.set(__self__, "sending_metrics", sending_metrics)

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ARM id of the resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="reasonForLogsStatus")
    def reason_for_logs_status(self) -> Optional[str]:
        """
        Reason for why the resource is sending logs (or why it is not sending).
        """
        return pulumi.get(self, "reason_for_logs_status")

    @property
    @pulumi.getter(name="reasonForMetricsStatus")
    def reason_for_metrics_status(self) -> Optional[str]:
        """
        Reason for why the resource is sending metrics (or why it is not sending).
        """
        return pulumi.get(self, "reason_for_metrics_status")

    @property
    @pulumi.getter(name="sendingLogs")
    def sending_logs(self) -> Optional[bool]:
        """
        Flag indicating if resource is sending logs to Logz.
        """
        return pulumi.get(self, "sending_logs")

    @property
    @pulumi.getter(name="sendingMetrics")
    def sending_metrics(self) -> Optional[bool]:
        """
        Flag indicating if resource is sending metrics to Logz.
        """
        return pulumi.get(self, "sending_metrics")


@pulumi.output_type
class MonitoringTagRulesPropertiesResponse(dict):
    """
    Definition of the properties for a TagRules resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "systemData":
            suggest = "system_data"
        elif key == "logRules":
            suggest = "log_rules"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in MonitoringTagRulesPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        MonitoringTagRulesPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        MonitoringTagRulesPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 provisioning_state: str,
                 system_data: 'outputs.SystemDataResponse',
                 log_rules: Optional['outputs.LogRulesResponse'] = None):
        """
        Definition of the properties for a TagRules resource.
        :param str provisioning_state: Flag specifying if the resource provisioning state as tracked by ARM.
        :param 'SystemDataResponse' system_data: Metadata pertaining to creation and last modification of the resource.
        :param 'LogRulesResponse' log_rules: Set of rules for sending logs for the Monitor resource.
        """
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        pulumi.set(__self__, "system_data", system_data)
        if log_rules is not None:
            pulumi.set(__self__, "log_rules", log_rules)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        Flag specifying if the resource provisioning state as tracked by ARM.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> 'outputs.SystemDataResponse':
        """
        Metadata pertaining to creation and last modification of the resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter(name="logRules")
    def log_rules(self) -> Optional['outputs.LogRulesResponse']:
        """
        Set of rules for sending logs for the Monitor resource.
        """
        return pulumi.get(self, "log_rules")


@pulumi.output_type
class PlanDataResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "billingCycle":
            suggest = "billing_cycle"
        elif key == "effectiveDate":
            suggest = "effective_date"
        elif key == "planDetails":
            suggest = "plan_details"
        elif key == "usageType":
            suggest = "usage_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in PlanDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        PlanDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        PlanDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 billing_cycle: Optional[str] = None,
                 effective_date: Optional[str] = None,
                 plan_details: Optional[str] = None,
                 usage_type: Optional[str] = None):
        """
        :param str billing_cycle: different billing cycles like MONTHLY/WEEKLY. this could be enum
        :param str effective_date: date when plan was applied
        :param str plan_details: plan id as published by Logz
        :param str usage_type: different usage type like PAYG/COMMITTED. this could be enum
        """
        if billing_cycle is not None:
            pulumi.set(__self__, "billing_cycle", billing_cycle)
        if effective_date is not None:
            pulumi.set(__self__, "effective_date", effective_date)
        if plan_details is not None:
            pulumi.set(__self__, "plan_details", plan_details)
        if usage_type is not None:
            pulumi.set(__self__, "usage_type", usage_type)

    @property
    @pulumi.getter(name="billingCycle")
    def billing_cycle(self) -> Optional[str]:
        """
        different billing cycles like MONTHLY/WEEKLY. this could be enum
        """
        return pulumi.get(self, "billing_cycle")

    @property
    @pulumi.getter(name="effectiveDate")
    def effective_date(self) -> Optional[str]:
        """
        date when plan was applied
        """
        return pulumi.get(self, "effective_date")

    @property
    @pulumi.getter(name="planDetails")
    def plan_details(self) -> Optional[str]:
        """
        plan id as published by Logz
        """
        return pulumi.get(self, "plan_details")

    @property
    @pulumi.getter(name="usageType")
    def usage_type(self) -> Optional[str]:
        """
        different usage type like PAYG/COMMITTED. this could be enum
        """
        return pulumi.get(self, "usage_type")


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "createdBy":
            suggest = "created_by"
        elif key == "createdByType":
            suggest = "created_by_type"
        elif key == "lastModifiedAt":
            suggest = "last_modified_at"
        elif key == "lastModifiedBy":
            suggest = "last_modified_by"
        elif key == "lastModifiedByType":
            suggest = "last_modified_by_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SystemDataResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SystemDataResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The timestamp of resource last modification (UTC)
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The timestamp of resource last modification (UTC)
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")


@pulumi.output_type
class UserInfoResponse(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "emailAddress":
            suggest = "email_address"
        elif key == "firstName":
            suggest = "first_name"
        elif key == "lastName":
            suggest = "last_name"
        elif key == "phoneNumber":
            suggest = "phone_number"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in UserInfoResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        UserInfoResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        UserInfoResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 email_address: Optional[str] = None,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 phone_number: Optional[str] = None):
        """
        :param str email_address: Email of the user used by Logz for contacting them if needed
        :param str first_name: First Name of the user
        :param str last_name: Last Name of the user
        :param str phone_number: Phone number of the user used by Logz for contacting them if needed
        """
        if email_address is not None:
            pulumi.set(__self__, "email_address", email_address)
        if first_name is not None:
            pulumi.set(__self__, "first_name", first_name)
        if last_name is not None:
            pulumi.set(__self__, "last_name", last_name)
        if phone_number is not None:
            pulumi.set(__self__, "phone_number", phone_number)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> Optional[str]:
        """
        Email of the user used by Logz for contacting them if needed
        """
        return pulumi.get(self, "email_address")

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> Optional[str]:
        """
        First Name of the user
        """
        return pulumi.get(self, "first_name")

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> Optional[str]:
        """
        Last Name of the user
        """
        return pulumi.get(self, "last_name")

    @property
    @pulumi.getter(name="phoneNumber")
    def phone_number(self) -> Optional[str]:
        """
        Phone number of the user used by Logz for contacting them if needed
        """
        return pulumi.get(self, "phone_number")


@pulumi.output_type
class UserRoleResponseResponse(dict):
    """
    Response for checking user's role for Logz.io account.
    """
    def __init__(__self__, *,
                 role: Optional[str] = None):
        """
        Response for checking user's role for Logz.io account.
        :param str role: User roles on configured in Logz.io account.
        """
        if role is not None:
            pulumi.set(__self__, "role", role)

    @property
    @pulumi.getter
    def role(self) -> Optional[str]:
        """
        User roles on configured in Logz.io account.
        """
        return pulumi.get(self, "role")


@pulumi.output_type
class VMResourcesResponse(dict):
    """
    VM Resource Ids
    """
    def __init__(__self__, *,
                 agent_version: Optional[str] = None,
                 id: Optional[str] = None):
        """
        VM Resource Ids
        :param str agent_version: Version of the Logz agent installed on the VM.
        :param str id: Request of a list vm host update operation.
        """
        if agent_version is not None:
            pulumi.set(__self__, "agent_version", agent_version)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="agentVersion")
    def agent_version(self) -> Optional[str]:
        """
        Version of the Logz agent installed on the VM.
        """
        return pulumi.get(self, "agent_version")

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Request of a list vm host update operation.
        """
        return pulumi.get(self, "id")


