# ApPerformance

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**free_memory** | **int** | free memory in kilobytes | [optional] 
**cpu_utilized** | **list[int]** | CPU utilization in percentage, one per core | [optional] 
**up_time** | **int** | AP uptime in seconds | [optional] 
**cami_crashed** | **int** | number of time cloud-to-ap-management process crashed | [optional] 
**cpu_temperature** | **int** | cpu temperature in Celsius | [optional] 
**low_memory_reboot** | **bool** | low memory reboot happened | [optional] 
**eth_link_state** | [**EthernetLinkState**](EthernetLinkState.md) |  | [optional] 
**cloud_tx_bytes** | **int** | Data sent by AP to the cloud | [optional] 
**cloud_rx_bytes** | **int** | Data received by AP from cloud | [optional] 
**ps_cpu_util** | [**list[PerProcessUtilization]**](PerProcessUtilization.md) |  | [optional] 
**ps_mem_util** | [**list[PerProcessUtilization]**](PerProcessUtilization.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

