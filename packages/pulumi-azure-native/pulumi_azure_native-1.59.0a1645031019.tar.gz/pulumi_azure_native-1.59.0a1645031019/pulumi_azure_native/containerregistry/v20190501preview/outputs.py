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
    'ActiveDirectoryObjectResponse',
    'SystemDataResponse',
    'TokenCertificateResponse',
    'TokenCredentialsPropertiesResponse',
    'TokenPasswordResponse',
]

@pulumi.output_type
class ActiveDirectoryObjectResponse(dict):
    """
    The Active Directory Object that will be used for authenticating the token of a container registry.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "objectId":
            suggest = "object_id"
        elif key == "tenantId":
            suggest = "tenant_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ActiveDirectoryObjectResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ActiveDirectoryObjectResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ActiveDirectoryObjectResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 object_id: Optional[str] = None,
                 tenant_id: Optional[str] = None):
        """
        The Active Directory Object that will be used for authenticating the token of a container registry.
        :param str object_id: The user/group/application object ID for Active Directory Object that will be used for authenticating the token of a container registry.
        :param str tenant_id: The tenant ID of user/group/application object Active Directory Object that will be used for authenticating the token of a container registry.
        """
        if object_id is not None:
            pulumi.set(__self__, "object_id", object_id)
        if tenant_id is not None:
            pulumi.set(__self__, "tenant_id", tenant_id)

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> Optional[str]:
        """
        The user/group/application object ID for Active Directory Object that will be used for authenticating the token of a container registry.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> Optional[str]:
        """
        The tenant ID of user/group/application object Active Directory Object that will be used for authenticating the token of a container registry.
        """
        return pulumi.get(self, "tenant_id")


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
        :param str last_modified_at: The timestamp of resource modification (UTC).
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
        The timestamp of resource modification (UTC).
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
class TokenCertificateResponse(dict):
    """
    The properties of a certificate used for authenticating a token.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "encodedPemCertificate":
            suggest = "encoded_pem_certificate"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TokenCertificateResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TokenCertificateResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TokenCertificateResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 encoded_pem_certificate: Optional[str] = None,
                 expiry: Optional[str] = None,
                 name: Optional[str] = None,
                 thumbprint: Optional[str] = None):
        """
        The properties of a certificate used for authenticating a token.
        :param str encoded_pem_certificate: Base 64 encoded string of the public certificate1 in PEM format that will be used for authenticating the token.
        :param str expiry: The expiry datetime of the certificate.
        :param str thumbprint: The thumbprint of the certificate.
        """
        if encoded_pem_certificate is not None:
            pulumi.set(__self__, "encoded_pem_certificate", encoded_pem_certificate)
        if expiry is not None:
            pulumi.set(__self__, "expiry", expiry)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)

    @property
    @pulumi.getter(name="encodedPemCertificate")
    def encoded_pem_certificate(self) -> Optional[str]:
        """
        Base 64 encoded string of the public certificate1 in PEM format that will be used for authenticating the token.
        """
        return pulumi.get(self, "encoded_pem_certificate")

    @property
    @pulumi.getter
    def expiry(self) -> Optional[str]:
        """
        The expiry datetime of the certificate.
        """
        return pulumi.get(self, "expiry")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[str]:
        """
        The thumbprint of the certificate.
        """
        return pulumi.get(self, "thumbprint")


@pulumi.output_type
class TokenCredentialsPropertiesResponse(dict):
    """
    The properties of the credentials that can be used for authenticating the token.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "activeDirectoryObject":
            suggest = "active_directory_object"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TokenCredentialsPropertiesResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TokenCredentialsPropertiesResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TokenCredentialsPropertiesResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 active_directory_object: Optional['outputs.ActiveDirectoryObjectResponse'] = None,
                 certificates: Optional[Sequence['outputs.TokenCertificateResponse']] = None,
                 passwords: Optional[Sequence['outputs.TokenPasswordResponse']] = None):
        """
        The properties of the credentials that can be used for authenticating the token.
        :param 'ActiveDirectoryObjectResponse' active_directory_object: The Active Directory Object that will be used for authenticating the token of a container registry.
        """
        if active_directory_object is not None:
            pulumi.set(__self__, "active_directory_object", active_directory_object)
        if certificates is not None:
            pulumi.set(__self__, "certificates", certificates)
        if passwords is not None:
            pulumi.set(__self__, "passwords", passwords)

    @property
    @pulumi.getter(name="activeDirectoryObject")
    def active_directory_object(self) -> Optional['outputs.ActiveDirectoryObjectResponse']:
        """
        The Active Directory Object that will be used for authenticating the token of a container registry.
        """
        return pulumi.get(self, "active_directory_object")

    @property
    @pulumi.getter
    def certificates(self) -> Optional[Sequence['outputs.TokenCertificateResponse']]:
        return pulumi.get(self, "certificates")

    @property
    @pulumi.getter
    def passwords(self) -> Optional[Sequence['outputs.TokenPasswordResponse']]:
        return pulumi.get(self, "passwords")


@pulumi.output_type
class TokenPasswordResponse(dict):
    """
    The password that will be used for authenticating the token of a container registry.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "creationTime":
            suggest = "creation_time"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TokenPasswordResponse. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TokenPasswordResponse.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TokenPasswordResponse.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 value: str,
                 creation_time: Optional[str] = None,
                 expiry: Optional[str] = None,
                 name: Optional[str] = None):
        """
        The password that will be used for authenticating the token of a container registry.
        :param str value: The password value.
        :param str creation_time: The creation datetime of the password.
        :param str expiry: The expiry datetime of the password.
        :param str name: The password name "password1" or "password2"
        """
        pulumi.set(__self__, "value", value)
        if creation_time is not None:
            pulumi.set(__self__, "creation_time", creation_time)
        if expiry is not None:
            pulumi.set(__self__, "expiry", expiry)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The password value.
        """
        return pulumi.get(self, "value")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> Optional[str]:
        """
        The creation datetime of the password.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def expiry(self) -> Optional[str]:
        """
        The expiry datetime of the password.
        """
        return pulumi.get(self, "expiry")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The password name "password1" or "password2"
        """
        return pulumi.get(self, "name")


