# swagger_client.WLANServiceMetricsApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_service_metricsfor_customer**](WLANServiceMetricsApi.md#get_service_metricsfor_customer) | **GET** /portal/serviceMetric/forCustomer | Get list of WLAN Service Metrics for customerId, optional set of location ids, optional set of equipment ids, optional set of client MAC addresses, optional set of metric data types.  Only metrics that are created between specified fromTime and toTime are retrieved.  

# **get_service_metricsfor_customer**
> PaginationResponseServiceMetric get_service_metricsfor_customer(from_time, to_time, customer_id, pagination_context, location_ids=location_ids, equipment_ids=equipment_ids, client_macs=client_macs, data_types=data_types, sort_by=sort_by)

Get list of WLAN Service Metrics for customerId, optional set of location ids, optional set of equipment ids, optional set of client MAC addresses, optional set of metric data types.  Only metrics that are created between specified fromTime and toTime are retrieved.  

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.WLANServiceMetricsApi(swagger_client.ApiClient(configuration))
from_time = 789 # int | Include metrics created after (and including) this timestamp in milliseconds
to_time = 789 # int | Include metrics created before (and including) this timestamp in milliseconds
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextServiceMetric() # PaginationContextServiceMetric | pagination context
location_ids = [56] # list[int] | Set of location ids. Empty or null means retrieve metrics for all locations for the customer. (optional)
equipment_ids = [56] # list[int] | Set of equipment ids. Empty or null means retrieve metrics for all equipment for the customer. (optional)
client_macs = ['client_macs_example'] # list[str] | Set of client MAC addresses. Empty or null means retrieve metrics for all client MACs for the customer. (optional)
data_types = [swagger_client.ServiceMetricDataType()] # list[ServiceMetricDataType] | Set of metric data types. Empty or null means retrieve all. (optional)
sort_by = [swagger_client.SortColumnsServiceMetric()] # list[SortColumnsServiceMetric] | Sort options. If not provided, then results will be ordered by equipmentId and createdTimestamp. (optional)

try:
    # Get list of WLAN Service Metrics for customerId, optional set of location ids, optional set of equipment ids, optional set of client MAC addresses, optional set of metric data types.  Only metrics that are created between specified fromTime and toTime are retrieved.  
    api_response = api_instance.get_service_metricsfor_customer(from_time, to_time, customer_id, pagination_context, location_ids=location_ids, equipment_ids=equipment_ids, client_macs=client_macs, data_types=data_types, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling WLANServiceMetricsApi->get_service_metricsfor_customer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_time** | **int**| Include metrics created after (and including) this timestamp in milliseconds | 
 **to_time** | **int**| Include metrics created before (and including) this timestamp in milliseconds | 
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextServiceMetric**](.md)| pagination context | 
 **location_ids** | [**list[int]**](int.md)| Set of location ids. Empty or null means retrieve metrics for all locations for the customer. | [optional] 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Empty or null means retrieve metrics for all equipment for the customer. | [optional] 
 **client_macs** | [**list[str]**](str.md)| Set of client MAC addresses. Empty or null means retrieve metrics for all client MACs for the customer. | [optional] 
 **data_types** | [**list[ServiceMetricDataType]**](ServiceMetricDataType.md)| Set of metric data types. Empty or null means retrieve all. | [optional] 
 **sort_by** | [**list[SortColumnsServiceMetric]**](SortColumnsServiceMetric.md)| Sort options. If not provided, then results will be ordered by equipmentId and createdTimestamp. | [optional] 

### Return type

[**PaginationResponseServiceMetric**](PaginationResponseServiceMetric.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

