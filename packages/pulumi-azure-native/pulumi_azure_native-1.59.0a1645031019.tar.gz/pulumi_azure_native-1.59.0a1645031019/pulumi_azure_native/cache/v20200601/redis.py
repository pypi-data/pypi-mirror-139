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

__all__ = ['RedisArgs', 'Redis']

@pulumi.input_type
class RedisArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 sku: pulumi.Input['SkuArgs'],
                 enable_non_ssl_port: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 minimum_tls_version: Optional[pulumi.Input[Union[str, 'TlsVersion']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 redis_configuration: Optional[pulumi.Input['RedisCommonPropertiesRedisConfigurationArgs']] = None,
                 replicas_per_master: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 static_ip: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tenant_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Redis resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input['SkuArgs'] sku: The SKU of the Redis cache to deploy.
        :param pulumi.Input[bool] enable_non_ssl_port: Specifies whether the non-ssl Redis server port (6379) is enabled.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'TlsVersion']] minimum_tls_version: Optional: requires clients to use a specified TLS version (or higher) to connect (e,g, '1.0', '1.1', '1.2')
        :param pulumi.Input[str] name: The name of the Redis cache.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public endpoint access is allowed for this cache.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'. If 'Disabled', private endpoints are the exclusive access method. Default value is 'Enabled'
        :param pulumi.Input['RedisCommonPropertiesRedisConfigurationArgs'] redis_configuration: All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
        :param pulumi.Input[int] replicas_per_master: The number of replicas to be created per master.
        :param pulumi.Input[int] shard_count: The number of shards to be created on a Premium Cluster Cache.
        :param pulumi.Input[str] static_ip: Static IP address. Optionally, may be specified when deploying a Redis cache inside an existing Azure Virtual Network; auto assigned by default.
        :param pulumi.Input[str] subnet_id: The full resource ID of a subnet in a virtual network to deploy the Redis cache in. Example format: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/Microsoft.{Network|ClassicNetwork}/VirtualNetworks/vnet1/subnets/subnet1
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tenant_settings: A dictionary of tenant settings
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: A list of availability zones denoting where the resource needs to come from.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        pulumi.set(__self__, "sku", sku)
        if enable_non_ssl_port is None:
            enable_non_ssl_port = False
        if enable_non_ssl_port is not None:
            pulumi.set(__self__, "enable_non_ssl_port", enable_non_ssl_port)
        if location is not None:
            pulumi.set(__self__, "location", location)
        if minimum_tls_version is not None:
            pulumi.set(__self__, "minimum_tls_version", minimum_tls_version)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if public_network_access is None:
            public_network_access = 'Enabled'
        if public_network_access is not None:
            pulumi.set(__self__, "public_network_access", public_network_access)
        if redis_configuration is not None:
            pulumi.set(__self__, "redis_configuration", redis_configuration)
        if replicas_per_master is not None:
            pulumi.set(__self__, "replicas_per_master", replicas_per_master)
        if shard_count is not None:
            pulumi.set(__self__, "shard_count", shard_count)
        if static_ip is not None:
            pulumi.set(__self__, "static_ip", static_ip)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tenant_settings is not None:
            pulumi.set(__self__, "tenant_settings", tenant_settings)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

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
    @pulumi.getter
    def sku(self) -> pulumi.Input['SkuArgs']:
        """
        The SKU of the Redis cache to deploy.
        """
        return pulumi.get(self, "sku")

    @sku.setter
    def sku(self, value: pulumi.Input['SkuArgs']):
        pulumi.set(self, "sku", value)

    @property
    @pulumi.getter(name="enableNonSslPort")
    def enable_non_ssl_port(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the non-ssl Redis server port (6379) is enabled.
        """
        return pulumi.get(self, "enable_non_ssl_port")

    @enable_non_ssl_port.setter
    def enable_non_ssl_port(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_non_ssl_port", value)

    @property
    @pulumi.getter
    def location(self) -> Optional[pulumi.Input[str]]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter(name="minimumTlsVersion")
    def minimum_tls_version(self) -> Optional[pulumi.Input[Union[str, 'TlsVersion']]]:
        """
        Optional: requires clients to use a specified TLS version (or higher) to connect (e,g, '1.0', '1.1', '1.2')
        """
        return pulumi.get(self, "minimum_tls_version")

    @minimum_tls_version.setter
    def minimum_tls_version(self, value: Optional[pulumi.Input[Union[str, 'TlsVersion']]]):
        pulumi.set(self, "minimum_tls_version", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Redis cache.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]:
        """
        Whether or not public endpoint access is allowed for this cache.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'. If 'Disabled', private endpoints are the exclusive access method. Default value is 'Enabled'
        """
        return pulumi.get(self, "public_network_access")

    @public_network_access.setter
    def public_network_access(self, value: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]]):
        pulumi.set(self, "public_network_access", value)

    @property
    @pulumi.getter(name="redisConfiguration")
    def redis_configuration(self) -> Optional[pulumi.Input['RedisCommonPropertiesRedisConfigurationArgs']]:
        """
        All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
        """
        return pulumi.get(self, "redis_configuration")

    @redis_configuration.setter
    def redis_configuration(self, value: Optional[pulumi.Input['RedisCommonPropertiesRedisConfigurationArgs']]):
        pulumi.set(self, "redis_configuration", value)

    @property
    @pulumi.getter(name="replicasPerMaster")
    def replicas_per_master(self) -> Optional[pulumi.Input[int]]:
        """
        The number of replicas to be created per master.
        """
        return pulumi.get(self, "replicas_per_master")

    @replicas_per_master.setter
    def replicas_per_master(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "replicas_per_master", value)

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shards to be created on a Premium Cluster Cache.
        """
        return pulumi.get(self, "shard_count")

    @shard_count.setter
    def shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "shard_count", value)

    @property
    @pulumi.getter(name="staticIP")
    def static_ip(self) -> Optional[pulumi.Input[str]]:
        """
        Static IP address. Optionally, may be specified when deploying a Redis cache inside an existing Azure Virtual Network; auto assigned by default.
        """
        return pulumi.get(self, "static_ip")

    @static_ip.setter
    def static_ip(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "static_ip", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The full resource ID of a subnet in a virtual network to deploy the Redis cache in. Example format: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/Microsoft.{Network|ClassicNetwork}/VirtualNetworks/vnet1/subnets/subnet1
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tenantSettings")
    def tenant_settings(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A dictionary of tenant settings
        """
        return pulumi.get(self, "tenant_settings")

    @tenant_settings.setter
    def tenant_settings(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tenant_settings", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of availability zones denoting where the resource needs to come from.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "zones", value)


class Redis(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_non_ssl_port: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 minimum_tls_version: Optional[pulumi.Input[Union[str, 'TlsVersion']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 redis_configuration: Optional[pulumi.Input[pulumi.InputType['RedisCommonPropertiesRedisConfigurationArgs']]] = None,
                 replicas_per_master: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 static_ip: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tenant_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        A single Redis item in List or Get Operation.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enable_non_ssl_port: Specifies whether the non-ssl Redis server port (6379) is enabled.
        :param pulumi.Input[str] location: The geo-location where the resource lives
        :param pulumi.Input[Union[str, 'TlsVersion']] minimum_tls_version: Optional: requires clients to use a specified TLS version (or higher) to connect (e,g, '1.0', '1.1', '1.2')
        :param pulumi.Input[str] name: The name of the Redis cache.
        :param pulumi.Input[Union[str, 'PublicNetworkAccess']] public_network_access: Whether or not public endpoint access is allowed for this cache.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'. If 'Disabled', private endpoints are the exclusive access method. Default value is 'Enabled'
        :param pulumi.Input[pulumi.InputType['RedisCommonPropertiesRedisConfigurationArgs']] redis_configuration: All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
        :param pulumi.Input[int] replicas_per_master: The number of replicas to be created per master.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[int] shard_count: The number of shards to be created on a Premium Cluster Cache.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The SKU of the Redis cache to deploy.
        :param pulumi.Input[str] static_ip: Static IP address. Optionally, may be specified when deploying a Redis cache inside an existing Azure Virtual Network; auto assigned by default.
        :param pulumi.Input[str] subnet_id: The full resource ID of a subnet in a virtual network to deploy the Redis cache in. Example format: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/Microsoft.{Network|ClassicNetwork}/VirtualNetworks/vnet1/subnets/subnet1
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tenant_settings: A dictionary of tenant settings
        :param pulumi.Input[Sequence[pulumi.Input[str]]] zones: A list of availability zones denoting where the resource needs to come from.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: RedisArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        A single Redis item in List or Get Operation.

        :param str resource_name: The name of the resource.
        :param RedisArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(RedisArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 enable_non_ssl_port: Optional[pulumi.Input[bool]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 minimum_tls_version: Optional[pulumi.Input[Union[str, 'TlsVersion']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'PublicNetworkAccess']]] = None,
                 redis_configuration: Optional[pulumi.Input[pulumi.InputType['RedisCommonPropertiesRedisConfigurationArgs']]] = None,
                 replicas_per_master: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 static_ip: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tenant_settings: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = RedisArgs.__new__(RedisArgs)

            if enable_non_ssl_port is None:
                enable_non_ssl_port = False
            __props__.__dict__["enable_non_ssl_port"] = enable_non_ssl_port
            __props__.__dict__["location"] = location
            __props__.__dict__["minimum_tls_version"] = minimum_tls_version
            __props__.__dict__["name"] = name
            if public_network_access is None:
                public_network_access = 'Enabled'
            __props__.__dict__["public_network_access"] = public_network_access
            __props__.__dict__["redis_configuration"] = redis_configuration
            __props__.__dict__["replicas_per_master"] = replicas_per_master
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["shard_count"] = shard_count
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__.__dict__["sku"] = sku
            __props__.__dict__["static_ip"] = static_ip
            __props__.__dict__["subnet_id"] = subnet_id
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tenant_settings"] = tenant_settings
            __props__.__dict__["zones"] = zones
            __props__.__dict__["access_keys"] = None
            __props__.__dict__["host_name"] = None
            __props__.__dict__["instances"] = None
            __props__.__dict__["linked_servers"] = None
            __props__.__dict__["port"] = None
            __props__.__dict__["private_endpoint_connections"] = None
            __props__.__dict__["provisioning_state"] = None
            __props__.__dict__["redis_version"] = None
            __props__.__dict__["ssl_port"] = None
            __props__.__dict__["type"] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-native:cache:Redis"), pulumi.Alias(type_="azure-native:cache/v20150801:Redis"), pulumi.Alias(type_="azure-native:cache/v20160401:Redis"), pulumi.Alias(type_="azure-native:cache/v20170201:Redis"), pulumi.Alias(type_="azure-native:cache/v20171001:Redis"), pulumi.Alias(type_="azure-native:cache/v20180301:Redis"), pulumi.Alias(type_="azure-native:cache/v20190701:Redis"), pulumi.Alias(type_="azure-native:cache/v20201201:Redis"), pulumi.Alias(type_="azure-native:cache/v20210601:Redis")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Redis, __self__).__init__(
            'azure-native:cache/v20200601:Redis',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Redis':
        """
        Get an existing Redis resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = RedisArgs.__new__(RedisArgs)

        __props__.__dict__["access_keys"] = None
        __props__.__dict__["enable_non_ssl_port"] = None
        __props__.__dict__["host_name"] = None
        __props__.__dict__["instances"] = None
        __props__.__dict__["linked_servers"] = None
        __props__.__dict__["location"] = None
        __props__.__dict__["minimum_tls_version"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["port"] = None
        __props__.__dict__["private_endpoint_connections"] = None
        __props__.__dict__["provisioning_state"] = None
        __props__.__dict__["public_network_access"] = None
        __props__.__dict__["redis_configuration"] = None
        __props__.__dict__["redis_version"] = None
        __props__.__dict__["replicas_per_master"] = None
        __props__.__dict__["shard_count"] = None
        __props__.__dict__["sku"] = None
        __props__.__dict__["ssl_port"] = None
        __props__.__dict__["static_ip"] = None
        __props__.__dict__["subnet_id"] = None
        __props__.__dict__["tags"] = None
        __props__.__dict__["tenant_settings"] = None
        __props__.__dict__["type"] = None
        __props__.__dict__["zones"] = None
        return Redis(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessKeys")
    def access_keys(self) -> pulumi.Output['outputs.RedisAccessKeysResponse']:
        """
        The keys of the Redis cache - not set if this object is not the response to Create or Update redis cache
        """
        return pulumi.get(self, "access_keys")

    @property
    @pulumi.getter(name="enableNonSslPort")
    def enable_non_ssl_port(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the non-ssl Redis server port (6379) is enabled.
        """
        return pulumi.get(self, "enable_non_ssl_port")

    @property
    @pulumi.getter(name="hostName")
    def host_name(self) -> pulumi.Output[str]:
        """
        Redis host name.
        """
        return pulumi.get(self, "host_name")

    @property
    @pulumi.getter
    def instances(self) -> pulumi.Output[Sequence['outputs.RedisInstanceDetailsResponse']]:
        """
        List of the Redis instances associated with the cache
        """
        return pulumi.get(self, "instances")

    @property
    @pulumi.getter(name="linkedServers")
    def linked_servers(self) -> pulumi.Output[Sequence['outputs.RedisLinkedServerResponse']]:
        """
        List of the linked servers associated with the cache
        """
        return pulumi.get(self, "linked_servers")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The geo-location where the resource lives
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="minimumTlsVersion")
    def minimum_tls_version(self) -> pulumi.Output[Optional[str]]:
        """
        Optional: requires clients to use a specified TLS version (or higher) to connect (e,g, '1.0', '1.1', '1.2')
        """
        return pulumi.get(self, "minimum_tls_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def port(self) -> pulumi.Output[int]:
        """
        Redis non-SSL port.
        """
        return pulumi.get(self, "port")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.PrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connection associated with the specified redis cache
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Redis instance provisioning status.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not public endpoint access is allowed for this cache.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'. If 'Disabled', private endpoints are the exclusive access method. Default value is 'Enabled'
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter(name="redisConfiguration")
    def redis_configuration(self) -> pulumi.Output[Optional['outputs.RedisCommonPropertiesResponseRedisConfiguration']]:
        """
        All Redis Settings. Few possible keys: rdb-backup-enabled,rdb-storage-connection-string,rdb-backup-frequency,maxmemory-delta,maxmemory-policy,notify-keyspace-events,maxmemory-samples,slowlog-log-slower-than,slowlog-max-len,list-max-ziplist-entries,list-max-ziplist-value,hash-max-ziplist-entries,hash-max-ziplist-value,set-max-intset-entries,zset-max-ziplist-entries,zset-max-ziplist-value etc.
        """
        return pulumi.get(self, "redis_configuration")

    @property
    @pulumi.getter(name="redisVersion")
    def redis_version(self) -> pulumi.Output[str]:
        """
        Redis version.
        """
        return pulumi.get(self, "redis_version")

    @property
    @pulumi.getter(name="replicasPerMaster")
    def replicas_per_master(self) -> pulumi.Output[Optional[int]]:
        """
        The number of replicas to be created per master.
        """
        return pulumi.get(self, "replicas_per_master")

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of shards to be created on a Premium Cluster Cache.
        """
        return pulumi.get(self, "shard_count")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        The SKU of the Redis cache to deploy.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="sslPort")
    def ssl_port(self) -> pulumi.Output[int]:
        """
        Redis SSL port.
        """
        return pulumi.get(self, "ssl_port")

    @property
    @pulumi.getter(name="staticIP")
    def static_ip(self) -> pulumi.Output[Optional[str]]:
        """
        Static IP address. Optionally, may be specified when deploying a Redis cache inside an existing Azure Virtual Network; auto assigned by default.
        """
        return pulumi.get(self, "static_ip")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        The full resource ID of a subnet in a virtual network to deploy the Redis cache in. Example format: /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/Microsoft.{Network|ClassicNetwork}/VirtualNetworks/vnet1/subnets/subnet1
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tenantSettings")
    def tenant_settings(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A dictionary of tenant settings
        """
        return pulumi.get(self, "tenant_settings")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def zones(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        A list of availability zones denoting where the resource needs to come from.
        """
        return pulumi.get(self, "zones")

