# PasspointProfile

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** |  | [optional] 
**enable_interworking_and_hs20** | **bool** |  | [optional] 
**additional_steps_required_for_access** | **int** |  | [optional] 
**deauth_request_timeout** | **int** |  | [optional] 
**operating_class** | **int** |  | [optional] 
**terms_and_conditions_file** | [**ManagedFileInfo**](ManagedFileInfo.md) |  | [optional] 
**whitelist_domain** | **str** |  | [optional] 
**emergency_services_reachable** | **bool** |  | [optional] 
**unauthenticated_emergency_service_accessible** | **bool** |  | [optional] 
**internet_connectivity** | **bool** |  | [optional] 
**ip_address_type_availability** | [**Object**](Object.md) |  | [optional] 
**qos_map_set_configuration** | **list[str]** |  | [optional] 
**hessid** | [**MacAddress**](MacAddress.md) |  | [optional] 
**ap_geospatial_location** | **str** |  | [optional] 
**ap_civic_location** | **str** |  | [optional] 
**anqp_domain_id** | **int** |  | [optional] 
**disable_downstream_group_addressed_forwarding** | **bool** |  | [optional] 
**enable2pt4_g_hz** | **bool** |  | [optional] 
**enable5_g_hz** | **bool** |  | [optional] 
**associated_access_ssid_profile_ids** | **list[int]** |  | [optional] 
**osu_ssid_profile_id** | **int** |  | [optional] 
**passpoint_operator_profile_id** | **int** | Profile Id of a PasspointOperatorProfile profile, must be also added to the children of this profile | [optional] 
**passpoint_venue_profile_id** | **int** | Profile Id of a PasspointVenueProfile profile, must be also added to the children of this profile | [optional] 
**passpoint_osu_provider_profile_ids** | **list[int]** | array containing Profile Ids of PasspointOsuProviderProfiles, must be also added to the children of this profile | [optional] 
**ap_public_location_id_uri** | **str** |  | [optional] 
**access_network_type** | [**PasspointAccessNetworkType**](PasspointAccessNetworkType.md) |  | [optional] 
**network_authentication_type** | [**PasspointNetworkAuthenticationType**](PasspointNetworkAuthenticationType.md) |  | [optional] 
**connection_capability_set** | [**list[PasspointConnectionCapability]**](PasspointConnectionCapability.md) |  | [optional] 
**gas_addr3_behaviour** | [**PasspointGasAddress3Behaviour**](PasspointGasAddress3Behaviour.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

