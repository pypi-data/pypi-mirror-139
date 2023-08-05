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
    'ArtifactDeploymentStatusPropertiesArgs',
    'ArtifactInstallPropertiesArgs',
    'ArtifactParameterPropertiesArgs',
    'CustomImagePropertiesCustomArgs',
    'CustomImagePropertiesFromVmArgs',
    'DayDetailsArgs',
    'FormulaPropertiesFromVmArgs',
    'GalleryImageReferenceArgs',
    'HourDetailsArgs',
    'LabVirtualMachineArgs',
    'LinuxOsInfoArgs',
    'SubnetOverrideArgs',
    'SubnetArgs',
    'WeekDetailsArgs',
    'WindowsOsInfoArgs',
]

@pulumi.input_type
class ArtifactDeploymentStatusPropertiesArgs:
    def __init__(__self__, *,
                 artifacts_applied: Optional[pulumi.Input[int]] = None,
                 deployment_status: Optional[pulumi.Input[str]] = None,
                 total_artifacts: Optional[pulumi.Input[int]] = None):
        """
        Properties of an artifact deployment.
        :param pulumi.Input[int] artifacts_applied: The total count of the artifacts that were successfully applied.
        :param pulumi.Input[str] deployment_status: The deployment status of the artifact.
        :param pulumi.Input[int] total_artifacts: The total count of the artifacts that were tentatively applied.
        """
        if artifacts_applied is not None:
            pulumi.set(__self__, "artifacts_applied", artifacts_applied)
        if deployment_status is not None:
            pulumi.set(__self__, "deployment_status", deployment_status)
        if total_artifacts is not None:
            pulumi.set(__self__, "total_artifacts", total_artifacts)

    @property
    @pulumi.getter(name="artifactsApplied")
    def artifacts_applied(self) -> Optional[pulumi.Input[int]]:
        """
        The total count of the artifacts that were successfully applied.
        """
        return pulumi.get(self, "artifacts_applied")

    @artifacts_applied.setter
    def artifacts_applied(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "artifacts_applied", value)

    @property
    @pulumi.getter(name="deploymentStatus")
    def deployment_status(self) -> Optional[pulumi.Input[str]]:
        """
        The deployment status of the artifact.
        """
        return pulumi.get(self, "deployment_status")

    @deployment_status.setter
    def deployment_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "deployment_status", value)

    @property
    @pulumi.getter(name="totalArtifacts")
    def total_artifacts(self) -> Optional[pulumi.Input[int]]:
        """
        The total count of the artifacts that were tentatively applied.
        """
        return pulumi.get(self, "total_artifacts")

    @total_artifacts.setter
    def total_artifacts(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "total_artifacts", value)


