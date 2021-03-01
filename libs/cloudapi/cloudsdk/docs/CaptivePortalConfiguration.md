# CaptivePortalConfiguration

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** |  | [optional] 
**browser_title** | **str** |  | [optional] 
**header_content** | **str** |  | [optional] 
**user_acceptance_policy** | **str** |  | [optional] 
**success_page_markdown_text** | **str** |  | [optional] 
**redirect_url** | **str** |  | [optional] 
**external_captive_portal_url** | **str** |  | [optional] 
**session_timeout_in_minutes** | **int** |  | [optional] 
**logo_file** | [**ManagedFileInfo**](ManagedFileInfo.md) |  | [optional] 
**background_file** | [**ManagedFileInfo**](ManagedFileInfo.md) |  | [optional] 
**walled_garden_allowlist** | **list[str]** |  | [optional] 
**username_password_file** | [**ManagedFileInfo**](ManagedFileInfo.md) |  | [optional] 
**authentication_type** | [**CaptivePortalAuthenticationType**](CaptivePortalAuthenticationType.md) |  | [optional] 
**radius_auth_method** | [**RadiusAuthenticationMethod**](RadiusAuthenticationMethod.md) |  | [optional] 
**max_users_with_same_credentials** | **int** |  | [optional] 
**external_policy_file** | [**ManagedFileInfo**](ManagedFileInfo.md) |  | [optional] 
**background_position** | [**BackgroundPosition**](BackgroundPosition.md) |  | [optional] 
**background_repeat** | [**BackgroundRepeat**](BackgroundRepeat.md) |  | [optional] 
**radius_service_id** | **int** |  | [optional] 
**expiry_type** | [**SessionExpiryType**](SessionExpiryType.md) |  | [optional] 
**user_list** | [**list[TimedAccessUserRecord]**](TimedAccessUserRecord.md) |  | [optional] 
**mac_allow_list** | [**list[MacAllowlistRecord]**](MacAllowlistRecord.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

