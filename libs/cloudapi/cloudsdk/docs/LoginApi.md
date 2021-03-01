# swagger_client.LoginApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_access_token**](LoginApi.md#get_access_token) | **POST** /management/v1/oauth2/token | Get access token - to be used as Bearer token header for all other API requests.
[**portal_ping**](LoginApi.md#portal_ping) | **GET** /ping | Portal proces version info.

# **get_access_token**
> WebTokenResult get_access_token(body)

Get access token - to be used as Bearer token header for all other API requests.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LoginApi(swagger_client.ApiClient(configuration))
body = swagger_client.WebTokenRequest() # WebTokenRequest | User id and password

try:
    # Get access token - to be used as Bearer token header for all other API requests.
    api_response = api_instance.get_access_token(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->get_access_token: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**WebTokenRequest**](WebTokenRequest.md)| User id and password | 

### Return type

[**WebTokenResult**](WebTokenResult.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **portal_ping**
> PingResponse portal_ping()

Portal proces version info.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.LoginApi(swagger_client.ApiClient(configuration))

try:
    # Portal proces version info.
    api_response = api_instance.portal_ping()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LoginApi->portal_ping: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**PingResponse**](PingResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