@pulumi.input_type
class ArtifactInstallPropertiesArgs:
    def __init__(__self__, *,
                 artifact_id: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactParameterPropertiesArgs']]]] = None):
        """
        Properties of an artifact.
        :param pulumi.Input[str] artifact_id: The artifact's identifier.
        :param pulumi.Input[Sequence[pulumi.Input['ArtifactParameterPropertiesArgs']]] parameters: The parameters of the artifact.
        """
        if artifact_id is not None:
            pulumi.set(__self__, "artifact_id", artifact_id)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)

    @property
    @pulumi.getter(name="artifactId")
    def artifact_id(self) -> Optional[pulumi.Input[str]]:
        """
        The artifact's identifier.
        """
        return pulumi.get(self, "artifact_id")

    @artifact_id.setter
    def artifact_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "artifact_id", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactParameterPropertiesArgs']]]]:
        """
        The parameters of the artifact.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactParameterPropertiesArgs']]]]):
        pulumi.set(self, "parameters", value)


@pulumi.input_type
class ArtifactParameterPropertiesArgs:
    def __init__(__self__, *,
                 name: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        Properties of an artifact parameter.
        :param pulumi.Input[str] name: The name of the artifact parameter.
        :param pulumi.Input[str] value: The value of the artifact parameter.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the artifact parameter.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        The value of the artifact parameter.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class CustomImagePropertiesCustomArgs:
    def __init__(__self__, *,
                 image_name: Optional[pulumi.Input[str]] = None,
                 sys_prep: Optional[pulumi.Input[bool]] = None):
        """
        Properties for creating a custom image from a VHD.
        :param pulumi.Input[str] image_name: The image name.
        :param pulumi.Input[bool] sys_prep: Indicates whether sysprep has been run on the VHD.
        """
        if image_name is not None:
            pulumi.set(__self__, "image_name", image_name)
        if sys_prep is not None:
            pulumi.set(__self__, "sys_prep", sys_prep)

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> Optional[pulumi.Input[str]]:
        """
        The image name.
        """
        return pulumi.get(self, "image_name")

    @image_name.setter
    def image_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "image_name", value)

    @property
    @pulumi.getter(name="sysPrep")
    def sys_prep(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether sysprep has been run on the VHD.
        """
        return pulumi.get(self, "sys_prep")

    @sys_prep.setter
    def sys_prep(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sys_prep", value)


@pulumi.input_type
class CustomImagePropertiesFromVmArgs:
    def __init__(__self__, *,
                 linux_os_info: Optional[pulumi.Input['LinuxOsInfoArgs']] = None,
                 source_vm_id: Optional[pulumi.Input[str]] = None,
                 sys_prep: Optional[pulumi.Input[bool]] = None,
                 windows_os_info: Optional[pulumi.Input['WindowsOsInfoArgs']] = None):
        """
        Properties for creating a custom image from a virtual machine.
        :param pulumi.Input['LinuxOsInfoArgs'] linux_os_info: The Linux OS information of the VM.
        :param pulumi.Input[str] source_vm_id: The source vm identifier.
        :param pulumi.Input[bool] sys_prep: Indicates whether sysprep has been run on the VHD.
        :param pulumi.Input['WindowsOsInfoArgs'] windows_os_info: The Windows OS information of the VM.
        """
        if linux_os_info is not None:
            pulumi.set(__self__, "linux_os_info", linux_os_info)
        if source_vm_id is not None:
            pulumi.set(__self__, "source_vm_id", source_vm_id)
        if sys_prep is not None:
            pulumi.set(__self__, "sys_prep", sys_prep)
        if windows_os_info is not None:
            pulumi.set(__self__, "windows_os_info", windows_os_info)

    @property
    @pulumi.getter(name="linuxOsInfo")
    def linux_os_info(self) -> Optional[pulumi.Input['LinuxOsInfoArgs']]:
        """
        The Linux OS information of the VM.
        """
        return pulumi.get(self, "linux_os_info")

    @linux_os_info.setter
    def linux_os_info(self, value: Optional[pulumi.Input['LinuxOsInfoArgs']]):
        pulumi.set(self, "linux_os_info", value)

    @property
    @pulumi.getter(name="sourceVmId")
    def source_vm_id(self) -> Optional[pulumi.Input[str]]:
        """
        The source vm identifier.
        """
        return pulumi.get(self, "source_vm_id")

    @source_vm_id.setter
    def source_vm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_vm_id", value)

    @property
    @pulumi.getter(name="sysPrep")
    def sys_prep(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether sysprep has been run on the VHD.
        """
        return pulumi.get(self, "sys_prep")

    @sys_prep.setter
    def sys_prep(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sys_prep", value)

    @property
    @pulumi.getter(name="windowsOsInfo")
    def windows_os_info(self) -> Optional[pulumi.Input['WindowsOsInfoArgs']]:
        """
        The Windows OS information of the VM.
        """
        return pulumi.get(self, "windows_os_info")

    @windows_os_info.setter
    def windows_os_info(self, value: Optional[pulumi.Input['WindowsOsInfoArgs']]):
        pulumi.set(self, "windows_os_info", value)


@pulumi.input_type
class DayDetailsArgs:
    def __init__(__self__, *,
                 time: Optional[pulumi.Input[str]] = None):
        """
        Properties of a daily schedule.
        """
        if time is not None:
            pulumi.set(__self__, "time", time)

    @property
    @pulumi.getter
    def time(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "time")

    @time.setter
    def time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time", value)


@pulumi.input_type
class FormulaPropertiesFromVmArgs:
    def __init__(__self__, *,
                 lab_vm_id: Optional[pulumi.Input[str]] = None):
        """
        Information about a VM from which a formula is to be created.
        :param pulumi.Input[str] lab_vm_id: The identifier of the VM from which a formula is to be created.
        """
        if lab_vm_id is not None:
            pulumi.set(__self__, "lab_vm_id", lab_vm_id)

    @property
    @pulumi.getter(name="labVmId")
    def lab_vm_id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the VM from which a formula is to be created.
        """
        return pulumi.get(self, "lab_vm_id")

    @lab_vm_id.setter
    def lab_vm_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lab_vm_id", value)


@pulumi.input_type
class GalleryImageReferenceArgs:
    def __init__(__self__, *,
                 offer: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[str]] = None):
        """
        The reference information for an Azure Marketplace image.
        :param pulumi.Input[str] offer: The offer of the gallery image.
        :param pulumi.Input[str] os_type: The OS type of the gallery image.
        :param pulumi.Input[str] publisher: The publisher of the gallery image.
        :param pulumi.Input[str] sku: The SKU of the gallery image.
        :param pulumi.Input[str] version: The version of the gallery image.
        """
        if offer is not None:
            pulumi.set(__self__, "offer", offer)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def offer(self) -> Optional[pulumi.Input[str]]:
        """
        The offer of the gallery image.
        """
        return pulumi.get(self, "offer")

    @offer.setter
    def offer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "offer", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        The OS type of the gallery image.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter
    def publisher(self) -> Optional[pulumi.Input[str]]:
        """
        The publisher of the gallery image.
        """
        return pulumi.get(self, "publisher")

    @publisher.setter
    def publisher(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "publisher", value)

    @property
    @pulumi.getter
    def sku(self) -> Optional[pulumi.Input[str]]:
        """
        The SKU of the gallery image.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of the gallery image.
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class HourDetailsArgs:
    def __init__(__self__, *,
                 minute: Optional[pulumi.Input[int]] = None):
        """
        Properties of an hourly schedule.
        :param pulumi.Input[int] minute: Minutes of the hour the schedule will run.
        """
        if minute is not None:
            pulumi.set(__self__, "minute", minute)

    @property
    @pulumi.getter
    def minute(self) -> Optional[pulumi.Input[int]]:
        """
        Minutes of the hour the schedule will run.
        """
        return pulumi.get(self, "minute")

    @minute.setter
    def minute(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "minute", value)


@pulumi.input_type
class LabVirtualMachineArgs:
    def __init__(__self__, *,
                 artifact_deployment_status: Optional[pulumi.Input['ArtifactDeploymentStatusPropertiesArgs']] = None,
                 artifacts: Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactInstallPropertiesArgs']]]] = None,
                 compute_id: Optional[pulumi.Input[str]] = None,
                 created_by_user: Optional[pulumi.Input[str]] = None,
                 created_by_user_id: Optional[pulumi.Input[str]] = None,
                 custom_image_id: Optional[pulumi.Input[str]] = None,
                 disallow_public_ip_address: Optional[pulumi.Input[bool]] = None,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 gallery_image_reference: Optional[pulumi.Input['GalleryImageReferenceArgs']] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 is_authentication_with_ssh_key: Optional[pulumi.Input[bool]] = None,
                 lab_subnet_name: Optional[pulumi.Input[str]] = None,
                 lab_virtual_network_id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 notes: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[str]] = None,
                 owner_object_id: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 size: Optional[pulumi.Input[str]] = None,
                 ssh_key: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        A virtual machine.
        :param pulumi.Input['ArtifactDeploymentStatusPropertiesArgs'] artifact_deployment_status: The artifact deployment status for the virtual machine.
        :param pulumi.Input[Sequence[pulumi.Input['ArtifactInstallPropertiesArgs']]] artifacts: The artifacts to be installed on the virtual machine.
        :param pulumi.Input[str] compute_id: The resource identifier (Microsoft.Compute) of the virtual machine.
        :param pulumi.Input[str] created_by_user: The email address of creator of the virtual machine.
        :param pulumi.Input[str] created_by_user_id: The object identifier of the creator of the virtual machine.
        :param pulumi.Input[str] custom_image_id: The custom image identifier of the virtual machine.
        :param pulumi.Input[bool] disallow_public_ip_address: Indicates whether the virtual machine is to be created without a public IP address.
        :param pulumi.Input[str] fqdn: The fully-qualified domain name of the virtual machine.
        :param pulumi.Input['GalleryImageReferenceArgs'] gallery_image_reference: The Microsoft Azure Marketplace image reference of the virtual machine.
        :param pulumi.Input[str] id: The identifier of the resource.
        :param pulumi.Input[bool] is_authentication_with_ssh_key: A value indicating whether this virtual machine uses an SSH key for authentication.
        :param pulumi.Input[str] lab_subnet_name: The lab subnet name of the virtual machine.
        :param pulumi.Input[str] lab_virtual_network_id: The lab virtual network identifier of the virtual machine.
        :param pulumi.Input[str] location: The location of the resource.
        :param pulumi.Input[str] name: The name of the resource.
        :param pulumi.Input[str] notes: The notes of the virtual machine.
        :param pulumi.Input[str] os_type: The OS type of the virtual machine.
        :param pulumi.Input[str] owner_object_id: The object identifier of the owner of the virtual machine.
        :param pulumi.Input[str] password: The password of the virtual machine administrator.
        :param pulumi.Input[str] provisioning_state: The provisioning status of the resource.
        :param pulumi.Input[str] size: The size of the virtual machine.
        :param pulumi.Input[str] ssh_key: The SSH key of the virtual machine administrator.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The tags of the resource.
        :param pulumi.Input[str] type: The type of the resource.
        :param pulumi.Input[str] user_name: The user name of the virtual machine.
        """
        if artifact_deployment_status is not None:
            pulumi.set(__self__, "artifact_deployment_status", artifact_deployment_status)
        if artifacts is not None:
            pulumi.set(__self__, "artifacts", artifacts)
        if compute_id is not None:
            pulumi.set(__self__, "compute_id", compute_id)
        if created_by_user is not None:
            pulumi.set(__self__, "created_by_user", created_by_user)
        if created_by_user_id is not None:
            pulumi.set(__self__, "created_by_user_id", created_by_user_id)
        if custom_image_id is not None:
            pulumi.set(__self__, "custom_image_id", custom_image_id)
        if disallow_public_ip_address is not None:
            pulumi.set(__self__, "disallow_public_ip_address", disallow_public_ip_address)
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if gallery_image_reference is not None:
            pulumi.set(__self__, "gallery_image_reference", gallery_image_reference)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if is_authentication_with_ssh_key is not None:
            pulumi.set(__self__, "is_authentication_with_ssh_key", is_authentication_with_ssh_key)
        if lab_subnet_name is not None:
            pulumi.set(__self__, "lab_subnet_name", lab_subnet_name)
        if lab_virtual_network_id is not None:
            pulumi.set(__self__, "lab_virtual_network_id", lab_virtual_network_id)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if notes is not None:
            pulumi.set(__self__, "notes", notes)
        if os_type is not None:
            pulumi.set(__self__, "os_type", os_type)
        if owner_object_id is not None:
            pulumi.set(__self__, "owner_object_id", owner_object_id)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if size is not None:
            pulumi.set(__self__, "size", size)
        if ssh_key is not None:
            pulumi.set(__self__, "ssh_key", ssh_key)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter(name="artifactDeploymentStatus")
    def artifact_deployment_status(self) -> Optional[pulumi.Input['ArtifactDeploymentStatusPropertiesArgs']]:
        """
        The artifact deployment status for the virtual machine.
        """
        return pulumi.get(self, "artifact_deployment_status")

    @artifact_deployment_status.setter
    def artifact_deployment_status(self, value: Optional[pulumi.Input['ArtifactDeploymentStatusPropertiesArgs']]):
        pulumi.set(self, "artifact_deployment_status", value)

    @property
    @pulumi.getter
    def artifacts(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactInstallPropertiesArgs']]]]:
        """
        The artifacts to be installed on the virtual machine.
        """
        return pulumi.get(self, "artifacts")

    @artifacts.setter
    def artifacts(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ArtifactInstallPropertiesArgs']]]]):
        pulumi.set(self, "artifacts", value)

    @property
    @pulumi.getter(name="computeId")
    def compute_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource identifier (Microsoft.Compute) of the virtual machine.
        """
        return pulumi.get(self, "compute_id")

    @compute_id.setter
    def compute_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_id", value)

    @property
    @pulumi.getter(name="createdByUser")
    def created_by_user(self) -> Optional[pulumi.Input[str]]:
        """
        The email address of creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user")

    @created_by_user.setter
    def created_by_user(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by_user", value)

    @property
    @pulumi.getter(name="createdByUserId")
    def created_by_user_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object identifier of the creator of the virtual machine.
        """
        return pulumi.get(self, "created_by_user_id")

    @created_by_user_id.setter
    def created_by_user_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_by_user_id", value)

    @property
    @pulumi.getter(name="customImageId")
    def custom_image_id(self) -> Optional[pulumi.Input[str]]:
        """
        The custom image identifier of the virtual machine.
        """
        return pulumi.get(self, "custom_image_id")

    @custom_image_id.setter
    def custom_image_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "custom_image_id", value)

    @property
    @pulumi.getter(name="disallowPublicIpAddress")
    def disallow_public_ip_address(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether the virtual machine is to be created without a public IP address.
        """
        return pulumi.get(self, "disallow_public_ip_address")

    @disallow_public_ip_address.setter
    def disallow_public_ip_address(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "disallow_public_ip_address", value)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        The fully-qualified domain name of the virtual machine.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="galleryImageReference")
    def gallery_image_reference(self) -> Optional[pulumi.Input['GalleryImageReferenceArgs']]:
        """
        The Microsoft Azure Marketplace image reference of the virtual machine.
        """
        return pulumi.get(self, "gallery_image_reference")

    @gallery_image_reference.setter
    def gallery_image_reference(self, value: Optional[pulumi.Input['GalleryImageReferenceArgs']]):
        pulumi.set(self, "gallery_image_reference", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The identifier of the resource.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="isAuthenticationWithSshKey")
    def is_authentication_with_ssh_key(self) -> Optional[pulumi.Input[bool]]:
        """
        A value indicating whether this virtual machine uses an SSH key for authentication.
        """
        return pulumi.get(self, "is_authentication_with_ssh_key")

    @is_authentication_with_ssh_key.setter
    def is_authentication_with_ssh_key(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_authentication_with_ssh_key", value)

    @property
    @pulumi.getter(name="labSubnetName")
    def lab_subnet_name(self) -> Optional[pulumi.Input[str]]:
        """
        The lab subnet name of the virtual machine.
        """
        return pulumi.get(self, "lab_subnet_name")

    @lab_subnet_name.setter
    def lab_subnet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lab_subnet_name", value)

    @property
    @pulumi.getter(name="labVirtualNetworkId")
    def lab_virtual_network_id(self) -> Optional[pulumi.Input[str]]:
        """
        The lab virtual network identifier of the virtual machine.
        """
        return pulumi.get(self, "lab_virtual_network_id")

    @lab_virtual_network_id.setter
    def lab_virtual_network_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lab_virtual_network_id", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The location of the resource.
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def notes(self) -> Optional[pulumi.Input[str]]:
        """
        The notes of the virtual machine.
        """
        return pulumi.get(self, "notes")

    @notes.setter
    def notes(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "notes", value)

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> Optional[pulumi.Input[str]]:
        """
        The OS type of the virtual machine.
        """
        return pulumi.get(self, "os_type")

    @os_type.setter
    def os_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "os_type", value)

    @property
    @pulumi.getter(name="ownerObjectId")
    def owner_object_id(self) -> Optional[pulumi.Input[str]]:
        """
        The object identifier of the owner of the virtual machine.
        """
        return pulumi.get(self, "owner_object_id")

    @owner_object_id.setter
    def owner_object_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "owner_object_id", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        The password of the virtual machine administrator.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input[str]]:
        """
        The provisioning status of the resource.
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter
    def size(self) -> Optional[pulumi.Input[str]]:
        """
        The size of the virtual machine.
        """
        return pulumi.get(self, "size")

    @size.setter
    def size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "size", value)

    @property
    @pulumi.getter(name="sshKey")
    def ssh_key(self) -> Optional[pulumi.Input[str]]:
        """
        The SSH key of the virtual machine administrator.
        """
        return pulumi.get(self, "ssh_key")

    @ssh_key.setter
    def ssh_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ssh_key", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The user name of the virtual machine.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


@pulumi.input_type
class LinuxOsInfoArgs:
    def __init__(__self__, *,
                 linux_os_state: Optional[pulumi.Input[Union[str, 'LinuxOsState']]] = None):
        """
        Information about a Linux OS.
        :param pulumi.Input[Union[str, 'LinuxOsState']] linux_os_state: The state of the Linux OS.
        """
        if linux_os_state is not None:
            pulumi.set(__self__, "linux_os_state", linux_os_state)

    @property
    @pulumi.getter(name="linuxOsState")
    def linux_os_state(self) -> Optional[pulumi.Input[Union[str, 'LinuxOsState']]]:
        """
        The state of the Linux OS.
        """
        return pulumi.get(self, "linux_os_state")

    @linux_os_state.setter
    def linux_os_state(self, value: Optional[pulumi.Input[Union[str, 'LinuxOsState']]]):
        pulumi.set(self, "linux_os_state", value)


@pulumi.input_type
class SubnetOverrideArgs:
    def __init__(__self__, *,
                 lab_subnet_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 use_in_vm_creation_permission: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]] = None,
                 use_public_ip_address_permission: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]] = None):
        """
        Property overrides on a subnet of a virtual network.
        :param pulumi.Input[str] lab_subnet_name: The name given to the subnet within the lab.
        :param pulumi.Input[str] resource_id: The resource identifier of the subnet.
        :param pulumi.Input[Union[str, 'UsagePermissionType']] use_in_vm_creation_permission: Indicates whether this subnet can be used during virtual machine creation.
        :param pulumi.Input[Union[str, 'UsagePermissionType']] use_public_ip_address_permission: Indicates whether public IP addresses can be assigned to virtual machines on this subnet.
        """
        if lab_subnet_name is not None:
            pulumi.set(__self__, "lab_subnet_name", lab_subnet_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if use_in_vm_creation_permission is not None:
            pulumi.set(__self__, "use_in_vm_creation_permission", use_in_vm_creation_permission)
        if use_public_ip_address_permission is not None:
            pulumi.set(__self__, "use_public_ip_address_permission", use_public_ip_address_permission)

    @property
    @pulumi.getter(name="labSubnetName")
    def lab_subnet_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name given to the subnet within the lab.
        """
        return pulumi.get(self, "lab_subnet_name")

    @lab_subnet_name.setter
    def lab_subnet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lab_subnet_name", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        The resource identifier of the subnet.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)

    @property
    @pulumi.getter(name="useInVmCreationPermission")
    def use_in_vm_creation_permission(self) -> Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]:
        """
        Indicates whether this subnet can be used during virtual machine creation.
        """
        return pulumi.get(self, "use_in_vm_creation_permission")

    @use_in_vm_creation_permission.setter
    def use_in_vm_creation_permission(self, value: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]):
        pulumi.set(self, "use_in_vm_creation_permission", value)

    @property
    @pulumi.getter(name="usePublicIpAddressPermission")
    def use_public_ip_address_permission(self) -> Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]:
        """
        Indicates whether public IP addresses can be assigned to virtual machines on this subnet.
        """
        return pulumi.get(self, "use_public_ip_address_permission")

    @use_public_ip_address_permission.setter
    def use_public_ip_address_permission(self, value: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]):
        pulumi.set(self, "use_public_ip_address_permission", value)


