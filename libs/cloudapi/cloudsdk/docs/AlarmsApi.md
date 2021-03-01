# swagger_client.AlarmsApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_alarm**](AlarmsApi.md#delete_alarm) | **DELETE** /portal/alarm | Delete Alarm
[**get_alarm_counts**](AlarmsApi.md#get_alarm_counts) | **GET** /portal/alarm/counts | Get counts of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.
[**get_alarmsfor_customer**](AlarmsApi.md#get_alarmsfor_customer) | **GET** /portal/alarm/forCustomer | Get list of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.
[**get_alarmsfor_equipment**](AlarmsApi.md#get_alarmsfor_equipment) | **GET** /portal/alarm/forEquipment | Get list of Alarms for customerId, set of equipment ids, and set of alarm codes.
[**reset_alarm_counts**](AlarmsApi.md#reset_alarm_counts) | **POST** /portal/alarm/resetCounts | Reset accumulated counts of Alarms.
[**update_alarm**](AlarmsApi.md#update_alarm) | **PUT** /portal/alarm | Update Alarm

# **delete_alarm**
> Alarm delete_alarm(customer_id, equipment_id, alarm_code, created_timestamp)

Delete Alarm

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | 
equipment_id = 789 # int | 
alarm_code = swagger_client.AlarmCode() # AlarmCode | 
created_timestamp = 789 # int | 

try:
    # Delete Alarm
    api_response = api_instance.delete_alarm(customer_id, equipment_id, alarm_code, created_timestamp)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->delete_alarm: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**|  | 
 **equipment_id** | **int**|  | 
 **alarm_code** | [**AlarmCode**](.md)|  | 
 **created_timestamp** | **int**|  | 

### Return type

[**Alarm**](Alarm.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_alarm_counts**
> AlarmCounts get_alarm_counts(customer_id, equipment_ids=equipment_ids, alarm_codes=alarm_codes)

Get counts of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
equipment_ids = [56] # list[int] | Set of equipment ids. Empty or null means retrieve for all equipment for the customer. (optional)
alarm_codes = [swagger_client.AlarmCode()] # list[AlarmCode] | Set of alarm codes. Empty or null means retrieve all. (optional)

try:
    # Get counts of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.
    api_response = api_instance.get_alarm_counts(customer_id, equipment_ids=equipment_ids, alarm_codes=alarm_codes)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->get_alarm_counts: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Empty or null means retrieve for all equipment for the customer. | [optional] 
 **alarm_codes** | [**list[AlarmCode]**](AlarmCode.md)| Set of alarm codes. Empty or null means retrieve all. | [optional] 

### Return type

[**AlarmCounts**](AlarmCounts.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_alarmsfor_customer**
> PaginationResponseAlarm get_alarmsfor_customer(customer_id, pagination_context, equipment_ids=equipment_ids, alarm_codes=alarm_codes, created_after_timestamp=created_after_timestamp, sort_by=sort_by)

Get list of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
pagination_context = swagger_client.PaginationContextAlarm() # PaginationContextAlarm | pagination context
equipment_ids = [56] # list[int] | Set of equipment ids. Empty or null means retrieve all equipment for the customer. (optional)
alarm_codes = [swagger_client.AlarmCode()] # list[AlarmCode] | Set of alarm codes. Empty or null means retrieve all. (optional)
created_after_timestamp = -1 # int | retrieve alarms created after the specified time (optional) (default to -1)
sort_by = [swagger_client.SortColumnsAlarm()] # list[SortColumnsAlarm] | sort options (optional)

try:
    # Get list of Alarms for customerId, optional set of equipment ids, optional set of alarm codes.
    api_response = api_instance.get_alarmsfor_customer(customer_id, pagination_context, equipment_ids=equipment_ids, alarm_codes=alarm_codes, created_after_timestamp=created_after_timestamp, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->get_alarmsfor_customer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextAlarm**](.md)| pagination context | 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Empty or null means retrieve all equipment for the customer. | [optional] 
 **alarm_codes** | [**list[AlarmCode]**](AlarmCode.md)| Set of alarm codes. Empty or null means retrieve all. | [optional] 
 **created_after_timestamp** | **int**| retrieve alarms created after the specified time | [optional] [default to -1]
 **sort_by** | [**list[SortColumnsAlarm]**](SortColumnsAlarm.md)| sort options | [optional] 

### Return type

[**PaginationResponseAlarm**](PaginationResponseAlarm.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_alarmsfor_equipment**
> list[Alarm] get_alarmsfor_equipment(customer_id, equipment_ids, alarm_codes=alarm_codes, created_after_timestamp=created_after_timestamp)

Get list of Alarms for customerId, set of equipment ids, and set of alarm codes.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id
equipment_ids = [56] # list[int] | Set of equipment ids. Must not be empty.
alarm_codes = [swagger_client.AlarmCode()] # list[AlarmCode] | Set of alarm codes. Empty or null means retrieve all. (optional)
created_after_timestamp = -1 # int | retrieve alarms created after the specified time (optional) (default to -1)

try:
    # Get list of Alarms for customerId, set of equipment ids, and set of alarm codes.
    api_response = api_instance.get_alarmsfor_equipment(customer_id, equipment_ids, alarm_codes=alarm_codes, created_after_timestamp=created_after_timestamp)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->get_alarmsfor_equipment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **equipment_ids** | [**list[int]**](int.md)| Set of equipment ids. Must not be empty. | 
 **alarm_codes** | [**list[AlarmCode]**](AlarmCode.md)| Set of alarm codes. Empty or null means retrieve all. | [optional] 
 **created_after_timestamp** | **int**| retrieve alarms created after the specified time | [optional] [default to -1]

### Return type

[**list[Alarm]**](Alarm.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reset_alarm_counts**
> GenericResponse reset_alarm_counts()

Reset accumulated counts of Alarms.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))

try:
    # Reset accumulated counts of Alarms.
    api_response = api_instance.reset_alarm_counts()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->reset_alarm_counts: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_alarm**
> Alarm update_alarm(body)

Update Alarm

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.AlarmsApi(swagger_client.ApiClient(configuration))
body = swagger_client.Alarm() # Alarm | Alarm info

try:
    # Update Alarm
    api_response = api_instance.update_alarm(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling AlarmsApi->update_alarm: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Alarm**](Alarm.md)| Alarm info | 

### Return type

[**Alarm**](Alarm.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

