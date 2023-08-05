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
from ._inputs import *

__all__ = ['WebAppBackupConfigurationArgs', 'WebAppBackupConfiguration']

@pulumi.input_type
class WebAppBackupConfigurationArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 storage_account_url: pulumi.Input[str],
                 backup_name: Optional[pulumi.Input[str]] = None,
                 backup_schedule: Optional[pulumi.Input['BackupScheduleArgs']] = None,
                 databases: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseBackupSettingArgs']]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a WebAppBackupConfiguration resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] storage_account_url: SAS URL to the container.
        :param pulumi.Input[str] backup_name: Name of the backup.
        :param pulumi.Input['BackupScheduleArgs'] backup_schedule: Schedule for the backup if it is executed periodically.
        :param pulumi.Input[Sequence[pulumi.Input['DatabaseBackupSettingArgs']]] databases: Databases included in the backup.
        :param pulumi.Input[bool] enabled: True if the backup schedule is enabled (must be included in that case), false if the backup schedule should be disabled.
        :param pulumi.Input[str] kind: Kind of resource.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "storage_account_url", storage_account_url)
        if backup_name is not None:
            pulumi.set(__self__, "backup_name", backup_name)
        if backup_schedule is not None:
            pulumi.set(__self__, "backup_schedule", backup_schedule)
        if databases is not None:
            pulumi.set(__self__, "databases", databases)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Name of the app.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group to which the resource belongs.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="storageAccountUrl")
    def storage_account_url(self) -> pulumi.Input[str]:
        """
        SAS URL to the container.
        """
        return pulumi.get(self, "storage_account_url")

    @storage_account_url.setter
    def storage_account_url(self, value: pulumi.Input[str]):
        pulumi.set(self, "storage_account_url", value)

    @property
    @pulumi.getter(name="backupName")
    def backup_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the backup.
        """
        return pulumi.get(self, "backup_name")

    @backup_name.setter
    def backup_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "backup_name", value)

    @property
    @pulumi.getter(name="backupSchedule")
    def backup_schedule(self) -> Optional[pulumi.Input['BackupScheduleArgs']]:
        """
        Schedule for the backup if it is executed periodically.
        """
        return pulumi.get(self, "backup_schedule")

    @backup_schedule.setter
    def backup_schedule(self, value: Optional[pulumi.Input['BackupScheduleArgs']]):
        pulumi.set(self, "backup_schedule", value)

    @property
    @pulumi.getter
    def databases(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseBackupSettingArgs']]]]:
        """
        Databases included in the backup.
        """
        return pulumi.get(self, "databases")

    @databases.setter
    def databases(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['DatabaseBackupSettingArgs']]]]):
        pulumi.set(self, "databases", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        True if the backup schedule is enabled (must be included in that case), false if the backup schedule should be disabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)


class WebAppBackupConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_name: Optional[pulumi.Input[str]] = None,
                 backup_schedule: Optional[pulumi.Input[pulumi.InputType['BackupScheduleArgs']]] = None,
                 databases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseBackupSettingArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_account_url: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Description of a backup which will be performed.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] backup_name: Name of the backup.
        :param pulumi.Input[pulumi.InputType['BackupScheduleArgs']] backup_schedule: Schedule for the backup if it is executed periodically.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseBackupSettingArgs']]]] databases: Databases included in the backup.
        :param pulumi.Input[bool] enabled: True if the backup schedule is enabled (must be included in that case), false if the backup schedule should be disabled.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] storage_account_url: SAS URL to the container.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: WebAppBackupConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Description of a backup which will be performed.

        :param str resource_name: The name of the resource.
        :param WebAppBackupConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(WebAppBackupConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 backup_name: Optional[pulumi.Input[str]] = None,
                 backup_schedule: Optional[pulumi.Input[pulumi.InputType['BackupScheduleArgs']]] = None,
                 databases: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['DatabaseBackupSettingArgs']]]]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 storage_account_url: Optional[pulumi.Input[str]] = None,
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
            __props__ = WebAppBackupConfigurationArgs.__new__(WebAppBackupConfigurationArgs)

            __props__.__dict__["backup_name"] = backup_name
            __props__.__dict__["backup_schedule"] = backup_schedule
            __props__.__dict__["databases"] = databases
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["kind"] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            if storage_account_url is None and not opts.urn:
                raise TypeError("Missing required property 'storage_account_url'")
            __props__.__dict__["storage_account_url"] = storage_account_url
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:web:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20150801:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20160801:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20181101:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20190801:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20200601:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20200901:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20201001:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20201201:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20210101:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20210115:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20210201:WebAppBackupConfiguration"), pulumi.Alias(type_="azure-native:web/v20210301:WebAppBackupConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppBackupConfiguration, __self__).__init__(
            'azure-native:web/v20180201:WebAppBackupConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppBackupConfiguration':
        """
        Get an existing WebAppBackupConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = WebAppBackupConfigurationArgs.__new__(WebAppBackupConfigurationArgs)

        __props__.__dict__["backup_name"] = None
        __props__.__dict__["backup_schedule"] = None
        __props__.__dict__["databases"] = None
        __props__.__dict__["enabled"] = None
        __props__.__dict__["kind"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["storage_account_url"] = None
        __props__.__dict__["type"] = None
        return WebAppBackupConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="backupName")
    def backup_name(self) -> pulumi.Output[Optional[str]]:
        """
        Name of the backup.
        """
        return pulumi.get(self, "backup_name")

    @property
    @pulumi.getter(name="backupSchedule")
    def backup_schedule(self) -> pulumi.Output[Optional['outputs.BackupScheduleResponse']]:
        """
        Schedule for the backup if it is executed periodically.
        """
        return pulumi.get(self, "backup_schedule")

    @property
    @pulumi.getter
    def databases(self) -> pulumi.Output[Optional[Sequence['outputs.DatabaseBackupSettingResponse']]]:
        """
        Databases included in the backup.
        """
        return pulumi.get(self, "databases")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        True if the backup schedule is enabled (must be included in that case), false if the backup schedule should be disabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="storageAccountUrl")
    def storage_account_url(self) -> pulumi.Output[str]:
        """
        SAS URL to the container.
        """
        return pulumi.get(self, "storage_account_url")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

