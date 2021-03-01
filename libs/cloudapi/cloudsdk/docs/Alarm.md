# Alarm

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**customer_id** | **int** |  | [optional] 
**equipment_id** | **int** |  | [optional] 
**alarm_code** | [**AlarmCode**](AlarmCode.md) |  | [optional] 
**created_timestamp** | **int** |  | [optional] 
**originator_type** | [**OriginatorType**](OriginatorType.md) |  | [optional] 
**severity** | [**StatusCode**](StatusCode.md) |  | [optional] 
**scope_type** | [**AlarmScopeType**](AlarmScopeType.md) |  | [optional] 
**scope_id** | **str** |  | [optional] 
**details** | [**AlarmDetails**](AlarmDetails.md) |  | [optional] 
**acknowledged** | **bool** |  | [optional] 
**last_modified_timestamp** | **int** | must be provided for update operation, update will be rejected if provided value does not match the one currently stored in the database | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

