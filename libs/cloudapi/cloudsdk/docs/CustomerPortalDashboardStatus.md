# CustomerPortalDashboardStatus

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** |  | 
**status_data_type** | **str** |  | [optional] 
**time_bucket_id** | **int** | All metrics/events that have (createdTimestamp % timeBucketMs &#x3D;&#x3D; timeBucketId) are counted in this object. | [optional] 
**time_bucket_ms** | **int** | Length of the time bucket in milliseconds | [optional] 
**equipment_in_service_count** | **int** |  | [optional] 
**equipment_with_clients_count** | **int** |  | [optional] 
**total_provisioned_equipment** | **int** |  | [optional] 
**traffic_bytes_downstream** | **int** |  | [optional] 
**traffic_bytes_upstream** | **int** |  | [optional] 
**associated_clients_count_per_radio** | [**IntegerPerRadioTypeMap**](IntegerPerRadioTypeMap.md) |  | [optional] 
**client_count_per_oui** | [**IntegerValueMap**](IntegerValueMap.md) |  | [optional] 
**equipment_count_per_oui** | [**IntegerValueMap**](IntegerValueMap.md) |  | [optional] 
**alarms_count_by_severity** | [**IntegerPerStatusCodeMap**](IntegerPerStatusCodeMap.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

