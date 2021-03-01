# ApNodeMetrics

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**model_type** | **str** |  | 
**period_length_sec** | **int** | How many seconds the AP measured for the metric | [optional] 
**client_mac_addresses_per_radio** | [**ListOfMacsPerRadioMap**](ListOfMacsPerRadioMap.md) |  | [optional] 
**tx_bytes_per_radio** | [**LongPerRadioTypeMap**](LongPerRadioTypeMap.md) |  | [optional] 
**rx_bytes_per_radio** | [**LongPerRadioTypeMap**](LongPerRadioTypeMap.md) |  | [optional] 
**noise_floor_per_radio** | [**IntegerPerRadioTypeMap**](IntegerPerRadioTypeMap.md) |  | [optional] 
**tunnel_metrics** | [**list[TunnelMetricData]**](TunnelMetricData.md) |  | [optional] 
**network_probe_metrics** | [**list[NetworkProbeMetrics]**](NetworkProbeMetrics.md) |  | [optional] 
**radius_metrics** | [**list[RadiusMetrics]**](RadiusMetrics.md) |  | [optional] 
**cloud_link_availability** | **int** |  | [optional] 
**cloud_link_latency_in_ms** | **int** |  | [optional] 
**channel_utilization_per_radio** | [**IntegerPerRadioTypeMap**](IntegerPerRadioTypeMap.md) |  | [optional] 
**ap_performance** | [**ApPerformance**](ApPerformance.md) |  | [optional] 
**vlan_subnet** | [**list[VlanSubnet]**](VlanSubnet.md) |  | [optional] 
**radio_utilization_per_radio** | [**ListOfRadioUtilizationPerRadioMap**](ListOfRadioUtilizationPerRadioMap.md) |  | [optional] 
**radio_stats_per_radio** | [**RadioStatisticsPerRadioMap**](RadioStatisticsPerRadioMap.md) |  | [optional] 
**mcs_stats_per_radio** | [**ListOfMcsStatsPerRadioMap**](ListOfMcsStatsPerRadioMap.md) |  | [optional] 
**wmm_queues_per_radio** | [**MapOfWmmQueueStatsPerRadioMap**](MapOfWmmQueueStatsPerRadioMap.md) |  | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

