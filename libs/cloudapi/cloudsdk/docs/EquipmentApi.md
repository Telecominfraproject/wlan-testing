# swagger_client.EquipmentApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_equipment**](EquipmentApi.md#create_equipment) | **POST** /portal/equipment | Create new Equipment
[**delete_equipment**](EquipmentApi.md#delete_equipment) | **DELETE** /portal/equipment | Delete Equipment
[**get_default_equipment_details**](EquipmentApi.md#get_default_equipment_details) | **GET** /portal/equipment/defaultDetails | Get default values for Equipment details for a specific equipment type
[**get_equipment_by_customer_id**](EquipmentApi.md#get_equipment_by_customer_id) | **GET** /portal/equipment/forCustomer | Get Equipment By customerId
[**get_equipment_by_customer_with_filter**](EquipmentApi.md#get_equipment_by_customer_with_filter) | **GET** /portal/equipment/forCustomerWithFilter | Get Equipment for customerId, equipment type, and location id
[**get_equipment_by_id**](EquipmentApi.md#get_equipment_by_id) | **GET** /portal/equipment | Get Equipment By Id
[**get_equipment_by_set_of_ids**](EquipmentApi.md#get_equipment_by_set_of_ids) | **GET** /portal/equipment/inSet | Get Equipment By a set of ids
[**update_equipment**](EquipmentApi.md#update_equipment) | **PUT** /portal/equipment | Update Equipment
[**update_equipment_rrm_bulk**](EquipmentApi.md#update_equipment_rrm_bulk) | **PUT** /portal/equipment/rrmBulk | Update RRM related properties of Equipment in bulk

# **create_equipment**
> Equipment create_equipment(body)

Create new Equipment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
body = swagger_client.Equipment() # Equipment | equipment info

try:
    # Create new Equipment
    api_response = api_instance.create_equipment(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->create_equipment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Equipment**](Equipment.md)| equipment info | 

### Return type

[**Equipment**](Equipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_equipment**
> Equipment delete_equipment(equipment_id)

Delete Equipment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | equipment id

try:
    # Delete Equipment
    api_response = api_instance.delete_equipment(equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->delete_equipment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| equipment id | 

### Return type

[**Equipment**](Equipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_default_equipment_details**
> EquipmentDetails get_default_equipment_details(equipment_type=equipment_type)

Get default values for Equipment details for a specific equipment type

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
equipment_type = swagger_client.EquipmentType() # EquipmentType |  (optional)

try:
    # Get default values for Equipment details for a specific equipment type
    api_response = api_instance.get_default_equipment_details(equipment_type=equipment_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->get_default_equipment_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_type** | [**EquipmentType**](.md)|  | [optional] 

### Return type

[**EquipmentDetails**](EquipmentDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_equipment_by_customer_id**
> PaginationResponseEquipment get_equipment_by_customer_id(customer_id, pagination_context, sort_by=sort_by)

Get Equipment By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
customer_id = 789 # int | customer id
pagination_context = swagger_client.PaginationContextEquipment() # PaginationContextEquipment | pagination context
sort_by = [swagger_client.SortColumnsEquipment()] # list[SortColumnsEquipment] | sort options (optional)

try:
    # Get Equipment By customerId
    api_response = api_instance.get_equipment_by_customer_id(customer_id, pagination_context, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->get_equipment_by_customer_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextEquipment**](.md)| pagination context | 
 **sort_by** | [**list[SortColumnsEquipment]**](SortColumnsEquipment.md)| sort options | [optional] 

### Return type

[**PaginationResponseEquipment**](PaginationResponseEquipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_equipment_by_customer_with_filter**
> PaginationResponseEquipment get_equipment_by_customer_with_filter(customer_id, equipment_type=equipment_type, location_ids=location_ids, criteria=criteria, sort_by=sort_by, pagination_context=pagination_context)

Get Equipment for customerId, equipment type, and location id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
customer_id = 789 # int | customer id
equipment_type = swagger_client.EquipmentType() # EquipmentType | equipment type (optional)
location_ids = [56] # list[int] | set of location ids (optional)
criteria = 'criteria_example' # str | search criteria (optional)
sort_by = [swagger_client.SortColumnsEquipment()] # list[SortColumnsEquipment] | sort options (optional)
pagination_context = swagger_client.PaginationContextEquipment() # PaginationContextEquipment | pagination context (optional)

try:
    # Get Equipment for customerId, equipment type, and location id
    api_response = api_instance.get_equipment_by_customer_with_filter(customer_id, equipment_type=equipment_type, location_ids=location_ids, criteria=criteria, sort_by=sort_by, pagination_context=pagination_context)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->get_equipment_by_customer_with_filter: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **equipment_type** | [**EquipmentType**](.md)| equipment type | [optional] 
 **location_ids** | [**list[int]**](int.md)| set of location ids | [optional] 
 **criteria** | **str**| search criteria | [optional] 
 **sort_by** | [**list[SortColumnsEquipment]**](SortColumnsEquipment.md)| sort options | [optional] 
 **pagination_context** | [**PaginationContextEquipment**](.md)| pagination context | [optional] 

### Return type

[**PaginationResponseEquipment**](PaginationResponseEquipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_equipment_by_id**
> Equipment get_equipment_by_id(equipment_id)

Get Equipment By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | equipment id

try:
    # Get Equipment By Id
    api_response = api_instance.get_equipment_by_id(equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->get_equipment_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| equipment id | 

### Return type

[**Equipment**](Equipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_equipment_by_set_of_ids**
> list[Equipment] get_equipment_by_set_of_ids(equipment_id_set)

Get Equipment By a set of ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
equipment_id_set = [56] # list[int] | set of equipment ids

try:
    # Get Equipment By a set of ids
    api_response = api_instance.get_equipment_by_set_of_ids(equipment_id_set)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->get_equipment_by_set_of_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id_set** | [**list[int]**](int.md)| set of equipment ids | 

### Return type

[**list[Equipment]**](Equipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_equipment**
> Equipment update_equipment(body)

Update Equipment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
body = swagger_client.Equipment() # Equipment | equipment info

try:
    # Update Equipment
    api_response = api_instance.update_equipment(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->update_equipment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Equipment**](Equipment.md)| equipment info | 

### Return type

[**Equipment**](Equipment.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_equipment_rrm_bulk**
> GenericResponse update_equipment_rrm_bulk(body)

Update RRM related properties of Equipment in bulk

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentApi(swagger_client.ApiClient(configuration))
body = swagger_client.EquipmentRrmBulkUpdateRequest() # EquipmentRrmBulkUpdateRequest | Equipment RRM bulk update request

try:
    # Update RRM related properties of Equipment in bulk
    api_response = api_instance.update_equipment_rrm_bulk(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentApi->update_equipment_rrm_bulk: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**EquipmentRrmBulkUpdateRequest**](EquipmentRrmBulkUpdateRequest.md)| Equipment RRM bulk update request | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

