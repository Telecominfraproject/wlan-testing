# swagger_client.CustomerApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_customer_by_id**](CustomerApi.md#get_customer_by_id) | **GET** /portal/customer | Get Customer By Id
[**update_customer**](CustomerApi.md#update_customer) | **PUT** /portal/customer | Update Customer

# **get_customer_by_id**
> Customer get_customer_by_id(customer_id)

Get Customer By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.CustomerApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id

try:
    # Get Customer By Id
    api_response = api_instance.get_customer_by_id(customer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerApi->get_customer_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 

### Return type

[**Customer**](Customer.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_customer**
> Customer update_customer(body)

Update Customer

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.CustomerApi(swagger_client.ApiClient(configuration))
body = swagger_client.Customer() # Customer | customer info

try:
    # Update Customer
    api_response = api_instance.update_customer(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CustomerApi->update_customer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Customer**](Customer.md)| customer info | 

### Return type

[**Customer**](Customer.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

