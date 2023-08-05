# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities
from . import outputs

__all__ = [
    'GetPipelineResult',
    'AwaitableGetPipelineResult',
    'get_pipeline',
    'get_pipeline_output',
]

@pulumi.output_type
class GetPipelineResult:
    """
    Azure DevOps Pipeline used to configure Continuous Integration (CI) & Continuous Delivery (CD) for Azure resources.
    """
    def __init__(__self__, bootstrap_configuration=None, id=None, location=None, name=None, organization=None, pipeline_id=None, project=None, tags=None, type=None):
        if bootstrap_configuration and not isinstance(bootstrap_configuration, dict):
            raise TypeError("Expected argument 'bootstrap_configuration' to be a dict")
        pulumi.set(__self__, "bootstrap_configuration", bootstrap_configuration)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if organization and not isinstance(organization, dict):
            raise TypeError("Expected argument 'organization' to be a dict")
        pulumi.set(__self__, "organization", organization)
        if pipeline_id and not isinstance(pipeline_id, int):
            raise TypeError("Expected argument 'pipeline_id' to be a int")
        pulumi.set(__self__, "pipeline_id", pipeline_id)
        if project and not isinstance(project, dict):
            raise TypeError("Expected argument 'project' to be a dict")
        pulumi.set(__self__, "project", project)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="bootstrapConfiguration")
    def bootstrap_configuration(self) -> 'outputs.BootstrapConfigurationResponse':
        """
        Configuration used to bootstrap the Pipeline.
        """
        return pulumi.get(self, "bootstrap_configuration")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> Optional[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def organization(self) -> 'outputs.OrganizationReferenceResponse':
        """
        Reference to the Azure DevOps Organization containing the Pipeline.
        """
        return pulumi.get(self, "organization")

    @property
    @pulumi.getter(name="pipelineId")
    def pipeline_id(self) -> int:
        """
        Unique identifier of the Azure Pipeline within the Azure DevOps Project.
        """
        return pulumi.get(self, "pipeline_id")

    @property
    @pulumi.getter
    def project(self) -> 'outputs.ProjectReferenceResponse':
        """
        Reference to the Azure DevOps Project containing the Pipeline.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource Tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource Type
        """
        return pulumi.get(self, "type")


class AwaitableGetPipelineResult(GetPipelineResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPipelineResult(
            bootstrap_configuration=self.bootstrap_configuration,
            id=self.id,
            location=self.location,
            name=self.name,
            organization=self.organization,
            pipeline_id=self.pipeline_id,
            project=self.project,
            tags=self.tags,
            type=self.type)


def get_pipeline(pipeline_name: Optional[str] = None,
                 resource_group_name: Optional[str] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPipelineResult:
    """
    Azure DevOps Pipeline used to configure Continuous Integration (CI) & Continuous Delivery (CD) for Azure resources.


    :param str pipeline_name: The name of the Azure Pipeline resource in ARM.
    :param str resource_group_name: Name of the resource group within the Azure subscription.
    """
    __args__ = dict()
    __args__['pipelineName'] = pipeline_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:devops/v20190701preview:getPipeline', __args__, opts=opts, typ=GetPipelineResult).value

    return AwaitableGetPipelineResult(
        bootstrap_configuration=__ret__.bootstrap_configuration,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        organization=__ret__.organization,
        pipeline_id=__ret__.pipeline_id,
        project=__ret__.project,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_pipeline)
def get_pipeline_output(pipeline_name: Optional[pulumi.Input[str]] = None,
                        resource_group_name: Optional[pulumi.Input[str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPipelineResult]:
    """
    Azure DevOps Pipeline used to configure Continuous Integration (CI) & Continuous Delivery (CD) for Azure resources.


    :param str pipeline_name: The name of the Azure Pipeline resource in ARM.
    :param str resource_group_name: Name of the resource group within the Azure subscription.
    """
    ...
