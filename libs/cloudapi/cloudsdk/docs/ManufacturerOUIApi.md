# swagger_client.ManufacturerOUIApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_manufacturer_details_record**](ManufacturerOUIApi.md#create_manufacturer_details_record) | **POST** /portal/manufacturer | Create new ManufacturerDetailsRecord
[**create_manufacturer_oui_details**](ManufacturerOUIApi.md#create_manufacturer_oui_details) | **POST** /portal/manufacturer/oui | Create new ManufacturerOuiDetails
[**delete_manufacturer_details_record**](ManufacturerOUIApi.md#delete_manufacturer_details_record) | **DELETE** /portal/manufacturer | Delete ManufacturerDetailsRecord
[**delete_manufacturer_oui_details**](ManufacturerOUIApi.md#delete_manufacturer_oui_details) | **DELETE** /portal/manufacturer/oui | Delete ManufacturerOuiDetails
[**get_alias_values_that_begin_with**](ManufacturerOUIApi.md#get_alias_values_that_begin_with) | **GET** /portal/manufacturer/oui/alias | Get manufacturer aliases that begin with the given prefix
[**get_all_manufacturer_oui_details**](ManufacturerOUIApi.md#get_all_manufacturer_oui_details) | **GET** /portal/manufacturer/oui/all | Get all ManufacturerOuiDetails
[**get_manufacturer_details_for_oui_list**](ManufacturerOUIApi.md#get_manufacturer_details_for_oui_list) | **GET** /portal/manufacturer/oui/list | Get ManufacturerOuiDetails for the list of OUIs
[**get_manufacturer_details_record**](ManufacturerOUIApi.md#get_manufacturer_details_record) | **GET** /portal/manufacturer | Get ManufacturerDetailsRecord By id
[**get_manufacturer_oui_details_by_oui**](ManufacturerOUIApi.md#get_manufacturer_oui_details_by_oui) | **GET** /portal/manufacturer/oui | Get ManufacturerOuiDetails By oui
[**get_oui_list_for_manufacturer**](ManufacturerOUIApi.md#get_oui_list_for_manufacturer) | **GET** /portal/manufacturer/oui/forManufacturer | Get Oui List for manufacturer
[**update_manufacturer_details_record**](ManufacturerOUIApi.md#update_manufacturer_details_record) | **PUT** /portal/manufacturer | Update ManufacturerDetailsRecord
[**update_oui_alias**](ManufacturerOUIApi.md#update_oui_alias) | **PUT** /portal/manufacturer/oui/alias | Update alias for ManufacturerOuiDetails
[**upload_oui_data_file**](ManufacturerOUIApi.md#upload_oui_data_file) | **POST** /portal/manufacturer/oui/upload | Upload the gziped OUI DataFile, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/
[**upload_oui_data_file_base64**](ManufacturerOUIApi.md#upload_oui_data_file_base64) | **POST** /portal/manufacturer/oui/upload/base64 | Upload the gziped OUI DataFile using base64 encoding, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/

# **create_manufacturer_details_record**
> ManufacturerDetailsRecord create_manufacturer_details_record(body)

Create new ManufacturerDetailsRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = swagger_client.ManufacturerDetailsRecord() # ManufacturerDetailsRecord | ManufacturerDetailsRecord info

try:
    # Create new ManufacturerDetailsRecord
    api_response = api_instance.create_manufacturer_details_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->create_manufacturer_details_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)| ManufacturerDetailsRecord info | 

### Return type

[**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_manufacturer_oui_details**
> ManufacturerOuiDetails create_manufacturer_oui_details(body)

Create new ManufacturerOuiDetails

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = swagger_client.ManufacturerOuiDetails() # ManufacturerOuiDetails | ManufacturerOuiDetails info

try:
    # Create new ManufacturerOuiDetails
    api_response = api_instance.create_manufacturer_oui_details(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->create_manufacturer_oui_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)| ManufacturerOuiDetails info | 

### Return type

[**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_manufacturer_details_record**
> ManufacturerDetailsRecord delete_manufacturer_details_record(id)

Delete ManufacturerDetailsRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
id = 789 # int | ManufacturerDetailsRecord id

try:
    # Delete ManufacturerDetailsRecord
    api_response = api_instance.delete_manufacturer_details_record(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->delete_manufacturer_details_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| ManufacturerDetailsRecord id | 

### Return type

[**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_manufacturer_oui_details**
> ManufacturerOuiDetails delete_manufacturer_oui_details(oui)

Delete ManufacturerOuiDetails

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
oui = 'oui_example' # str | ManufacturerOuiDetails oui

try:
    # Delete ManufacturerOuiDetails
    api_response = api_instance.delete_manufacturer_oui_details(oui)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->delete_manufacturer_oui_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oui** | **str**| ManufacturerOuiDetails oui | 

### Return type

[**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_alias_values_that_begin_with**
> list[str] get_alias_values_that_begin_with(prefix, max_results)

Get manufacturer aliases that begin with the given prefix

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
prefix = 'prefix_example' # str | prefix for the manufacturer alias
max_results = -1 # int | max results to return, use -1 for no limit (default to -1)

try:
    # Get manufacturer aliases that begin with the given prefix
    api_response = api_instance.get_alias_values_that_begin_with(prefix, max_results)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_alias_values_that_begin_with: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prefix** | **str**| prefix for the manufacturer alias | 
 **max_results** | **int**| max results to return, use -1 for no limit | [default to -1]

### Return type

**list[str]**

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_manufacturer_oui_details**
> list[ManufacturerOuiDetails] get_all_manufacturer_oui_details()

Get all ManufacturerOuiDetails

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))

try:
    # Get all ManufacturerOuiDetails
    api_response = api_instance.get_all_manufacturer_oui_details()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_all_manufacturer_oui_details: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[ManufacturerOuiDetails]**](ManufacturerOuiDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_manufacturer_details_for_oui_list**
> ManufacturerOuiDetailsPerOuiMap get_manufacturer_details_for_oui_list(oui_list)

Get ManufacturerOuiDetails for the list of OUIs

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
oui_list = ['oui_list_example'] # list[str] | 

try:
    # Get ManufacturerOuiDetails for the list of OUIs
    api_response = api_instance.get_manufacturer_details_for_oui_list(oui_list)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_manufacturer_details_for_oui_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oui_list** | [**list[str]**](str.md)|  | 

### Return type

[**ManufacturerOuiDetailsPerOuiMap**](ManufacturerOuiDetailsPerOuiMap.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_manufacturer_details_record**
> ManufacturerDetailsRecord get_manufacturer_details_record(id)

Get ManufacturerDetailsRecord By id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
id = 789 # int | ManufacturerDetailsRecord id

try:
    # Get ManufacturerDetailsRecord By id
    api_response = api_instance.get_manufacturer_details_record(id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_manufacturer_details_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| ManufacturerDetailsRecord id | 

### Return type

[**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_manufacturer_oui_details_by_oui**
> ManufacturerOuiDetails get_manufacturer_oui_details_by_oui(oui)

Get ManufacturerOuiDetails By oui

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
oui = 'oui_example' # str | ManufacturerOuiDetails oui

try:
    # Get ManufacturerOuiDetails By oui
    api_response = api_instance.get_manufacturer_oui_details_by_oui(oui)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_manufacturer_oui_details_by_oui: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **oui** | **str**| ManufacturerOuiDetails oui | 

### Return type

[**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_oui_list_for_manufacturer**
> list[str] get_oui_list_for_manufacturer(manufacturer, exact_match)

Get Oui List for manufacturer

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
manufacturer = 'manufacturer_example' # str | Manufacturer name or alias
exact_match = true # bool | Perform exact match (true) or prefix match (false) for the manufacturer name or alias

try:
    # Get Oui List for manufacturer
    api_response = api_instance.get_oui_list_for_manufacturer(manufacturer, exact_match)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->get_oui_list_for_manufacturer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **manufacturer** | **str**| Manufacturer name or alias | 
 **exact_match** | **bool**| Perform exact match (true) or prefix match (false) for the manufacturer name or alias | 

### Return type

**list[str]**

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_manufacturer_details_record**
> ManufacturerDetailsRecord update_manufacturer_details_record(body)

Update ManufacturerDetailsRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = swagger_client.ManufacturerDetailsRecord() # ManufacturerDetailsRecord | ManufacturerDetailsRecord info

try:
    # Update ManufacturerDetailsRecord
    api_response = api_instance.update_manufacturer_details_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->update_manufacturer_details_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)| ManufacturerDetailsRecord info | 

### Return type

[**ManufacturerDetailsRecord**](ManufacturerDetailsRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_oui_alias**
> ManufacturerOuiDetails update_oui_alias(body)

Update alias for ManufacturerOuiDetails

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = swagger_client.ManufacturerOuiDetails() # ManufacturerOuiDetails | ManufacturerOuiDetails info

try:
    # Update alias for ManufacturerOuiDetails
    api_response = api_instance.update_oui_alias(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->update_oui_alias: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)| ManufacturerOuiDetails info | 

### Return type

[**ManufacturerOuiDetails**](ManufacturerOuiDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_oui_data_file**
> GenericResponse upload_oui_data_file(body, file_name)

Upload the gziped OUI DataFile, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = swagger_client.Object() # Object | Contents of gziped OUI DataFile, raw
file_name = 'file_name_example' # str | file name that is being uploaded

try:
    # Upload the gziped OUI DataFile, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/
    api_response = api_instance.upload_oui_data_file(body, file_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->upload_oui_data_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | **Object**| Contents of gziped OUI DataFile, raw | 
 **file_name** | **str**| file name that is being uploaded | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_oui_data_file_base64**
> GenericResponse upload_oui_data_file_base64(body, file_name)

Upload the gziped OUI DataFile using base64 encoding, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ManufacturerOUIApi(swagger_client.ApiClient(configuration))
body = 'body_example' # str | Contents of gziped OUI DataFile, base64-encoded
file_name = 'file_name_example' # str | file name that is being uploaded

try:
    # Upload the gziped OUI DataFile using base64 encoding, in the format that is published by IEEE. Latest sanitized IEEE OUI data file (oui.txt.gz) can be obtained from https://linuxnet.ca/ieee/oui/
    api_response = api_instance.upload_oui_data_file_base64(body, file_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ManufacturerOUIApi->upload_oui_data_file_base64: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**str**](str.md)| Contents of gziped OUI DataFile, base64-encoded | 
 **file_name** | **str**| file name that is being uploaded | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/octet-stream
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

