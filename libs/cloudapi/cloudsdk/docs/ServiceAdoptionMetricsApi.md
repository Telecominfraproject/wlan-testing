# swagger_client.ServiceAdoptionMetricsApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_adoption_metrics_all_per_day**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_all_per_day) | **GET** /portal/adoptionMetrics/allPerDay | Get daily service adoption metrics for a given year
[**get_adoption_metrics_all_per_month**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_all_per_month) | **GET** /portal/adoptionMetrics/allPerMonth | Get monthly service adoption metrics for a given year
[**get_adoption_metrics_all_per_week**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_all_per_week) | **GET** /portal/adoptionMetrics/allPerWeek | Get weekly service adoption metrics for a given year
[**get_adoption_metrics_per_customer_per_day**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_per_customer_per_day) | **GET** /portal/adoptionMetrics/perCustomerPerDay | Get daily service adoption metrics for a given year aggregated by customer and filtered by specified customer ids
[**get_adoption_metrics_per_equipment_per_day**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_per_equipment_per_day) | **GET** /portal/adoptionMetrics/perEquipmentPerDay | Get daily service adoption metrics for a given year filtered by specified equipment ids
[**get_adoption_metrics_per_location_per_day**](ServiceAdoptionMetricsApi.md#get_adoption_metrics_per_location_per_day) | **GET** /portal/adoptionMetrics/perLocationPerDay | Get daily service adoption metrics for a given year aggregated by location and filtered by specified location ids

# **get_adoption_metrics_all_per_day**
> list[ServiceAdoptionMetrics] get_adoption_metrics_all_per_day(year)

Get daily service adoption metrics for a given year

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 

try:
    # Get daily service adoption metrics for a given year
    api_response = api_instance.get_adoption_metrics_all_per_day(year)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_all_per_day: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_adoption_metrics_all_per_month**
> list[ServiceAdoptionMetrics] get_adoption_metrics_all_per_month(year)

Get monthly service adoption metrics for a given year

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 

try:
    # Get monthly service adoption metrics for a given year
    api_response = api_instance.get_adoption_metrics_all_per_month(year)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_all_per_month: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_adoption_metrics_all_per_week**
> list[ServiceAdoptionMetrics] get_adoption_metrics_all_per_week(year)

Get weekly service adoption metrics for a given year

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 

try:
    # Get weekly service adoption metrics for a given year
    api_response = api_instance.get_adoption_metrics_all_per_week(year)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_all_per_week: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_adoption_metrics_per_customer_per_day**
> list[ServiceAdoptionMetrics] get_adoption_metrics_per_customer_per_day(year, customer_ids)

Get daily service adoption metrics for a given year aggregated by customer and filtered by specified customer ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 
customer_ids = [56] # list[int] | filter by customer ids.

try:
    # Get daily service adoption metrics for a given year aggregated by customer and filtered by specified customer ids
    api_response = api_instance.get_adoption_metrics_per_customer_per_day(year, customer_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_per_customer_per_day: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 
 **customer_ids** | [**list[int]**](int.md)| filter by customer ids. | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_adoption_metrics_per_equipment_per_day**
> list[ServiceAdoptionMetrics] get_adoption_metrics_per_equipment_per_day(year, equipment_ids)

Get daily service adoption metrics for a given year filtered by specified equipment ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 
equipment_ids = [56] # list[int] | filter by equipment ids.

try:
    # Get daily service adoption metrics for a given year filtered by specified equipment ids
    api_response = api_instance.get_adoption_metrics_per_equipment_per_day(year, equipment_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_per_equipment_per_day: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 
 **equipment_ids** | [**list[int]**](int.md)| filter by equipment ids. | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_adoption_metrics_per_location_per_day**
> list[ServiceAdoptionMetrics] get_adoption_metrics_per_location_per_day(year, location_ids)

Get daily service adoption metrics for a given year aggregated by location and filtered by specified location ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ServiceAdoptionMetricsApi(swagger_client.ApiClient(configuration))
year = 56 # int | 
location_ids = [56] # list[int] | filter by location ids.

try:
    # Get daily service adoption metrics for a given year aggregated by location and filtered by specified location ids
    api_response = api_instance.get_adoption_metrics_per_location_per_day(year, location_ids)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ServiceAdoptionMetricsApi->get_adoption_metrics_per_location_per_day: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **year** | **int**|  | 
 **location_ids** | [**list[int]**](int.md)| filter by location ids. | 

### Return type

[**list[ServiceAdoptionMetrics]**](ServiceAdoptionMetrics.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

