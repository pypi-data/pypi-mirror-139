# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from .. import _utilities
import typing
# Export this package's modules as members:
from ._enums import *
from .configuration_store import *
from .get_configuration_store import *
from .get_key_value import *
from .get_private_endpoint_connection import *
from .key_value import *
from .list_configuration_store_key_value import *
from .list_configuration_store_keys import *
from .private_endpoint_connection import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_azure_native.appconfiguration.v20190201preview as __v20190201preview
    v20190201preview = __v20190201preview
    import pulumi_azure_native.appconfiguration.v20191001 as __v20191001
    v20191001 = __v20191001
    import pulumi_azure_native.appconfiguration.v20191101preview as __v20191101preview
    v20191101preview = __v20191101preview
    import pulumi_azure_native.appconfiguration.v20200601 as __v20200601
    v20200601 = __v20200601
    import pulumi_azure_native.appconfiguration.v20200701preview as __v20200701preview
    v20200701preview = __v20200701preview
    import pulumi_azure_native.appconfiguration.v20210301preview as __v20210301preview
    v20210301preview = __v20210301preview
    import pulumi_azure_native.appconfiguration.v20211001preview as __v20211001preview
    v20211001preview = __v20211001preview
else:
    v20190201preview = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20190201preview')
    v20191001 = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20191001')
    v20191101preview = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20191101preview')
    v20200601 = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20200601')
    v20200701preview = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20200701preview')
    v20210301preview = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20210301preview')
    v20211001preview = _utilities.lazy_import('pulumi_azure_native.appconfiguration.v20211001preview')

