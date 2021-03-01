# swagger_client.StatusApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_status_by_customer_equipment**](StatusApi.md#get_status_by_customer_equipment) | **GET** /portal/status/forEquipment | Get all Status objects for a given customer equipment.
[**get_status_by_customer_equipment_with_filter**](StatusApi.md#get_status_by_customer_equipment_with_filter) | **GET** /portal/status/forEquipmentWithFilter | Get Status objects for a given customer equipment ids and status data types.
[**get_status_by_customer_id**](StatusApi.md#get_status_by_customer_id) | **GET** /portal/status/forCustomer | Get all Status objects By customerId
[**get_status_by_customer_with_filter**](StatusApi.md#get_status_by_customer_with_filter) | **GET** /portal/status/forCustomerWithFilter | Get list of Statuses for customerId, set of equipment ids, and set of status data types.

# **get_status_by_customer_equipment**
> list[Status] get_status_by_customer_equipment(customer_id, equipment_id)

Get all Status objects for a given customer equipment.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.StatusApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
equipment_id = 789 # int | Equipment id

try:
    # Get all Status objects for a given customer equipment.
    api_response = api_instance.get_status_by_customer_equipment(customer_id, equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusApi->get_status_by_customer_equipment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **equipment_id** | **int**| Equipment id | 

### Return type

[**list[Status]**](Status.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_status_by_customer_equipment_with_filter**
> list[Status] get_status_by_customer_equipment_with_filter(customer_id, equipment_ids, status_data_types=status_data_types)

Get Status objects for a given customer equipment ids and status data types.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.StatusApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
equipment_ids = [56] # list[int] | Set of equipment ids. Must not be empty or null.
status_data_types = [swagger_client.StatusDataType()] # list[StatusDataType] | Set of status data types. Empty or null means retrieve all data types. (optional)

try:
    # Get Status objects for a given customer equipment ids and status data types.
    api_response = api_instance.get_status_by_customer_equipment_with_filter(customer_id, equipment_ids, status_data_types=status_data_types)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusApi->get_status_by_customer_equipment_with_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Must not be empty or null. | 
 **status_data_types** | [**list[StatusDataType]**](StatusDataType.md)| Set of status data types. Empty or null means retrieve all data types. | [optional] 

### Return type

[**list[Status]**](Status.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_status_by_customer_id**
> PaginationResponseStatus get_status_by_customer_id(customer_id, pagination_context, sort_by=sort_by)

Get all Status objects By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.StatusApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextStatus() # PaginationContextStatus | pagination context
sort_by = [swagger_client.SortColumnsStatus()] # list[SortColumnsStatus] | sort options (optional)

try:
    # Get all Status objects By customerId
    api_response = api_instance.get_status_by_customer_id(customer_id, pagination_context, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusApi->get_status_by_customer_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextStatus**](.md)| pagination context | 
 **sort_by** | [**list[SortColumnsStatus]**](SortColumnsStatus.md)| sort options | [optional] 

### Return type

[**PaginationResponseStatus**](PaginationResponseStatus.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_status_by_customer_with_filter**
> PaginationResponseStatus get_status_by_customer_with_filter(customer_id, pagination_context, equipment_ids=equipment_ids, status_data_types=status_data_types, sort_by=sort_by)

Get list of Statuses for customerId, set of equipment ids, and set of status data types.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.StatusApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextStatus() # PaginationContextStatus | pagination context
equipment_ids = [56] # list[int] | Set of equipment ids. Empty or null means retrieve all equipment for the customer. (optional)
status_data_types = [swagger_client.StatusDataType()] # list[StatusDataType] | Set of status data types. Empty or null means retrieve all data types. (optional)
sort_by = [swagger_client.SortColumnsStatus()] # list[SortColumnsStatus] | sort options (optional)

try:
    # Get list of Statuses for customerId, set of equipment ids, and set of status data types.
    api_response = api_instance.get_status_by_customer_with_filter(customer_id, pagination_context, equipment_ids=equipment_ids, status_data_types=status_data_types, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StatusApi->get_status_by_customer_with_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextStatus**](.md)| pagination context | 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Empty or null means retrieve all equipment for the customer. | [optional] 
 **status_data_types** | [**list[StatusDataType]**](StatusDataType.md)| Set of status data types. Empty or null means retrieve all data types. | [optional] 
 **sort_by** | [**list[SortColumnsStatus]**](SortColumnsStatus.md)| sort options | [optional] 

### Return type

[**PaginationResponseStatus**](PaginationResponseStatus.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

