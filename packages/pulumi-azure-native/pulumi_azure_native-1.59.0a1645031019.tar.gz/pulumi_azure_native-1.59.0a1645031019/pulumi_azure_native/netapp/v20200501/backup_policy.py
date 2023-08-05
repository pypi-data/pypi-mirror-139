# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs
from ._inputs import *

__all__ = ['BackupPolicyArgs', 'BackupPolicy']

@pulumi.input_type
class BackupPolicyArgs:
    def __init__(__self__, *,
                 account_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 backup_policy_name: Optional[pulumi.Input[str]] = None,
                 daily_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_backups: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeBackupsArgs']]]] = None,
                 volumes_assigned: Optional[pulumi.Input[int]] = None,
                 weekly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 yearly_backups_to_keep: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a BackupPolicy resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] backup_policy_name: Backup policy Name which uniquely identify backup policy.
        :param pulumi.Input[int] daily_backups_to_keep: Daily backups count to keep
        :param pulumi.Input[bool] enabled: The property to decide policy is enabled or not
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] monthly_backups_to_keep: Monthly backups count to keep
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input['VolumeBackupsArgs']]] volume_backups: A list of volumes assigned to this policy
        :param pulumi.Input[int] volumes_assigned: Volumes using current backup policy
        :param pulumi.Input[int] weekly_backups_to_keep: Weekly backups count to keep
        :param pulumi.Input[int] yearly_backups_to_keep: Yearly backups count to keep
        """
        pulumi.set(__self__, "account_name", account_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if backup_policy_name is not None:
            pulumi.set(__self__, "backup_policy_name", backup_policy_name)
        if daily_backups_to_keep is not None:
            pulumi.set(__self__, "daily_backups_to_keep", daily_backups_to_keep)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if monthly_backups_to_keep is not None:
            pulumi.set(__self__, "monthly_backups_to_keep", monthly_backups_to_keep)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if volume_backups is not None:
            pulumi.set(__self__, "volume_backups", volume_backups)
        if volumes_assigned is not None:
            pulumi.set(__self__, "volumes_assigned", volumes_assigned)
        if weekly_backups_to_keep is not None:
            pulumi.set(__self__, "weekly_backups_to_keep", weekly_backups_to_keep)
        if yearly_backups_to_keep is not None:
            pulumi.set(__self__, "yearly_backups_to_keep", yearly_backups_to_keep)

    @property
    @pulumi.getter(name="accountName")
    def account_name(self) -> pulumi.Input[str]:
        """
        The name of the NetApp account
        """
        return pulumi.get(self, "account_name")

    @account_name.setter
    def account_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "account_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="backupPolicyName")
    def backup_policy_name(self) -> Optional[pulumi.Input[str]]:
        """
        Backup policy Name which uniquely identify backup policy.
        """
        return pulumi.get(self, "backup_policy_name")

    @backup_policy_name.setter
    def backup_policy_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_policy_name", value)

    @property
    @pulumi.getter(name="dailyBackupsToKeep")
    def daily_backups_to_keep(self) -> Optional[pulumi.Input[int]]:
        """
        Daily backups count to keep
        """
        return pulumi.get(self, "daily_backups_to_keep")

    @daily_backups_to_keep.setter
    def daily_backups_to_keep(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "daily_backups_to_keep", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        The property to decide policy is enabled or not
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="monthlyBackupsToKeep")
    def monthly_backups_to_keep(self) -> Optional[pulumi.Input[int]]:
        """
        Monthly backups count to keep
        """
        return pulumi.get(self, "monthly_backups_to_keep")

    @monthly_backups_to_keep.setter
    def monthly_backups_to_keep(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "monthly_backups_to_keep", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="volumeBackups")
    def volume_backups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['VolumeBackupsArgs']]]]:
        """
        A list of volumes assigned to this policy
        """
        return pulumi.get(self, "volume_backups")

    @volume_backups.setter
    def volume_backups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['VolumeBackupsArgs']]]]):
        pulumi.set(self, "volume_backups", value)

    @property
    @pulumi.getter(name="volumesAssigned")
    def volumes_assigned(self) -> Optional[pulumi.Input[int]]:
        """
        Volumes using current backup policy
        """
        return pulumi.get(self, "volumes_assigned")

    @volumes_assigned.setter
    def volumes_assigned(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "volumes_assigned", value)

    @property
    @pulumi.getter(name="weeklyBackupsToKeep")
    def weekly_backups_to_keep(self) -> Optional[pulumi.Input[int]]:
        """
        Weekly backups count to keep
        """
        return pulumi.get(self, "weekly_backups_to_keep")

    @weekly_backups_to_keep.setter
    def weekly_backups_to_keep(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "weekly_backups_to_keep", value)

    @property
    @pulumi.getter(name="yearlyBackupsToKeep")
    def yearly_backups_to_keep(self) -> Optional[pulumi.Input[int]]:
        """
        Yearly backups count to keep
        """
        return pulumi.get(self, "yearly_backups_to_keep")

    @yearly_backups_to_keep.setter
    def yearly_backups_to_keep(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "yearly_backups_to_keep", value)


class BackupPolicy(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 backup_policy_name: Optional[pulumi.Input[str]] = None,
                 daily_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_backups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeBackupsArgs']]]]] = None,
                 volumes_assigned: Optional[pulumi.Input[int]] = None,
                 weekly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 yearly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Backup policy information

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] backup_policy_name: Backup policy Name which uniquely identify backup policy.
        :param pulumi.Input[int] daily_backups_to_keep: Daily backups count to keep
        :param pulumi.Input[bool] enabled: The property to decide policy is enabled or not
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[int] monthly_backups_to_keep: Monthly backups count to keep
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeBackupsArgs']]]] volume_backups: A list of volumes assigned to this policy
        :param pulumi.Input[int] volumes_assigned: Volumes using current backup policy
        :param pulumi.Input[int] weekly_backups_to_keep: Weekly backups count to keep
        :param pulumi.Input[int] yearly_backups_to_keep: Yearly backups count to keep
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BackupPolicyArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Backup policy information

        :param str resource_name: The name of the resource.
        :param BackupPolicyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BackupPolicyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 backup_policy_name: Optional[pulumi.Input[str]] = None,
                 daily_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 monthly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volume_backups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeBackupsArgs']]]]] = None,
                 volumes_assigned: Optional[pulumi.Input[int]] = None,
                 weekly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 yearly_backups_to_keep: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BackupPolicyArgs.__new__(BackupPolicyArgs)

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__.__dict__["account_name"] = account_name
            __props__.__dict__["backup_policy_name"] = backup_policy_name
            __props__.__dict__["daily_backups_to_keep"] = daily_backups_to_keep
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["location"] = location
            __props__.__dict__["monthly_backups_to_keep"] = monthly_backups_to_keep
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["volume_backups"] = volume_backups
            __props__.__dict__["volumes_assigned"] = volumes_assigned
            __props__.__dict__["weekly_backups_to_keep"] = weekly_backups_to_keep
            __props__.__dict__["yearly_backups_to_keep"] = yearly_backups_to_keep
            __props__.__dict__["name"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:netapp:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200601:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200701:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200801:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20200901:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20201101:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20201201:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210201:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210401:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210401preview:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210601:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20210801:BackupPolicy"), pulumi.Alias(type_="azure-native:netapp/v20211001:BackupPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BackupPolicy, __self__).__init__(
            'azure-native:netapp/v20200501:BackupPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BackupPolicy':
        """
        Get an existing BackupPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = BackupPolicyArgs.__new__(BackupPolicyArgs)

        __props__.__dict__["daily_backups_to_keep"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["monthly_backups_to_keep"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["volume_backups"] = None
        __props__.__dict__["volumes_assigned"] = None
        __props__.__dict__["weekly_backups_to_keep"] = None
        __props__.__dict__["yearly_backups_to_keep"] = None
        return BackupPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="dailyBackupsToKeep")
    def daily_backups_to_keep(self) -> pulumi.Output[Optional[int]]:
        """
        Daily backups count to keep
        """
        return pulumi.get(self, "daily_backups_to_keep")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        The property to decide policy is enabled or not
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="monthlyBackupsToKeep")
    def monthly_backups_to_keep(self) -> pulumi.Output[Optional[int]]:
        """
        Monthly backups count to keep
        """
        return pulumi.get(self, "monthly_backups_to_keep")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of backup policy
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="volumeBackups")
    def volume_backups(self) -> pulumi.Output[Optional[Sequence['outputs.VolumeBackupsResponse']]]:
        """
        A list of volumes assigned to this policy
        """
        return pulumi.get(self, "volume_backups")

    @property
    @pulumi.getter(name="volumesAssigned")
    def volumes_assigned(self) -> pulumi.Output[Optional[int]]:
        """
        Volumes using current backup policy
        """
        return pulumi.get(self, "volumes_assigned")

    @property
    @pulumi.getter(name="weeklyBackupsToKeep")
    def weekly_backups_to_keep(self) -> pulumi.Output[Optional[int]]:
        """
        Weekly backups count to keep
        """
        return pulumi.get(self, "weekly_backups_to_keep")

    @property
    @pulumi.getter(name="yearlyBackupsToKeep")
    def yearly_backups_to_keep(self) -> pulumi.Output[Optional[int]]:
        """
        Yearly backups count to keep
        """
        return pulumi.get(self, "yearly_backups_to_keep")

