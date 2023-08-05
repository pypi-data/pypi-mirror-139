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
    'SubscriptionAliasResponsePropertiesResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class SubscriptionAliasResponsePropertiesResponse(dict):
    """
    Put subscription creation result properties.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "acceptOwnershipState":
            suggest = "accept_ownership_state"
        elif key == "acceptOwnershipUrl":
            suggest = "accept_ownership_url"
        elif key == "subscriptionId":
            suggest = "subscription_id"
        elif key == "billingScope":
            suggest = "billing_scope"
        elif key == "createdTime":
            suggest = "created_time"
        elif key == "displayName":
            suggest = "display_name"
        elif key == "managementGroupId":
            suggest = "management_group_id"
        elif key == "provisioningState":
            suggest = "provisioning_state"
        elif key == "resellerId":
            suggest = "reseller_id"
        elif key == "subscriptionOwnerId":
            suggest = "subscription_owner_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SubscriptionAliasResponsePropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SubscriptionAliasResponsePropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SubscriptionAliasResponsePropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 accept_ownership_state: str,
                 accept_ownership_url: str,
                 subscription_id: str,
                 billing_scope: Optional[str] = None,
                 created_time: Optional[str] = None,
                 display_name: Optional[str] = None,
                 management_group_id: Optional[str] = None,
                 provisioning_state: Optional[str] = None,
                 reseller_id: Optional[str] = None,
                 subscription_owner_id: Optional[str] = None,
                 tags: Optional[Mapping[str, str]] = None,
                 workload: Optional[str] = None):
        """
        Put subscription creation result properties.
        :param str accept_ownership_state: The accept ownership state of the resource.
        :param str accept_ownership_url: Url to accept ownership of the subscription.
        :param str subscription_id: Newly created subscription Id.
        :param str billing_scope: Billing scope of the subscription.
               For CustomerLed and FieldLed - /billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}
               For PartnerLed - /billingAccounts/{billingAccountName}/customers/{customerName}
               For Legacy EA - /billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}
        :param str created_time: Created Time
        :param str display_name: The display name of the subscription.
        :param str management_group_id: The Management Group Id.
        :param str provisioning_state: The provisioning state of the resource.
        :param str reseller_id: Reseller Id
        :param str subscription_owner_id: Owner Id of the subscription
        :param Mapping[str, str] tags: Tags for the subscription
        :param str workload: The workload type of the subscription. It can be either Production or DevTest.
        """
        pulumi.set(__self__, "accept_ownership_state", accept_ownership_state)
        pulumi.set(__self__, "accept_ownership_url", accept_ownership_url)
        pulumi.set(__self__, "subscription_id", subscription_id)
        if billing_scope is not None:
            pulumi.set(__self__, "billing_scope", billing_scope)
        if created_time is not None:
            pulumi.set(__self__, "created_time", created_time)
        if display_name is not None:
            pulumi.set(__self__, "display_name", display_name)
        if management_group_id is not None:
            pulumi.set(__self__, "management_group_id", management_group_id)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if reseller_id is not None:
            pulumi.set(__self__, "reseller_id", reseller_id)
        if subscription_owner_id is not None:
            pulumi.set(__self__, "subscription_owner_id", subscription_owner_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if workload is not None:
            pulumi.set(__self__, "workload", workload)

    @property
    @pulumi.getter(name="acceptOwnershipState")
    def accept_ownership_state(self) -> str:
        """
        The accept ownership state of the resource.
        """
        return pulumi.get(self, "accept_ownership_state")

    @property
    @pulumi.getter(name="acceptOwnershipUrl")
    def accept_ownership_url(self) -> str:
        """
        Url to accept ownership of the subscription.
        """
        return pulumi.get(self, "accept_ownership_url")

    @property
    @pulumi.getter(name="subscriptionId")
    def subscription_id(self) -> str:
        """
        Newly created subscription Id.
        """
        return pulumi.get(self, "subscription_id")

    @property
    @pulumi.getter(name="billingScope")
    def billing_scope(self) -> Optional[str]:
        """
        Billing scope of the subscription.
        For CustomerLed and FieldLed - /billingAccounts/{billingAccountName}/billingProfiles/{billingProfileName}/invoiceSections/{invoiceSectionName}
        For PartnerLed - /billingAccounts/{billingAccountName}/customers/{customerName}
        For Legacy EA - /billingAccounts/{billingAccountName}/enrollmentAccounts/{enrollmentAccountName}
        """
        return pulumi.get(self, "billing_scope")

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> Optional[str]:
        """
        Created Time
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> Optional[str]:
        """
        The display name of the subscription.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter(name="managementGroupId")
    def management_group_id(self) -> Optional[str]:
        """
        The Management Group Id.
        """
        return pulumi.get(self, "management_group_id")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The provisioning state of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resellerId")
    def reseller_id(self) -> Optional[str]:
        """
        Reseller Id
        """
        return pulumi.get(self, "reseller_id")

    @property
    @pulumi.getter(name="subscriptionOwnerId")
    def subscription_owner_id(self) -> Optional[str]:
        """
        Owner Id of the subscription
        """
        return pulumi.get(self, "subscription_owner_id")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags for the subscription
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def workload(self) -> Optional[str]:
        """
        The workload type of the subscription. It can be either Production or DevTest.
        """
        return pulumi.get(self, "workload")


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


