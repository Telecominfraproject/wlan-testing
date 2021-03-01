# swagger_client.ClientsApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_client_sessions_in_set**](ClientsApi.md#get_all_client_sessions_in_set) | **GET** /portal/client/session/inSet | Get list of Client sessions for customerId and a set of client MAC addresses.
[**get_all_clients_in_set**](ClientsApi.md#get_all_clients_in_set) | **GET** /portal/client/inSet | Get list of Clients for customerId and a set of client MAC addresses.
[**get_blocked_clients**](ClientsApi.md#get_blocked_clients) | **GET** /portal/client/blocked | Retrieves a list of Clients for the customer that are marked as blocked. This per-customer list of blocked clients is pushed to every AP, so it has to be limited in size.
[**get_client_session_by_customer_with_filter**](ClientsApi.md#get_client_session_by_customer_with_filter) | **GET** /portal/client/session/forCustomer | Get list of Client sessions for customerId and a set of equipment/location ids. Equipment and locations filters are joined using logical AND operation.
[**get_for_customer**](ClientsApi.md#get_for_customer) | **GET** /portal/client/forCustomer | Get list of clients for a given customer by equipment ids
[**search_by_mac_address**](ClientsApi.md#search_by_mac_address) | **GET** /portal/client/searchByMac | Get list of Clients for customerId and searching by macSubstring.
[**update_client**](ClientsApi.md#update_client) | **PUT** /portal/client | Update Client

# **get_all_client_sessions_in_set**
> list[ClientSession] get_all_client_sessions_in_set(customer_id, client_macs)

Get list of Client sessions for customerId and a set of client MAC addresses.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
client_macs = ['client_macs_example'] # list[str] | Set of client MAC addresses.

try:
    # Get list of Client sessions for customerId and a set of client MAC addresses.
    api_response = api_instance.get_all_client_sessions_in_set(customer_id, client_macs)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->get_all_client_sessions_in_set: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **client_macs** | [**list[str]**](str.md)| Set of client MAC addresses. | 

### Return type

[**list[ClientSession]**](ClientSession.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_clients_in_set**
> list[Client] get_all_clients_in_set(customer_id, client_macs)

Get list of Clients for customerId and a set of client MAC addresses.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
client_macs = ['client_macs_example'] # list[str] | Set of client MAC addresses.

try:
    # Get list of Clients for customerId and a set of client MAC addresses.
    api_response = api_instance.get_all_clients_in_set(customer_id, client_macs)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->get_all_clients_in_set: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **client_macs** | [**list[str]**](str.md)| Set of client MAC addresses. | 

### Return type

[**list[Client]**](Client.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_blocked_clients**
> list[Client] get_blocked_clients(customer_id)

Retrieves a list of Clients for the customer that are marked as blocked. This per-customer list of blocked clients is pushed to every AP, so it has to be limited in size.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | Customer ID

try:
    # Retrieves a list of Clients for the customer that are marked as blocked. This per-customer list of blocked clients is pushed to every AP, so it has to be limited in size.
    api_response = api_instance.get_blocked_clients(customer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->get_blocked_clients: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| Customer ID | 

### Return type

[**list[Client]**](Client.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_client_session_by_customer_with_filter**
> PaginationResponseClientSession get_client_session_by_customer_with_filter(customer_id, pagination_context, equipment_ids=equipment_ids, location_ids=location_ids, sort_by=sort_by)

Get list of Client sessions for customerId and a set of equipment/location ids. Equipment and locations filters are joined using logical AND operation.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextClientSession() # PaginationContextClientSession | pagination context
equipment_ids = [56] # list[int] | set of equipment ids. Empty or null means retrieve all equipment for the customer. (optional)
location_ids = [56] # list[int] | set of location ids. Empty or null means retrieve for all locations for the customer. (optional)
sort_by = [swagger_client.SortColumnsClientSession()] # list[SortColumnsClientSession] | sort options (optional)

try:
    # Get list of Client sessions for customerId and a set of equipment/location ids. Equipment and locations filters are joined using logical AND operation.
    api_response = api_instance.get_client_session_by_customer_with_filter(customer_id, pagination_context, equipment_ids=equipment_ids, location_ids=location_ids, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->get_client_session_by_customer_with_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextClientSession**](.md)| pagination context | 
 **equipment_ids** | [**list[int]**](int.md)| set of equipment ids. Empty or null means retrieve all equipment for the customer. | [optional] 
 **location_ids** | [**list[int]**](int.md)| set of location ids. Empty or null means retrieve for all locations for the customer. | [optional] 
 **sort_by** | [**list[SortColumnsClientSession]**](SortColumnsClientSession.md)| sort options | [optional] 

### Return type

[**PaginationResponseClientSession**](PaginationResponseClientSession.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_for_customer**
> PaginationResponseClient get_for_customer(customer_id, equipment_ids=equipment_ids, sort_by=sort_by, pagination_context=pagination_context)

Get list of clients for a given customer by equipment ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | Customer ID
equipment_ids = [56] # list[int] | Equipment ID (optional)
sort_by = [swagger_client.SortColumnsClient()] # list[SortColumnsClient] | sort options (optional)
pagination_context = swagger_client.PaginationContextClient() # PaginationContextClient | pagination context (optional)

try:
    # Get list of clients for a given customer by equipment ids
    api_response = api_instance.get_for_customer(customer_id, equipment_ids=equipment_ids, sort_by=sort_by, pagination_context=pagination_context)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->get_for_customer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| Customer ID | 
 **equipment_ids** | [**list[int]**](int.md)| Equipment ID | [optional] 
 **sort_by** | [**list[SortColumnsClient]**](SortColumnsClient.md)| sort options | [optional] 
 **pagination_context** | [**PaginationContextClient**](.md)| pagination context | [optional] 

### Return type

[**PaginationResponseClient**](PaginationResponseClient.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_by_mac_address**
> PaginationResponseClient search_by_mac_address(customer_id, mac_substring=mac_substring, sort_by=sort_by, pagination_context=pagination_context)

Get list of Clients for customerId and searching by macSubstring.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
mac_substring = 'mac_substring_example' # str | MacAddress search criteria (optional)
sort_by = [swagger_client.SortColumnsClient()] # list[SortColumnsClient] | sort options (optional)
pagination_context = swagger_client.PaginationContextClient() # PaginationContextClient | pagination context (optional)

try:
    # Get list of Clients for customerId and searching by macSubstring.
    api_response = api_instance.search_by_mac_address(customer_id, mac_substring=mac_substring, sort_by=sort_by, pagination_context=pagination_context)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->search_by_mac_address: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **mac_substring** | **str**| MacAddress search criteria | [optional] 
 **sort_by** | [**list[SortColumnsClient]**](SortColumnsClient.md)| sort options | [optional] 
 **pagination_context** | [**PaginationContextClient**](.md)| pagination context | [optional] 

### Return type

[**PaginationResponseClient**](PaginationResponseClient.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_client**
> Client update_client(body)

Update Client

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ClientsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Client() # Client | Client info

try:
    # Update Client
    api_response = api_instance.update_client(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ClientsApi->update_client: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Client**](Client.md)| Client info | 

### Return type

[**Client**](Client.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

