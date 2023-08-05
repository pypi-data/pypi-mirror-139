# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'Access',
    'ApplicationGatewayCookieBasedAffinity',
    'ApplicationGatewayCustomErrorStatusCode',
    'ApplicationGatewayFirewallMode',
    'ApplicationGatewayProtocol',
    'ApplicationGatewayRedirectType',
    'ApplicationGatewayRequestRoutingRuleType',
    'ApplicationGatewaySkuName',
    'ApplicationGatewaySslCipherSuite',
    'ApplicationGatewaySslPolicyName',
    'ApplicationGatewaySslPolicyType',
    'ApplicationGatewaySslProtocol',
    'ApplicationGatewayTier',
    'AuthorizationUseStatus',
    'AzureFirewallApplicationRuleProtocolType',
    'AzureFirewallNatRCActionType',
    'AzureFirewallNetworkRuleProtocol',
    'AzureFirewallRCActionType',
    'AzureFirewallThreatIntelMode',
    'DdosCustomPolicyProtocol',
    'DdosCustomPolicyTriggerSensitivityOverride',
    'DdosSettingsProtectionCoverage',
    'DhGroup',
    'ExpressRouteCircuitPeeringAdvertisedPublicPrefixState',
    'ExpressRouteCircuitPeeringState',
    'ExpressRouteCircuitSkuFamily',
    'ExpressRouteCircuitSkuTier',
    'ExpressRouteLinkAdminState',
    'ExpressRouteLinkMacSecCipher',
    'ExpressRoutePeeringState',
    'ExpressRoutePeeringType',
    'ExpressRoutePortsEncapsulation',
    'FirewallPolicyFilterRuleActionType',
    'FirewallPolicyNatRuleActionType',
    'FirewallPolicyRuleConditionApplicationProtocolType',
    'FirewallPolicyRuleConditionNetworkProtocol',
    'FirewallPolicyRuleConditionType',
    'FirewallPolicyRuleType',
    'IPAllocationMethod',
    'IPVersion',
    'IkeEncryption',
    'IkeIntegrity',
    'IpsecEncryption',
    'IpsecIntegrity',
    'LoadBalancerOutboundRuleProtocol',
    'LoadBalancerSkuName',
    'LoadDistribution',
    'NatGatewaySkuName',
    'PcProtocol',
    'PfsGroup',
    'ProbeProtocol',
    'PublicIPAddressSkuName',
    'PublicIPPrefixSkuName',
    'ResourceIdentityType',
    'RouteFilterRuleType',
    'RouteNextHopType',
    'SecurityRuleAccess',
    'SecurityRuleDirection',
    'SecurityRuleProtocol',
    'ServiceProviderProvisioningState',
    'TransportProtocol',
    'VirtualNetworkGatewayConnectionProtocol',
    'VirtualNetworkGatewayConnectionType',
    'VirtualNetworkGatewaySkuName',
    'VirtualNetworkGatewaySkuTier',
    'VirtualNetworkGatewayType',
    'VirtualNetworkPeeringState',
    'VpnClientProtocol',
    'VpnGatewayGeneration',
    'VpnGatewayTunnelingProtocol',
    'VpnType',
    'WebApplicationFirewallAction',
    'WebApplicationFirewallEnabledState',
    'WebApplicationFirewallMatchVariable',
    'WebApplicationFirewallMode',
    'WebApplicationFirewallOperator',
    'WebApplicationFirewallRuleType',
    'WebApplicationFirewallTransform',
]


class Access(str, Enum):
    """
    The access type of the rule.
    """
    ALLOW = "Allow"
    DENY = "Deny"


