# ServiceAdoptionMetrics

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**year** | **int** |  | [optional] 
**month** | **int** |  | [optional] 
**week_of_year** | **int** |  | [optional] 
**day_of_year** | **int** |  | [optional] 
**customer_id** | **int** |  | [optional] 
**location_id** | **int** |  | [optional] 
**equipment_id** | **int** |  | [optional] 
**num_unique_connected_macs** | **int** | number of unique connected MAC addresses for the data point. Note - this number is accurate only at the lowest level of granularity - per AP per day. In case of aggregations - per location/customer or per week/month - this number is just a sum of corresponding datapoints, and it does not account for non-unique MACs in those cases. | [optional] 
**num_bytes_upstream** | **int** |  | [optional] 
**num_bytes_downstream** | **int** |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

