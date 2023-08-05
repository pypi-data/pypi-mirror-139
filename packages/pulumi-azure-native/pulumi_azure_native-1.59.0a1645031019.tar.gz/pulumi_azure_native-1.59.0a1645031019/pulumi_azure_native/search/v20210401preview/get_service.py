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
    'GetServiceResult',
    'AwaitableGetServiceResult',
    'get_service',
    'get_service_output',
]

@pulumi.output_type
class GetServiceResult:
    """
    Describes an Azure Cognitive Search service and its current state.
    """
    def __init__(__self__, auth_options=None, disable_local_auth=None, disabled_data_exfiltration_options=None, e_tag=None, encryption_with_cmk=None, hosting_mode=None, id=None, identity=None, location=None, name=None, network_rule_set=None, partition_count=None, private_endpoint_connections=None, provisioning_state=None, public_network_access=None, replica_count=None, semantic_search=None, shared_private_link_resources=None, sku=None, status=None, status_details=None, tags=None, type=None):
        if auth_options and not isinstance(auth_options, dict):
            raise TypeError("Expected argument 'auth_options' to be a dict")
        pulumi.set(__self__, "auth_options", auth_options)
        if disable_local_auth and not isinstance(disable_local_auth, bool):
            raise TypeError("Expected argument 'disable_local_auth' to be a bool")
        pulumi.set(__self__, "disable_local_auth", disable_local_auth)
        if disabled_data_exfiltration_options and not isinstance(disabled_data_exfiltration_options, list):
            raise TypeError("Expected argument 'disabled_data_exfiltration_options' to be a list")
        pulumi.set(__self__, "disabled_data_exfiltration_options", disabled_data_exfiltration_options)
        if e_tag and not isinstance(e_tag, str):
            raise TypeError("Expected argument 'e_tag' to be a str")
        pulumi.set(__self__, "e_tag", e_tag)
        if encryption_with_cmk and not isinstance(encryption_with_cmk, dict):
            raise TypeError("Expected argument 'encryption_with_cmk' to be a dict")
        pulumi.set(__self__, "encryption_with_cmk", encryption_with_cmk)
        if hosting_mode and not isinstance(hosting_mode, str):
            raise TypeError("Expected argument 'hosting_mode' to be a str")
        pulumi.set(__self__, "hosting_mode", hosting_mode)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if identity and not isinstance(identity, dict):
            raise TypeError("Expected argument 'identity' to be a dict")
        pulumi.set(__self__, "identity", identity)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_rule_set and not isinstance(network_rule_set, dict):
            raise TypeError("Expected argument 'network_rule_set' to be a dict")
        pulumi.set(__self__, "network_rule_set", network_rule_set)
        if partition_count and not isinstance(partition_count, int):
            raise TypeError("Expected argument 'partition_count' to be a int")
        pulumi.set(__self__, "partition_count", partition_count)
        if private_endpoint_connections and not isinstance(private_endpoint_connections, list):
            raise TypeError("Expected argument 'private_endpoint_connections' to be a list")
        pulumi.set(__self__, "private_endpoint_connections", private_endpoint_connections)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if public_network_access and not isinstance(public_network_access, str):
            raise TypeError("Expected argument 'public_network_access' to be a str")
        pulumi.set(__self__, "public_network_access", public_network_access)
        if replica_count and not isinstance(replica_count, int):
            raise TypeError("Expected argument 'replica_count' to be a int")
        pulumi.set(__self__, "replica_count", replica_count)
        if semantic_search and not isinstance(semantic_search, str):
            raise TypeError("Expected argument 'semantic_search' to be a str")
        pulumi.set(__self__, "semantic_search", semantic_search)
        if shared_private_link_resources and not isinstance(shared_private_link_resources, list):
            raise TypeError("Expected argument 'shared_private_link_resources' to be a list")
        pulumi.set(__self__, "shared_private_link_resources", shared_private_link_resources)
        if sku and not isinstance(sku, dict):
            raise TypeError("Expected argument 'sku' to be a dict")
        pulumi.set(__self__, "sku", sku)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if status_details and not isinstance(status_details, str):
            raise TypeError("Expected argument 'status_details' to be a str")
        pulumi.set(__self__, "status_details", status_details)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter(name="authOptions")
    def auth_options(self) -> Optional['outputs.DataPlaneAuthOptionsResponse']:
        """
        Defines the options for how the data plane API of a search service authenticates requests. This cannot be set if 'disableLocalAuth' is set to true.
        """
        return pulumi.get(self, "auth_options")

    @property
    @pulumi.getter(name="disableLocalAuth")
    def disable_local_auth(self) -> Optional[bool]:
        """
        When set to true, calls to the search service will not be permitted to utilize API keys for authentication. This cannot be set to true if 'dataPlaneAuthOptions' are defined.
        """
        return pulumi.get(self, "disable_local_auth")

    @property
    @pulumi.getter(name="disabledDataExfiltrationOptions")
    def disabled_data_exfiltration_options(self) -> Optional[Sequence[str]]:
        """
        A list of data exfiltration scenarios that are explicitly disallowed for the search service. Currently, the only supported value is 'All' to disable all possible data export scenarios with more fine grained controls planned for the future.
        """
        return pulumi.get(self, "disabled_data_exfiltration_options")

    @property
    @pulumi.getter(name="eTag")
    def e_tag(self) -> str:
        """
        A system generated property representing the service's etag that can be for optimistic concurrency control during updates.
        """
        return pulumi.get(self, "e_tag")

    @property
    @pulumi.getter(name="encryptionWithCmk")
    def encryption_with_cmk(self) -> Optional['outputs.EncryptionWithCmkResponse']:
        """
        Specifies any policy regarding encryption of resources (such as indexes) using customer manager keys within a search service.
        """
        return pulumi.get(self, "encryption_with_cmk")

    @property
    @pulumi.getter(name="hostingMode")
    def hosting_mode(self) -> Optional[str]:
        """
        Applicable only for the standard3 SKU. You can set this property to enable up to 3 high density partitions that allow up to 1000 indexes, which is much higher than the maximum indexes allowed for any other SKU. For the standard3 SKU, the value is either 'default' or 'highDensity'. For all other SKUs, this value must be 'default'.
        """
        return pulumi.get(self, "hosting_mode")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Fully qualified resource ID for the resource. Ex - /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProviderNamespace}/{resourceType}/{resourceName}
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def identity(self) -> Optional['outputs.IdentityResponse']:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkRuleSet")
    def network_rule_set(self) -> Optional['outputs.NetworkRuleSetResponse']:
        """
        Network specific rules that determine how the Azure Cognitive Search service may be reached.
        """
        return pulumi.get(self, "network_rule_set")

    @property
    @pulumi.getter(name="partitionCount")
    def partition_count(self) -> Optional[int]:
        """
        The number of partitions in the search service; if specified, it can be 1, 2, 3, 4, 6, or 12. Values greater than 1 are only valid for standard SKUs. For 'standard3' services with hostingMode set to 'highDensity', the allowed values are between 1 and 3.
        """
        return pulumi.get(self, "partition_count")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> Sequence['outputs.PrivateEndpointConnectionResponse']:
        """
        The list of private endpoint connections to the Azure Cognitive Search service.
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The state of the last provisioning operation performed on the search service. Provisioning is an intermediate state that occurs while service capacity is being established. After capacity is set up, provisioningState changes to either 'succeeded' or 'failed'. Client applications can poll provisioning status (the recommended polling interval is from 30 seconds to one minute) by using the Get Search Service operation to see when an operation is completed. If you are using the free service, this value tends to come back as 'succeeded' directly in the call to Create search service. This is because the free service uses capacity that is already set up.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[str]:
        """
        This value can be set to 'enabled' to avoid breaking changes on existing customer resources and templates. If set to 'disabled', traffic over public interface is not allowed, and private endpoint connections would be the exclusive access method.
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="replicaCount")
    def replica_count(self) -> Optional[int]:
        """
        The number of replicas in the search service. If specified, it must be a value between 1 and 12 inclusive for standard SKUs or between 1 and 3 inclusive for basic SKU.
        """
        return pulumi.get(self, "replica_count")

    @property
    @pulumi.getter(name="semanticSearch")
    def semantic_search(self) -> Optional[str]:
        """
        Sets options that control the availability of semantic search. This configuration is only possible for certain Azure Cognitive Search SKUs in certain locations.
        """
        return pulumi.get(self, "semantic_search")

    @property
    @pulumi.getter(name="sharedPrivateLinkResources")
    def shared_private_link_resources(self) -> Sequence['outputs.SharedPrivateLinkResourceResponse']:
        """
        The list of shared private link resources managed by the Azure Cognitive Search service.
        """
        return pulumi.get(self, "shared_private_link_resources")

    @property
    @pulumi.getter
    def sku(self) -> Optional['outputs.SkuResponse']:
        """
        The SKU of the Search Service, which determines price tier and capacity limits. This property is required when creating a new Search Service.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        The status of the search service. Possible values include: 'running': The search service is running and no provisioning operations are underway. 'provisioning': The search service is being provisioned or scaled up or down. 'deleting': The search service is being deleted. 'degraded': The search service is degraded. This can occur when the underlying search units are not healthy. The search service is most likely operational, but performance might be slow and some requests might be dropped. 'disabled': The search service is disabled. In this state, the service will reject all API requests. 'error': The search service is in an error state. 'stopped': The search service is in a subscription that's disabled. If your service is in the degraded, disabled, or error states, it means the Azure Cognitive Search team is actively investigating the underlying issue. Dedicated services in these states are still chargeable based on the number of search units provisioned.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> str:
        """
        The details of the search service status.
        """
        return pulumi.get(self, "status_details")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")


class AwaitableGetServiceResult(GetServiceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceResult(
            auth_options=self.auth_options,
            disable_local_auth=self.disable_local_auth,
            disabled_data_exfiltration_options=self.disabled_data_exfiltration_options,
            e_tag=self.e_tag,
            encryption_with_cmk=self.encryption_with_cmk,
            hosting_mode=self.hosting_mode,
            id=self.id,
            identity=self.identity,
            location=self.location,
            name=self.name,
            network_rule_set=self.network_rule_set,
            partition_count=self.partition_count,
            private_endpoint_connections=self.private_endpoint_connections,
            provisioning_state=self.provisioning_state,
            public_network_access=self.public_network_access,
            replica_count=self.replica_count,
            semantic_search=self.semantic_search,
            shared_private_link_resources=self.shared_private_link_resources,
            sku=self.sku,
            status=self.status,
            status_details=self.status_details,
            tags=self.tags,
            type=self.type)


def get_service(resource_group_name: Optional[str] = None,
                search_service_name: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceResult:
    """
    Describes an Azure Cognitive Search service and its current state.


    :param str resource_group_name: The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str search_service_name: The name of the Azure Cognitive Search service associated with the specified resource group.
    """
    __args__ = dict()
    __args__['resourceGroupName'] = resource_group_name
    __args__['searchServiceName'] = search_service_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:search/v20210401preview:getService', __args__, opts=opts, typ=GetServiceResult).value

    return AwaitableGetServiceResult(
        auth_options=__ret__.auth_options,
        disable_local_auth=__ret__.disable_local_auth,
        disabled_data_exfiltration_options=__ret__.disabled_data_exfiltration_options,
        e_tag=__ret__.e_tag,
        encryption_with_cmk=__ret__.encryption_with_cmk,
        hosting_mode=__ret__.hosting_mode,
        id=__ret__.id,
        identity=__ret__.identity,
        location=__ret__.location,
        name=__ret__.name,
        network_rule_set=__ret__.network_rule_set,
        partition_count=__ret__.partition_count,
        private_endpoint_connections=__ret__.private_endpoint_connections,
        provisioning_state=__ret__.provisioning_state,
        public_network_access=__ret__.public_network_access,
        replica_count=__ret__.replica_count,
        semantic_search=__ret__.semantic_search,
        shared_private_link_resources=__ret__.shared_private_link_resources,
        sku=__ret__.sku,
        status=__ret__.status,
        status_details=__ret__.status_details,
        tags=__ret__.tags,
        type=__ret__.type)


@_utilities.lift_output_func(get_service)
def get_service_output(resource_group_name: Optional[pulumi.Input[str]] = None,
                       search_service_name: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetServiceResult]:
    """
    Describes an Azure Cognitive Search service and its current state.


    :param str resource_group_name: The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
    :param str search_service_name: The name of the Azure Cognitive Search service associated with the specified resource group.
    """
    ...
