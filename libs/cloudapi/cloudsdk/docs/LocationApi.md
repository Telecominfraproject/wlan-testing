# swagger_client.LocationApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_location**](LocationApi.md#create_location) | **POST** /portal/location | Create new Location
[**delete_location**](LocationApi.md#delete_location) | **DELETE** /portal/location | Delete Location
[**get_location_by_id**](LocationApi.md#get_location_by_id) | **GET** /portal/location | Get Location By Id
[**get_location_by_set_of_ids**](LocationApi.md#get_location_by_set_of_ids) | **GET** /portal/location/inSet | Get Locations By a set of ids
[**get_locations_by_customer_id**](LocationApi.md#get_locations_by_customer_id) | **GET** /portal/location/forCustomer | Get Locations By customerId
[**update_location**](LocationApi.md#update_location) | **PUT** /portal/location | Update Location

# **create_location**
> Location create_location(body)

Create new Location

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
body = swagger_client.Location() # Location | location info

try:
    # Create new Location
    api_response = api_instance.create_location(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->create_location: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Location**](Location.md)| location info | 

### Return type

[**Location**](Location.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_location**
> Location delete_location(location_id)

Delete Location

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
location_id = 789 # int | location id

try:
    # Delete Location
    api_response = api_instance.delete_location(location_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->delete_location: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **location_id** | **int**| location id | 

### Return type

[**Location**](Location.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_location_by_id**
> Location get_location_by_id(location_id)

Get Location By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
location_id = 789 # int | location id

try:
    # Get Location By Id
    api_response = api_instance.get_location_by_id(location_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->get_location_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **location_id** | **int**| location id | 

### Return type

[**Location**](Location.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_location_by_set_of_ids**
> list[Location] get_location_by_set_of_ids(location_id_set)

Get Locations By a set of ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
location_id_set = [56] # list[int] | set of location ids

try:
    # Get Locations By a set of ids
    api_response = api_instance.get_location_by_set_of_ids(location_id_set)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->get_location_by_set_of_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **location_id_set** | [**list[int]**](int.md)| set of location ids | 

### Return type

[**list[Location]**](Location.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_locations_by_customer_id**
> PaginationResponseLocation get_locations_by_customer_id(customer_id, pagination_context, sort_by=sort_by)

Get Locations By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
customer_id = 789 # int | customer id
pagination_context = swagger_client.PaginationContextLocation() # PaginationContextLocation | pagination context
sort_by = [swagger_client.SortColumnsLocation()] # list[SortColumnsLocation] | sort options (optional)

try:
    # Get Locations By customerId
    api_response = api_instance.get_locations_by_customer_id(customer_id, pagination_context, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->get_locations_by_customer_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextLocation**](.md)| pagination context | 
 **sort_by** | [**list[SortColumnsLocation]**](SortColumnsLocation.md)| sort options | [optional] 

### Return type

[**PaginationResponseLocation**](PaginationResponseLocation.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_location**
> Location update_location(body)

Update Location

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LocationApi(swagger_client.ApiClient(configuration))
body = swagger_client.Location() # Location | location info

try:
    # Update Location
    api_response = api_instance.update_location(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LocationApi->update_location: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Location**](Location.md)| location info | 

### Return type

[**Location**](Location.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

