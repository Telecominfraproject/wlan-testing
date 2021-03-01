# RadiusNasConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**nas_client_id** | **str** | String identifying the NAS (AP) – Default shall be set to the AP BASE MAC Address for the WAN Interface | [optional] [default to 'DEFAULT']
**nas_client_ip** | **str** | NAS-IP AVP - Default it shall be the WAN IP address of the AP when AP communicates with RADIUS server directly. | [optional] [default to 'WAN_IP']
**user_defined_nas_id** | **str** | user entered string if the nasClientId is &#x27;USER_DEFINED&#x27;. This should not be enabled and will not be passed to the AP unless the nasClientId is USER_DEFINED. | [optional] 
**user_defined_nas_ip** | **str** | user entered IP address if the nasClientIp is &#x27;USER_DEFINED&#x27;.  This should not be enabled and will not be passed to the AP unless the nasClientIp is USER_DEFINED. | [optional] 
**operator_id** | **str** | Carries the operator namespace identifier and the operator name.  The operator name is combined with the namespace identifier to uniquely identify the owner of an access network.  The value of the Operator-Name is a non-NULL terminated text. This is not to be confused with the Passpoint Operator Domain | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

