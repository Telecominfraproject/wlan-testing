# SsidConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** |  | [optional] 
**ssid** | **str** |  | [optional] 
**applied_radios** | [**list[RadioType]**](RadioType.md) |  | [optional] 
**ssid_admin_state** | [**StateSetting**](StateSetting.md) |  | [optional] 
**secure_mode** | [**SsidSecureMode**](SsidSecureMode.md) |  | [optional] 
**vlan_id** | **int** |  | [optional] 
**dynamic_vlan** | [**DynamicVlanMode**](DynamicVlanMode.md) |  | [optional] 
**key_str** | **str** |  | [optional] 
**broadcast_ssid** | [**StateSetting**](StateSetting.md) |  | [optional] 
**key_refresh** | **int** |  | [optional] [default to 0]
**no_local_subnets** | **bool** |  | [optional] 
**radius_service_id** | **int** |  | [optional] 
**radius_acounting_service_interval** | **int** | If this is set (i.e. non-null), RadiusAccountingService is configured, and SsidSecureMode is configured as Enterprise/Radius, ap will send interim accounting updates every N seconds | [optional] 
**radius_nas_configuration** | [**RadiusNasConfiguration**](RadiusNasConfiguration.md) |  | [optional] 
**captive_portal_id** | **int** | id of a CaptivePortalConfiguration profile, must be also added to the children of this profile | [optional] 
**bandwidth_limit_down** | **int** |  | [optional] 
**bandwidth_limit_up** | **int** |  | [optional] 
**client_bandwidth_limit_down** | **int** |  | [optional] 
**client_bandwidth_limit_up** | **int** |  | [optional] 
**video_traffic_only** | **bool** |  | [optional] 
**radio_based_configs** | [**RadioBasedSsidConfigurationMap**](RadioBasedSsidConfigurationMap.md) |  | [optional] 
**bonjour_gateway_profile_id** | **int** | id of a BonjourGateway profile, must be also added to the children of this profile | [optional] 
**enable80211w** | **bool** |  | [optional] 
**wep_config** | [**WepConfiguration**](WepConfiguration.md) |  | [optional] 
**forward_mode** | [**NetworkForwardMode**](NetworkForwardMode.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

