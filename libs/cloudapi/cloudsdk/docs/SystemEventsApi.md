# swagger_client.SystemEventsApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_system_eventsfor_customer**](SystemEventsApi.md#get_system_eventsfor_customer) | **GET** /portal/systemEvent/forCustomer | Get list of System Events for customerId, optional set of equipment ids, and optional set of data types. Only events that are created between specified fromTime and toTime are retrieved.

# **get_system_eventsfor_customer**
> PaginationResponseSystemEvent get_system_eventsfor_customer(from_time, to_time, customer_id, pagination_context, location_ids=location_ids, equipment_ids=equipment_ids, client_macs=client_macs, data_types=data_types, sort_by=sort_by)

Get list of System Events for customerId, optional set of equipment ids, and optional set of data types. Only events that are created between specified fromTime and toTime are retrieved.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.SystemEventsApi(swagger_client.ApiClient(configuration))
from_time = 789 # int | Include events created after (and including) this timestamp in milliseconds
to_time = 789 # int | Include events created before (and including) this timestamp in milliseconds
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextSystemEvent() # PaginationContextSystemEvent | pagination context
location_ids = [56] # list[int] | Set of location ids. Empty or null means retrieve events for all locations for the customer. (optional)
equipment_ids = [56] # list[int] | Set of equipment ids. Empty or null means retrieve events for all equipment for the customer. (optional)
client_macs = ['client_macs_example'] # list[str] | Set of client MAC addresses. Empty or null means retrieve events for all client MACs for the customer. (optional)
data_types = [swagger_client.SystemEventDataType()] # list[SystemEventDataType] | Set of system event data types. Empty or null means retrieve all. (optional)
sort_by = [swagger_client.SortColumnsSystemEvent()] # list[SortColumnsSystemEvent] | Sort options. If not provided, then results will be ordered by equipmentId and createdTimestamp. (optional)

try:
    # Get list of System Events for customerId, optional set of equipment ids, and optional set of data types. Only events that are created between specified fromTime and toTime are retrieved.
    api_response = api_instance.get_system_eventsfor_customer(from_time, to_time, customer_id, pagination_context, location_ids=location_ids, equipment_ids=equipment_ids, client_macs=client_macs, data_types=data_types, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemEventsApi->get_system_eventsfor_customer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **from_time** | **int**| Include events created after (and including) this timestamp in milliseconds | 
 **to_time** | **int**| Include events created before (and including) this timestamp in milliseconds | 
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextSystemEvent**](.md)| pagination context | 
 **location_ids** | [**list[int]**](int.md)| Set of location ids. Empty or null means retrieve events for all locations for the customer. | [optional] 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Empty or null means retrieve events for all equipment for the customer. | [optional] 
 **client_macs** | [**list[str]**](str.md)| Set of client MAC addresses. Empty or null means retrieve events for all client MACs for the customer. | [optional] 
 **data_types** | [**list[SystemEventDataType]**](SystemEventDataType.md)| Set of system event data types. Empty or null means retrieve all. | [optional] 
 **sort_by** | [**list[SortColumnsSystemEvent]**](SortColumnsSystemEvent.md)| Sort options. If not provided, then results will be ordered by equipmentId and createdTimestamp. | [optional] 

### Return type

[**PaginationResponseSystemEvent**](PaginationResponseSystemEvent.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