class ApplicationGatewayCookieBasedAffinity(str, Enum):
    """
    Cookie based affinity.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ApplicationGatewayCustomErrorStatusCode(str, Enum):
    """
    Status code of the application gateway customer error.
    """
    HTTP_STATUS403 = "HttpStatus403"
    HTTP_STATUS502 = "HttpStatus502"


class ApplicationGatewayFirewallMode(str, Enum):
    """
    Web application firewall mode.
    """
    DETECTION = "Detection"
    PREVENTION = "Prevention"


class ApplicationGatewayProtocol(str, Enum):
    """
    The protocol used for the probe.
    """
    HTTP = "Http"
    HTTPS = "Https"


class ApplicationGatewayRedirectType(str, Enum):
    """
    HTTP redirection type.
    """
    PERMANENT = "Permanent"
    FOUND = "Found"
    SEE_OTHER = "SeeOther"
    TEMPORARY = "Temporary"


class ApplicationGatewayRequestRoutingRuleType(str, Enum):
    """
    Rule type.
    """
    BASIC = "Basic"
    PATH_BASED_ROUTING = "PathBasedRouting"


class ApplicationGatewaySkuName(str, Enum):
    """
    Name of an application gateway SKU.
    """
    STANDARD_SMALL = "Standard_Small"
    STANDARD_MEDIUM = "Standard_Medium"
    STANDARD_LARGE = "Standard_Large"
    WA_F_MEDIUM = "WAF_Medium"
    WA_F_LARGE = "WAF_Large"
    STANDARD_V2 = "Standard_v2"
    WA_F_V2 = "WAF_v2"


class ApplicationGatewaySslCipherSuite(str, Enum):
    """
    Ssl cipher suites enums.
    """
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_256_CB_C_SHA384 = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_128_CB_C_SHA256 = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_256_CB_C_SHA = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_128_CB_C_SHA = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"
    TL_S_DH_E_RS_A_WIT_H_AE_S_256_GC_M_SHA384 = "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384"
    TL_S_DH_E_RS_A_WIT_H_AE_S_128_GC_M_SHA256 = "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256"
    TL_S_DH_E_RS_A_WIT_H_AE_S_256_CB_C_SHA = "TLS_DHE_RSA_WITH_AES_256_CBC_SHA"
    TL_S_DH_E_RS_A_WIT_H_AE_S_128_CB_C_SHA = "TLS_DHE_RSA_WITH_AES_128_CBC_SHA"
    TL_S_RS_A_WIT_H_AE_S_256_GC_M_SHA384 = "TLS_RSA_WITH_AES_256_GCM_SHA384"
    TL_S_RS_A_WIT_H_AE_S_128_GC_M_SHA256 = "TLS_RSA_WITH_AES_128_GCM_SHA256"
    TL_S_RS_A_WIT_H_AE_S_256_CB_C_SHA256 = "TLS_RSA_WITH_AES_256_CBC_SHA256"
    TL_S_RS_A_WIT_H_AE_S_128_CB_C_SHA256 = "TLS_RSA_WITH_AES_128_CBC_SHA256"
    TL_S_RS_A_WIT_H_AE_S_256_CB_C_SHA = "TLS_RSA_WITH_AES_256_CBC_SHA"
    TL_S_RS_A_WIT_H_AE_S_128_CB_C_SHA = "TLS_RSA_WITH_AES_128_CBC_SHA"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_256_GC_M_SHA384 = "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_128_GC_M_SHA256 = "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_256_CB_C_SHA384 = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_128_CB_C_SHA256 = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_256_CB_C_SHA = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"
    TL_S_ECDH_E_ECDS_A_WIT_H_AE_S_128_CB_C_SHA = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
    TL_S_DH_E_DS_S_WIT_H_AE_S_256_CB_C_SHA256 = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256"
    TL_S_DH_E_DS_S_WIT_H_AE_S_128_CB_C_SHA256 = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256"
    TL_S_DH_E_DS_S_WIT_H_AE_S_256_CB_C_SHA = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA"
    TL_S_DH_E_DS_S_WIT_H_AE_S_128_CB_C_SHA = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA"
    TL_S_RS_A_WIT_H_3_DE_S_ED_E_CB_C_SHA = "TLS_RSA_WITH_3DES_EDE_CBC_SHA"
    TL_S_DH_E_DS_S_WIT_H_3_DE_S_ED_E_CB_C_SHA = "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA"
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_128_GC_M_SHA256 = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
    TL_S_ECDH_E_RS_A_WIT_H_AE_S_256_GC_M_SHA384 = "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"


class ApplicationGatewaySslPolicyName(str, Enum):
    """
    Name of Ssl predefined policy.
    """
    APP_GW_SSL_POLICY20150501 = "AppGwSslPolicy20150501"
    APP_GW_SSL_POLICY20170401 = "AppGwSslPolicy20170401"
    APP_GW_SSL_POLICY20170401_S = "AppGwSslPolicy20170401S"


class ApplicationGatewaySslPolicyType(str, Enum):
    """
    Type of Ssl Policy.
    """
    PREDEFINED = "Predefined"
    CUSTOM = "Custom"


class ApplicationGatewaySslProtocol(str, Enum):
    """
    Minimum version of Ssl protocol to be supported on application gateway.
    """
    TL_SV1_0 = "TLSv1_0"
    TL_SV1_1 = "TLSv1_1"
    TL_SV1_2 = "TLSv1_2"


class ApplicationGatewayTier(str, Enum):
    """
    Tier of an application gateway.
    """
    STANDARD = "Standard"
    WAF = "WAF"
    STANDARD_V2 = "Standard_v2"
    WA_F_V2 = "WAF_v2"


class AuthorizationUseStatus(str, Enum):
    """
    The authorization use status.
    """
    AVAILABLE = "Available"
    IN_USE = "InUse"


class AzureFirewallApplicationRuleProtocolType(str, Enum):
    """
    Protocol type.
    """
    HTTP = "Http"
    HTTPS = "Https"
    MSSQL = "Mssql"


class AzureFirewallNatRCActionType(str, Enum):
    """
    The type of action.
    """
    SNAT = "Snat"
    DNAT = "Dnat"


class AzureFirewallNetworkRuleProtocol(str, Enum):
    """
    The protocol of a Network Rule resource.
    """
    TCP = "TCP"
    UDP = "UDP"
    ANY = "Any"
    ICMP = "ICMP"


class AzureFirewallRCActionType(str, Enum):
    """
    The type of action.
    """
    ALLOW = "Allow"
    DENY = "Deny"


class AzureFirewallThreatIntelMode(str, Enum):
    """
    The operation mode for Threat Intelligence.
    """
    ALERT = "Alert"
    DENY = "Deny"
    OFF = "Off"


class DdosCustomPolicyProtocol(str, Enum):
    """
    The protocol for which the DDoS protection policy is being customized.
    """
    TCP = "Tcp"
    UDP = "Udp"
    SYN = "Syn"


class DdosCustomPolicyTriggerSensitivityOverride(str, Enum):
    """
    The customized DDoS protection trigger rate sensitivity degrees. High: Trigger rate set with most sensitivity w.r.t. normal traffic. Default: Trigger rate set with moderate sensitivity w.r.t. normal traffic. Low: Trigger rate set with less sensitivity w.r.t. normal traffic. Relaxed: Trigger rate set with least sensitivity w.r.t. normal traffic.
    """
    RELAXED = "Relaxed"
    LOW = "Low"
    DEFAULT = "Default"
    HIGH = "High"


class DdosSettingsProtectionCoverage(str, Enum):
    """
    The DDoS protection policy customizability of the public IP. Only standard coverage will have the ability to be customized.
    """
    BASIC = "Basic"
    STANDARD = "Standard"


class DhGroup(str, Enum):
    """
    The DH Group used in IKE Phase 1 for initial SA.
    """
    NONE = "None"
    DH_GROUP1 = "DHGroup1"
    DH_GROUP2 = "DHGroup2"
    DH_GROUP14 = "DHGroup14"
    DH_GROUP2048 = "DHGroup2048"
    ECP256 = "ECP256"
    ECP384 = "ECP384"
    DH_GROUP24 = "DHGroup24"


class ExpressRouteCircuitPeeringAdvertisedPublicPrefixState(str, Enum):
    """
    The advertised public prefix state of the Peering resource.
    """
    NOT_CONFIGURED = "NotConfigured"
    CONFIGURING = "Configuring"
    CONFIGURED = "Configured"
    VALIDATION_NEEDED = "ValidationNeeded"


class ExpressRouteCircuitPeeringState(str, Enum):
    """
    The state of peering.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class ExpressRouteCircuitSkuFamily(str, Enum):
    """
    The family of the SKU.
    """
    UNLIMITED_DATA = "UnlimitedData"
    METERED_DATA = "MeteredData"


