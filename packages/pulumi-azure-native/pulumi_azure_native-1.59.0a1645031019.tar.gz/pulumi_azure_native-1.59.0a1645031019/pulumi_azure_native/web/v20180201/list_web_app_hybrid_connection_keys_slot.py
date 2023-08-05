# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from ... import _utilities

__all__ = [
    'ListWebAppHybridConnectionKeysSlotResult',
    'AwaitableListWebAppHybridConnectionKeysSlotResult',
    'list_web_app_hybrid_connection_keys_slot',
    'list_web_app_hybrid_connection_keys_slot_output',
]

@pulumi.output_type
class ListWebAppHybridConnectionKeysSlotResult:
    """
    Hybrid Connection key contract. This has the send key name and value for a Hybrid Connection.
    """
    def __init__(__self__, id=None, kind=None, name=None, send_key_name=None, send_key_value=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kind and not isinstance(kind, str):
            raise TypeError("Expected argument 'kind' to be a str")
        pulumi.set(__self__, "kind", kind)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if send_key_name and not isinstance(send_key_name, str):
            raise TypeError("Expected argument 'send_key_name' to be a str")
        pulumi.set(__self__, "send_key_name", send_key_name)
        if send_key_value and not isinstance(send_key_value, str):
            raise TypeError("Expected argument 'send_key_value' to be a str")
        pulumi.set(__self__, "send_key_value", send_key_value)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Resource Id.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def kind(self) -> Optional[str]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sendKeyName")
    def send_key_name(self) -> str:
        """
        The name of the send key.
        """
        return pulumi.get(self, "send_key_name")

    @property
    @pulumi.getter(name="sendKeyValue")
    def send_key_value(self) -> str:
        """
        The value of the send key.
        """
        return pulumi.get(self, "send_key_value")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Resource type.
        """
        return pulumi.get(self, "type")


class AwaitableListWebAppHybridConnectionKeysSlotResult(ListWebAppHybridConnectionKeysSlotResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListWebAppHybridConnectionKeysSlotResult(
            id=self.id,
            kind=self.kind,
            name=self.name,
            send_key_name=self.send_key_name,
            send_key_value=self.send_key_value,
            type=self.type)


def list_web_app_hybrid_connection_keys_slot(name: Optional[str] = None,
                                             namespace_name: Optional[str] = None,
                                             relay_name: Optional[str] = None,
                                             resource_group_name: Optional[str] = None,
                                             slot: Optional[str] = None,
                                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListWebAppHybridConnectionKeysSlotResult:
    """
    Hybrid Connection key contract. This has the send key name and value for a Hybrid Connection.


    :param str name: The name of the web app.
    :param str namespace_name: The namespace for this hybrid connection.
    :param str relay_name: The relay name for this hybrid connection.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: The name of the slot for the web app.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['namespaceName'] = namespace_name
    __args__['relayName'] = relay_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['slot'] = slot
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:web/v20180201:listWebAppHybridConnectionKeysSlot', __args__, opts=opts, typ=ListWebAppHybridConnectionKeysSlotResult).value

    return AwaitableListWebAppHybridConnectionKeysSlotResult(
        id=__ret__.id,
        kind=__ret__.kind,
        name=__ret__.name,
        send_key_name=__ret__.send_key_name,
        send_key_value=__ret__.send_key_value,
        type=__ret__.type)


@_utilities.lift_output_func(list_web_app_hybrid_connection_keys_slot)
def list_web_app_hybrid_connection_keys_slot_output(name: Optional[pulumi.Input[str]] = None,
                                                    namespace_name: Optional[pulumi.Input[str]] = None,
                                                    relay_name: Optional[pulumi.Input[str]] = None,
                                                    resource_group_name: Optional[pulumi.Input[str]] = None,
                                                    slot: Optional[pulumi.Input[str]] = None,
                                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[ListWebAppHybridConnectionKeysSlotResult]:
    """
    Hybrid Connection key contract. This has the send key name and value for a Hybrid Connection.


    :param str name: The name of the web app.
    :param str namespace_name: The namespace for this hybrid connection.
    :param str relay_name: The relay name for this hybrid connection.
    :param str resource_group_name: Name of the resource group to which the resource belongs.
    :param str slot: The name of the slot for the web app.
    """
    ...
