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

__all__ = ['JobArgs', 'Job']

@pulumi.input_type
class JobArgs:
    def __init__(__self__, *,
                 job_agent_name: pulumi.Input[str],
                 resource_group_name: pulumi.Input[str],
                 server_name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input['JobScheduleArgs']] = None):
        """
        The set of arguments for constructing a Job resource.
        :param pulumi.Input[str] job_agent_name: The name of the job agent.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] description: User-defined description of the job.
        :param pulumi.Input[str] job_name: The name of the job to get.
        :param pulumi.Input['JobScheduleArgs'] schedule: Schedule properties of the job.
        """
        pulumi.set(__self__, "job_agent_name", job_agent_name)
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "server_name", server_name)
        if description is None:
            description = ''
        if description is not None:
            pulumi.set(__self__, "description", description)
        if job_name is not None:
            pulumi.set(__self__, "job_name", job_name)
        if schedule is not None:
            pulumi.set(__self__, "schedule", schedule)

    @property
    @pulumi.getter(name="jobAgentName")
    def job_agent_name(self) -> pulumi.Input[str]:
        """
        The name of the job agent.
        """
        return pulumi.get(self, "job_agent_name")

    @job_agent_name.setter
    def job_agent_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "job_agent_name", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="serverName")
    def server_name(self) -> pulumi.Input[str]:
        """
        The name of the server.
        """
        return pulumi.get(self, "server_name")

    @server_name.setter
    def server_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        User-defined description of the job.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="jobName")
    def job_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the job to get.
        """
        return pulumi.get(self, "job_name")

    @job_name.setter
    def job_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "job_name", value)

    @property
    @pulumi.getter
    def schedule(self) -> Optional[pulumi.Input['JobScheduleArgs']]:
        """
        Schedule properties of the job.
        """
        return pulumi.get(self, "schedule")

    @schedule.setter
    def schedule(self, value: Optional[pulumi.Input['JobScheduleArgs']]):
        pulumi.set(self, "schedule", value)


class Job(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['JobScheduleArgs']]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        A job.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] description: User-defined description of the job.
        :param pulumi.Input[str] job_agent_name: The name of the job agent.
        :param pulumi.Input[str] job_name: The name of the job to get.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[pulumi.InputType['JobScheduleArgs']] schedule: Schedule properties of the job.
        :param pulumi.Input[str] server_name: The name of the server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: JobArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A job.

        :param str resource_name: The name of the resource.
        :param JobArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(JobArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 job_agent_name: Optional[pulumi.Input[str]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule: Optional[pulumi.Input[pulumi.InputType['JobScheduleArgs']]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
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
            __props__ = JobArgs.__new__(JobArgs)

            if description is None:
                description = ''
            __props__.__dict__["description"] = description
            if job_agent_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_agent_name'")
            __props__.__dict__["job_agent_name"] = job_agent_name
            __props__.__dict__["job_name"] = job_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["schedule"] = schedule
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__.__dict__["server_name"] = server_name
            __props__.__dict__["name"] = None
            __props__.__dict__["type"] = None
            __props__.__dict__["version"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:sql:Job"), pulumi.Alias(type_="azure-native:sql/v20170301preview:Job"), pulumi.Alias(type_="azure-native:sql/v20200202preview:Job"), pulumi.Alias(type_="azure-native:sql/v20200801preview:Job"), pulumi.Alias(type_="azure-native:sql/v20210201preview:Job"), pulumi.Alias(type_="azure-native:sql/v20210501preview:Job"), pulumi.Alias(type_="azure-native:sql/v20210801preview:Job")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Job, __self__).__init__(
            'azure-native:sql/v20201101preview:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = JobArgs.__new__(JobArgs)

        __props__.__dict__["description"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["schedule"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["version"] = None
        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        User-defined description of the job.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def schedule(self) -> pulumi.Output[Optional['outputs.JobScheduleResponse']]:
        """
        Schedule properties of the job.
        """
        return pulumi.get(self, "schedule")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[int]:
        """
        The job version number.
        """
        return pulumi.get(self, "version")