class ExpressRouteCircuitSkuTier(str, Enum):
    """
    The tier of the SKU.
    """
    STANDARD = "Standard"
    PREMIUM = "Premium"
    BASIC = "Basic"
    LOCAL = "Local"


class ExpressRouteLinkAdminState(str, Enum):
    """
    Administrative state of the physical port.
    """
    ENABLED = "Enabled"
    DISABLED = "Disabled"


class ExpressRouteLinkMacSecCipher(str, Enum):
    """
    Mac security cipher.
    """
    GCM_AES_128 = "gcm-aes-128"
    GCM_AES_256 = "gcm-aes-256"


class ExpressRoutePeeringState(str, Enum):
    """
    The peering state.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class ExpressRoutePeeringType(str, Enum):
    """
    The peering type.
    """
    AZURE_PUBLIC_PEERING = "AzurePublicPeering"
    AZURE_PRIVATE_PEERING = "AzurePrivatePeering"
    MICROSOFT_PEERING = "MicrosoftPeering"


class ExpressRoutePortsEncapsulation(str, Enum):
    """
    Encapsulation method on physical ports.
    """
    DOT1_Q = "Dot1Q"
    QIN_Q = "QinQ"


class FirewallPolicyFilterRuleActionType(str, Enum):
    """
    The type of action.
    """
    ALLOW = "Allow"
    DENY = "Deny"
    ALERT_ = "Alert "


class FirewallPolicyNatRuleActionType(str, Enum):
    """
    The type of action.
    """
    DNAT = "DNAT"
    SNAT = "SNAT"


class FirewallPolicyRuleConditionApplicationProtocolType(str, Enum):
    """
    Protocol type.
    """
    HTTP = "Http"
    HTTPS = "Https"


class FirewallPolicyRuleConditionNetworkProtocol(str, Enum):
    """
    The Network protocol of a Rule condition.
    """
    TCP = "TCP"
    UDP = "UDP"
    ANY = "Any"
    ICMP = "ICMP"


class FirewallPolicyRuleConditionType(str, Enum):
    """
    Rule Condition Type.
    """
    APPLICATION_RULE_CONDITION = "ApplicationRuleCondition"
    NETWORK_RULE_CONDITION = "NetworkRuleCondition"


class FirewallPolicyRuleType(str, Enum):
    """
    The type of the rule.
    """
    FIREWALL_POLICY_NAT_RULE = "FirewallPolicyNatRule"
    FIREWALL_POLICY_FILTER_RULE = "FirewallPolicyFilterRule"


class IPAllocationMethod(str, Enum):
    """
    The private IP address allocation method.
    """
    STATIC = "Static"
    DYNAMIC = "Dynamic"


class IPVersion(str, Enum):
    """
    Whether the specific IP configuration is IPv4 or IPv6. Default is IPv4.
    """
    I_PV4 = "IPv4"
    I_PV6 = "IPv6"


class IkeEncryption(str, Enum):
    """
    The IKE encryption algorithm (IKE phase 2).
    """
    DES = "DES"
    DES3 = "DES3"
    AES128 = "AES128"
    AES192 = "AES192"
    AES256 = "AES256"
    GCMAES256 = "GCMAES256"
    GCMAES128 = "GCMAES128"


class IkeIntegrity(str, Enum):
    """
    The IKE integrity algorithm (IKE phase 2).
    """
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA384 = "SHA384"
    GCMAES256 = "GCMAES256"
    GCMAES128 = "GCMAES128"


class IpsecEncryption(str, Enum):
    """
    The IPSec encryption algorithm (IKE phase 1).
    """
    NONE = "None"
    DES = "DES"
    DES3 = "DES3"
    AES128 = "AES128"
    AES192 = "AES192"
    AES256 = "AES256"
    GCMAES128 = "GCMAES128"
    GCMAES192 = "GCMAES192"
    GCMAES256 = "GCMAES256"


class IpsecIntegrity(str, Enum):
    """
    The IPSec integrity algorithm (IKE phase 1).
    """
    MD5 = "MD5"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    GCMAES128 = "GCMAES128"
    GCMAES192 = "GCMAES192"
    GCMAES256 = "GCMAES256"


class LoadBalancerOutboundRuleProtocol(str, Enum):
    """
    The protocol for the outbound rule in load balancer.
    """
    TCP = "Tcp"
    UDP = "Udp"
    ALL = "All"


class LoadBalancerSkuName(str, Enum):
    """
    Name of a load balancer SKU.
    """
    BASIC = "Basic"
    STANDARD = "Standard"


class LoadDistribution(str, Enum):
    """
    The load distribution policy for this rule.
    """
    DEFAULT = "Default"
    SOURCE_IP = "SourceIP"
    SOURCE_IP_PROTOCOL = "SourceIPProtocol"


class NatGatewaySkuName(str, Enum):
    """
    Name of Nat Gateway SKU.
    """
    STANDARD = "Standard"


class PcProtocol(str, Enum):
    """
    Protocol to be filtered on.
    """
    TCP = "TCP"
    UDP = "UDP"
    ANY = "Any"


class PfsGroup(str, Enum):
    """
    The Pfs Group used in IKE Phase 2 for new child SA.
    """
    NONE = "None"
    PFS1 = "PFS1"
    PFS2 = "PFS2"
    PFS2048 = "PFS2048"
    ECP256 = "ECP256"
    ECP384 = "ECP384"
    PFS24 = "PFS24"
    PFS14 = "PFS14"
    PFSMM = "PFSMM"


class ProbeProtocol(str, Enum):
    """
    The protocol of the end point. If 'Tcp' is specified, a received ACK is required for the probe to be successful. If 'Http' or 'Https' is specified, a 200 OK response from the specifies URI is required for the probe to be successful.
    """
    HTTP = "Http"
    TCP = "Tcp"
    HTTPS = "Https"


class PublicIPAddressSkuName(str, Enum):
    """
    Name of a public IP address SKU.
    """
    BASIC = "Basic"
    STANDARD = "Standard"


class PublicIPPrefixSkuName(str, Enum):
    """
    Name of a public IP prefix SKU.
    """
    STANDARD = "Standard"


class ResourceIdentityType(str, Enum):
    """
    The type of identity used for the resource. The type 'SystemAssigned, UserAssigned' includes both an implicitly created identity and a set of user assigned identities. The type 'None' will remove any identities from the virtual machine.
    """
    SYSTEM_ASSIGNED = "SystemAssigned"
    USER_ASSIGNED = "UserAssigned"
    SYSTEM_ASSIGNED_USER_ASSIGNED = "SystemAssigned, UserAssigned"
    NONE = "None"


class RouteFilterRuleType(str, Enum):
    """
    The rule type of the rule.
    """
    COMMUNITY = "Community"


class RouteNextHopType(str, Enum):
    """
    The type of Azure hop the packet should be sent to.
    """
    VIRTUAL_NETWORK_GATEWAY = "VirtualNetworkGateway"
    VNET_LOCAL = "VnetLocal"
    INTERNET = "Internet"
    VIRTUAL_APPLIANCE = "VirtualAppliance"
    NONE = "None"


class SecurityRuleAccess(str, Enum):
    """
    The network traffic is allowed or denied.
    """
    ALLOW = "Allow"
    DENY = "Deny"


class SecurityRuleDirection(str, Enum):
    """
    The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic.
    """
    INBOUND = "Inbound"
    OUTBOUND = "Outbound"


class SecurityRuleProtocol(str, Enum):
    """
    Network protocol this rule applies to.
    """
    TCP = "Tcp"
    UDP = "Udp"
    ICMP = "Icmp"
    ESP = "Esp"
    ASTERISK = "*"


class ServiceProviderProvisioningState(str, Enum):
    """
    The ServiceProviderProvisioningState state of the resource.
    """
    NOT_PROVISIONED = "NotProvisioned"
    PROVISIONING = "Provisioning"
    PROVISIONED = "Provisioned"
    DEPROVISIONING = "Deprovisioning"


class TransportProtocol(str, Enum):
    """
    The reference to the transport protocol used by the load balancing rule.
    """
    UDP = "Udp"
    TCP = "Tcp"
    ALL = "All"


class VirtualNetworkGatewayConnectionProtocol(str, Enum):
    """
    Connection protocol used for this connection.
    """
    IK_EV2 = "IKEv2"
    IK_EV1 = "IKEv1"


class VirtualNetworkGatewayConnectionType(str, Enum):
    """
    Gateway connection type.
    """
    IPSEC = "IPsec"
    VNET2_VNET = "Vnet2Vnet"
    EXPRESS_ROUTE = "ExpressRoute"
    VPN_CLIENT = "VPNClient"


class VirtualNetworkGatewaySkuName(str, Enum):
    """
    Gateway SKU name.
    """
    BASIC = "Basic"
    HIGH_PERFORMANCE = "HighPerformance"
    STANDARD = "Standard"
    ULTRA_PERFORMANCE = "UltraPerformance"
    VPN_GW1 = "VpnGw1"
    VPN_GW2 = "VpnGw2"
    VPN_GW3 = "VpnGw3"
    VPN_GW4 = "VpnGw4"
    VPN_GW5 = "VpnGw5"
    VPN_GW1_AZ = "VpnGw1AZ"
    VPN_GW2_AZ = "VpnGw2AZ"
    VPN_GW3_AZ = "VpnGw3AZ"
    VPN_GW4_AZ = "VpnGw4AZ"
    VPN_GW5_AZ = "VpnGw5AZ"
    ER_GW1_AZ = "ErGw1AZ"
    ER_GW2_AZ = "ErGw2AZ"
    ER_GW3_AZ = "ErGw3AZ"


class VirtualNetworkGatewaySkuTier(str, Enum):
    """
    Gateway SKU tier.
    """
    BASIC = "Basic"
    HIGH_PERFORMANCE = "HighPerformance"
    STANDARD = "Standard"
    ULTRA_PERFORMANCE = "UltraPerformance"
    VPN_GW1 = "VpnGw1"
    VPN_GW2 = "VpnGw2"
    VPN_GW3 = "VpnGw3"
    VPN_GW4 = "VpnGw4"
    VPN_GW5 = "VpnGw5"
    VPN_GW1_AZ = "VpnGw1AZ"
    VPN_GW2_AZ = "VpnGw2AZ"
    VPN_GW3_AZ = "VpnGw3AZ"
    VPN_GW4_AZ = "VpnGw4AZ"
    VPN_GW5_AZ = "VpnGw5AZ"
    ER_GW1_AZ = "ErGw1AZ"
    ER_GW2_AZ = "ErGw2AZ"
    ER_GW3_AZ = "ErGw3AZ"


class VirtualNetworkGatewayType(str, Enum):
    """
    The type of this virtual network gateway.
    """
    VPN = "Vpn"
    EXPRESS_ROUTE = "ExpressRoute"


class VirtualNetworkPeeringState(str, Enum):
    """
    The status of the virtual network peering.
    """
    INITIATED = "Initiated"
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"


class VpnClientProtocol(str, Enum):
    """
    VPN client protocol enabled for the virtual network gateway.
    """
    IKE_V2 = "IkeV2"
    SSTP = "SSTP"
    OPEN_VPN = "OpenVPN"


class VpnGatewayGeneration(str, Enum):
    """
    The generation for this VirtualNetworkGateway. Must be None if gatewayType is not VPN.
    """
    NONE = "None"
    GENERATION1 = "Generation1"
    GENERATION2 = "Generation2"


class VpnGatewayTunnelingProtocol(str, Enum):
    """
    VPN protocol enabled for the P2SVpnServerConfiguration.
    """
    IKE_V2 = "IkeV2"
    OPEN_VPN = "OpenVPN"


class VpnType(str, Enum):
    """
    The type of this virtual network gateway.
    """
    POLICY_BASED = "PolicyBased"
    ROUTE_BASED = "RouteBased"


class WebApplicationFirewallAction(str, Enum):
    """
    Type of Actions.
    """
    ALLOW = "Allow"
    BLOCK = "Block"
    LOG = "Log"


class WebApplicationFirewallEnabledState(str, Enum):
    """
    Describes if the policy is in enabled state or disabled state.
    """
    DISABLED = "Disabled"
    ENABLED = "Enabled"


class WebApplicationFirewallMatchVariable(str, Enum):
    """
    Match Variable.
    """
    REMOTE_ADDR = "RemoteAddr"
    REQUEST_METHOD = "RequestMethod"
    QUERY_STRING = "QueryString"
    POST_ARGS = "PostArgs"
    REQUEST_URI = "RequestUri"
    REQUEST_HEADERS = "RequestHeaders"
    REQUEST_BODY = "RequestBody"
    REQUEST_COOKIES = "RequestCookies"


class WebApplicationFirewallMode(str, Enum):
    """
    Describes if it is in detection mode or prevention mode at policy level.
    """
    PREVENTION = "Prevention"
    DETECTION = "Detection"


class WebApplicationFirewallOperator(str, Enum):
    """
    Describes operator to be matched.
    """
    IP_MATCH = "IPMatch"
    EQUAL = "Equal"
    CONTAINS = "Contains"
    LESS_THAN = "LessThan"
    GREATER_THAN = "GreaterThan"
    LESS_THAN_OR_EQUAL = "LessThanOrEqual"
    GREATER_THAN_OR_EQUAL = "GreaterThanOrEqual"
    BEGINS_WITH = "BeginsWith"
    ENDS_WITH = "EndsWith"
    REGEX = "Regex"


class WebApplicationFirewallRuleType(str, Enum):
    """
    Describes type of rule.
    """
    MATCH_RULE = "MatchRule"
    INVALID = "Invalid"


class WebApplicationFirewallTransform(str, Enum):
    """
    Describes what transforms applied before matching.
    """
    LOWERCASE = "Lowercase"
    TRIM = "Trim"
    URL_DECODE = "UrlDecode"
    URL_ENCODE = "UrlEncode"
    REMOVE_NULLS = "RemoveNulls"
    HTML_ENTITY_DECODE = "HtmlEntityDecode"
