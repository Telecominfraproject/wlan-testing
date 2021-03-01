# TunnelMetricData

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ip_addr** | **str** | IP address of tunnel peer | [optional] 
**cfg_time** | **int** | number of seconds tunnel was configured | [optional] 
**up_time** | **int** | number of seconds tunnel was up in current bin | [optional] 
**pings_sent** | **int** | number of &#x27;ping&#x27; sent in the current bin in case tunnel was DOWN | [optional] 
**pings_recvd** | **int** | number of &#x27;ping&#x27; response received by peer in the current bin in case tunnel was DOWN | [optional] 
**active_tun** | **bool** | Indicates if the current tunnel is the active one | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