@pulumi.input_type
class SubnetArgs:
    def __init__(__self__, *,
                 allow_public_ip: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]] = None,
                 lab_subnet_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        if allow_public_ip is not None:
            pulumi.set(__self__, "allow_public_ip", allow_public_ip)
        if lab_subnet_name is not None:
            pulumi.set(__self__, "lab_subnet_name", lab_subnet_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="allowPublicIp")
    def allow_public_ip(self) -> Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]:
        return pulumi.get(self, "allow_public_ip")

    @allow_public_ip.setter
    def allow_public_ip(self, value: Optional[pulumi.Input[Union[str, 'UsagePermissionType']]]):
        pulumi.set(self, "allow_public_ip", value)

    @property
    @pulumi.getter(name="labSubnetName")
    def lab_subnet_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "lab_subnet_name")

    @lab_subnet_name.setter
    def lab_subnet_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "lab_subnet_name", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class WeekDetailsArgs:
    def __init__(__self__, *,
                 time: Optional[pulumi.Input[str]] = None,
                 weekdays: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Properties of a weekly schedule.
        :param pulumi.Input[str] time: The time of the day.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] weekdays: The days of the week.
        """
        if time is not None:
            pulumi.set(__self__, "time", time)
        if weekdays is not None:
            pulumi.set(__self__, "weekdays", weekdays)

    @property
    @pulumi.getter
    def time(self) -> Optional[pulumi.Input[str]]:
        """
        The time of the day.
        """
        return pulumi.get(self, "time")

    @time.setter
    def time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time", value)

    @property
    @pulumi.getter
    def weekdays(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The days of the week.
        """
        return pulumi.get(self, "weekdays")

    @weekdays.setter
    def weekdays(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "weekdays", value)


@pulumi.input_type
class WindowsOsInfoArgs:
    def __init__(__self__, *,
                 windows_os_state: Optional[pulumi.Input[Union[str, 'WindowsOsState']]] = None):
        """
        Information about a Windows OS.
        :param pulumi.Input[Union[str, 'WindowsOsState']] windows_os_state: The state of the Windows OS.
        """
        if windows_os_state is not None:
            pulumi.set(__self__, "windows_os_state", windows_os_state)

    @property
    @pulumi.getter(name="windowsOsState")
    def windows_os_state(self) -> Optional[pulumi.Input[Union[str, 'WindowsOsState']]]:
        """
        The state of the Windows OS.
        """
        return pulumi.get(self, "windows_os_state")

    @windows_os_state.setter
    def windows_os_state(self, value: Optional[pulumi.Input[Union[str, 'WindowsOsState']]]):
        pulumi.set(self, "windows_os_state", value)


