# swagger_client.FileServicesApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_binary_file**](FileServicesApi.md#download_binary_file) | **GET** /filestore/{fileName} | Download binary file.
[**upload_binary_file**](FileServicesApi.md#upload_binary_file) | **POST** /filestore/{fileName} | Upload binary file.

# **download_binary_file**
> str download_binary_file(file_name)

Download binary file.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FileServicesApi(swagger_client.ApiClient(configuration))
file_name = 'file_name_example' # str | File name to download. File/path delimiters not allowed.

try:
    # Download binary file.
    api_response = api_instance.download_binary_file(file_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FileServicesApi->download_binary_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_name** | **str**| File name to download. File/path delimiters not allowed. | 

### Return type

**str**

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/octet-stream, application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_binary_file**
> GenericResponse upload_binary_file(body, file_name)

Upload binary file.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FileServicesApi(swagger_client.ApiClient(configuration))
body = swagger_client.Object() # Object | Contents of binary file
file_name = 'file_name_example' # str | File name that is being uploaded. File/path delimiters not allowed.

try:
    # Upload binary file.
    api_response = api_instance.upload_binary_file(body, file_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FileServicesApi->upload_binary_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **Object**| Contents of binary file | 
 **file_name** | **str**| File name that is being uploaded. File/path delimiters not allowed. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

