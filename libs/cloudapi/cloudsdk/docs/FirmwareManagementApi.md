# swagger_client.FirmwareManagementApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_customer_firmware_track_record**](FirmwareManagementApi.md#create_customer_firmware_track_record) | **POST** /portal/firmware/customerTrack | Create new CustomerFirmwareTrackRecord
[**create_firmware_track_record**](FirmwareManagementApi.md#create_firmware_track_record) | **POST** /portal/firmware/track | Create new FirmwareTrackRecord
[**create_firmware_version**](FirmwareManagementApi.md#create_firmware_version) | **POST** /portal/firmware/version | Create new FirmwareVersion
[**delete_customer_firmware_track_record**](FirmwareManagementApi.md#delete_customer_firmware_track_record) | **DELETE** /portal/firmware/customerTrack | Delete CustomerFirmwareTrackRecord
[**delete_firmware_track_assignment**](FirmwareManagementApi.md#delete_firmware_track_assignment) | **DELETE** /portal/firmware/trackAssignment | Delete FirmwareTrackAssignment
[**delete_firmware_track_record**](FirmwareManagementApi.md#delete_firmware_track_record) | **DELETE** /portal/firmware/track | Delete FirmwareTrackRecord
[**delete_firmware_version**](FirmwareManagementApi.md#delete_firmware_version) | **DELETE** /portal/firmware/version | Delete FirmwareVersion
[**get_customer_firmware_track_record**](FirmwareManagementApi.md#get_customer_firmware_track_record) | **GET** /portal/firmware/customerTrack | Get CustomerFirmwareTrackRecord By customerId
[**get_default_customer_track_setting**](FirmwareManagementApi.md#get_default_customer_track_setting) | **GET** /portal/firmware/customerTrack/default | Get default settings for handling automatic firmware upgrades
[**get_firmware_model_ids_by_equipment_type**](FirmwareManagementApi.md#get_firmware_model_ids_by_equipment_type) | **GET** /portal/firmware/model/byEquipmentType | Get equipment models from all known firmware versions filtered by equipmentType
[**get_firmware_track_assignment_details**](FirmwareManagementApi.md#get_firmware_track_assignment_details) | **GET** /portal/firmware/trackAssignment | Get FirmwareTrackAssignmentDetails for a given firmware track name
[**get_firmware_track_record**](FirmwareManagementApi.md#get_firmware_track_record) | **GET** /portal/firmware/track | Get FirmwareTrackRecord By Id
[**get_firmware_track_record_by_name**](FirmwareManagementApi.md#get_firmware_track_record_by_name) | **GET** /portal/firmware/track/byName | Get FirmwareTrackRecord By name
[**get_firmware_version**](FirmwareManagementApi.md#get_firmware_version) | **GET** /portal/firmware/version | Get FirmwareVersion By Id
[**get_firmware_version_by_equipment_type**](FirmwareManagementApi.md#get_firmware_version_by_equipment_type) | **GET** /portal/firmware/version/byEquipmentType | Get FirmwareVersions filtered by equipmentType and optional equipment model
[**get_firmware_version_by_name**](FirmwareManagementApi.md#get_firmware_version_by_name) | **GET** /portal/firmware/version/byName | Get FirmwareVersion By name
[**update_customer_firmware_track_record**](FirmwareManagementApi.md#update_customer_firmware_track_record) | **PUT** /portal/firmware/customerTrack | Update CustomerFirmwareTrackRecord
[**update_firmware_track_assignment_details**](FirmwareManagementApi.md#update_firmware_track_assignment_details) | **PUT** /portal/firmware/trackAssignment | Update FirmwareTrackAssignmentDetails
[**update_firmware_track_record**](FirmwareManagementApi.md#update_firmware_track_record) | **PUT** /portal/firmware/track | Update FirmwareTrackRecord
[**update_firmware_version**](FirmwareManagementApi.md#update_firmware_version) | **PUT** /portal/firmware/version | Update FirmwareVersion

# **create_customer_firmware_track_record**
> CustomerFirmwareTrackRecord create_customer_firmware_track_record(body)

Create new CustomerFirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.CustomerFirmwareTrackRecord() # CustomerFirmwareTrackRecord | CustomerFirmwareTrackRecord info

try:
    # Create new CustomerFirmwareTrackRecord
    api_response = api_instance.create_customer_firmware_track_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->create_customer_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)| CustomerFirmwareTrackRecord info | 

### Return type

[**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_firmware_track_record**
> FirmwareTrackRecord create_firmware_track_record(body)

Create new FirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.FirmwareTrackRecord() # FirmwareTrackRecord | FirmwareTrackRecord info

try:
    # Create new FirmwareTrackRecord
    api_response = api_instance.create_firmware_track_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->create_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FirmwareTrackRecord**](FirmwareTrackRecord.md)| FirmwareTrackRecord info | 

### Return type

[**FirmwareTrackRecord**](FirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_firmware_version**
> FirmwareVersion create_firmware_version(body)

Create new FirmwareVersion

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.FirmwareVersion() # FirmwareVersion | FirmwareVersion info

try:
    # Create new FirmwareVersion
    api_response = api_instance.create_firmware_version(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->create_firmware_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FirmwareVersion**](FirmwareVersion.md)| FirmwareVersion info | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_customer_firmware_track_record**
> CustomerFirmwareTrackRecord delete_customer_firmware_track_record(customer_id)

Delete CustomerFirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id

try:
    # Delete CustomerFirmwareTrackRecord
    api_response = api_instance.delete_customer_firmware_track_record(customer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->delete_customer_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 

### Return type

[**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_firmware_track_assignment**
> FirmwareTrackAssignmentDetails delete_firmware_track_assignment(firmware_track_id, firmware_version_id)

Delete FirmwareTrackAssignment

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_track_id = 789 # int | firmware track id
firmware_version_id = 789 # int | firmware version id

try:
    # Delete FirmwareTrackAssignment
    api_response = api_instance.delete_firmware_track_assignment(firmware_track_id, firmware_version_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->delete_firmware_track_assignment: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_track_id** | **int**| firmware track id | 
 **firmware_version_id** | **int**| firmware version id | 

### Return type

[**FirmwareTrackAssignmentDetails**](FirmwareTrackAssignmentDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_firmware_track_record**
> FirmwareTrackRecord delete_firmware_track_record(firmware_track_id)

Delete FirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_track_id = 789 # int | firmware track id

try:
    # Delete FirmwareTrackRecord
    api_response = api_instance.delete_firmware_track_record(firmware_track_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->delete_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_track_id** | **int**| firmware track id | 

### Return type

[**FirmwareTrackRecord**](FirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_firmware_version**
> FirmwareVersion delete_firmware_version(firmware_version_id)

Delete FirmwareVersion

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_version_id = 789 # int | firmwareVersion id

try:
    # Delete FirmwareVersion
    api_response = api_instance.delete_firmware_version(firmware_version_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->delete_firmware_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_version_id** | **int**| firmwareVersion id | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_customer_firmware_track_record**
> CustomerFirmwareTrackRecord get_customer_firmware_track_record(customer_id)

Get CustomerFirmwareTrackRecord By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | customer id

try:
    # Get CustomerFirmwareTrackRecord By customerId
    api_response = api_instance.get_customer_firmware_track_record(customer_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_customer_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 

### Return type

[**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_default_customer_track_setting**
> CustomerFirmwareTrackSettings get_default_customer_track_setting()

Get default settings for handling automatic firmware upgrades

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))

try:
    # Get default settings for handling automatic firmware upgrades
    api_response = api_instance.get_default_customer_track_setting()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_default_customer_track_setting: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**CustomerFirmwareTrackSettings**](CustomerFirmwareTrackSettings.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_model_ids_by_equipment_type**
> list[str] get_firmware_model_ids_by_equipment_type(equipment_type)

Get equipment models from all known firmware versions filtered by equipmentType

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
equipment_type = swagger_client.EquipmentType() # EquipmentType | 

try:
    # Get equipment models from all known firmware versions filtered by equipmentType
    api_response = api_instance.get_firmware_model_ids_by_equipment_type(equipment_type)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_model_ids_by_equipment_type: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_type** | [**EquipmentType**](.md)|  | 

### Return type

**list[str]**

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_track_assignment_details**
> list[FirmwareTrackAssignmentDetails] get_firmware_track_assignment_details(firmware_track_name)

Get FirmwareTrackAssignmentDetails for a given firmware track name

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_track_name = 'firmware_track_name_example' # str | firmware track name

try:
    # Get FirmwareTrackAssignmentDetails for a given firmware track name
    api_response = api_instance.get_firmware_track_assignment_details(firmware_track_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_track_assignment_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_track_name** | **str**| firmware track name | 

### Return type

[**list[FirmwareTrackAssignmentDetails]**](FirmwareTrackAssignmentDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_track_record**
> FirmwareTrackRecord get_firmware_track_record(firmware_track_id)

Get FirmwareTrackRecord By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_track_id = 789 # int | firmware track id

try:
    # Get FirmwareTrackRecord By Id
    api_response = api_instance.get_firmware_track_record(firmware_track_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_track_id** | **int**| firmware track id | 

### Return type

[**FirmwareTrackRecord**](FirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_track_record_by_name**
> FirmwareTrackRecord get_firmware_track_record_by_name(firmware_track_name)

Get FirmwareTrackRecord By name

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_track_name = 'firmware_track_name_example' # str | firmware track name

try:
    # Get FirmwareTrackRecord By name
    api_response = api_instance.get_firmware_track_record_by_name(firmware_track_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_track_record_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_track_name** | **str**| firmware track name | 

### Return type

[**FirmwareTrackRecord**](FirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_version**
> FirmwareVersion get_firmware_version(firmware_version_id)

Get FirmwareVersion By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_version_id = 789 # int | firmwareVersion id

try:
    # Get FirmwareVersion By Id
    api_response = api_instance.get_firmware_version(firmware_version_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_version_id** | **int**| firmwareVersion id | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_version_by_equipment_type**
> list[FirmwareVersion] get_firmware_version_by_equipment_type(equipment_type, model_id=model_id)

Get FirmwareVersions filtered by equipmentType and optional equipment model

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
equipment_type = swagger_client.EquipmentType() # EquipmentType | 
model_id = 'model_id_example' # str | optional filter by equipment model, if null - then firmware versions for all the equipment models are returned (optional)

try:
    # Get FirmwareVersions filtered by equipmentType and optional equipment model
    api_response = api_instance.get_firmware_version_by_equipment_type(equipment_type, model_id=model_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_version_by_equipment_type: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_type** | [**EquipmentType**](.md)|  | 
 **model_id** | **str**| optional filter by equipment model, if null - then firmware versions for all the equipment models are returned | [optional] 

### Return type

[**list[FirmwareVersion]**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_firmware_version_by_name**
> FirmwareVersion get_firmware_version_by_name(firmware_version_name)

Get FirmwareVersion By name

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
firmware_version_name = 'firmware_version_name_example' # str | firmwareVersion name

try:
    # Get FirmwareVersion By name
    api_response = api_instance.get_firmware_version_by_name(firmware_version_name)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->get_firmware_version_by_name: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **firmware_version_name** | **str**| firmwareVersion name | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_customer_firmware_track_record**
> CustomerFirmwareTrackRecord update_customer_firmware_track_record(body)

Update CustomerFirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.CustomerFirmwareTrackRecord() # CustomerFirmwareTrackRecord | CustomerFirmwareTrackRecord info

try:
    # Update CustomerFirmwareTrackRecord
    api_response = api_instance.update_customer_firmware_track_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->update_customer_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)| CustomerFirmwareTrackRecord info | 

### Return type

[**CustomerFirmwareTrackRecord**](CustomerFirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_firmware_track_assignment_details**
> FirmwareTrackAssignmentDetails update_firmware_track_assignment_details(body)

Update FirmwareTrackAssignmentDetails

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.FirmwareTrackAssignmentDetails() # FirmwareTrackAssignmentDetails | FirmwareTrackAssignmentDetails info

try:
    # Update FirmwareTrackAssignmentDetails
    api_response = api_instance.update_firmware_track_assignment_details(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->update_firmware_track_assignment_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FirmwareTrackAssignmentDetails**](FirmwareTrackAssignmentDetails.md)| FirmwareTrackAssignmentDetails info | 

### Return type

[**FirmwareTrackAssignmentDetails**](FirmwareTrackAssignmentDetails.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_firmware_track_record**
> FirmwareTrackRecord update_firmware_track_record(body)

Update FirmwareTrackRecord

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.FirmwareTrackRecord() # FirmwareTrackRecord | FirmwareTrackRecord info

try:
    # Update FirmwareTrackRecord
    api_response = api_instance.update_firmware_track_record(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->update_firmware_track_record: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FirmwareTrackRecord**](FirmwareTrackRecord.md)| FirmwareTrackRecord info | 

### Return type

[**FirmwareTrackRecord**](FirmwareTrackRecord.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_firmware_version**
> FirmwareVersion update_firmware_version(body)

Update FirmwareVersion

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.FirmwareManagementApi(swagger_client.ApiClient(configuration))
body = swagger_client.FirmwareVersion() # FirmwareVersion | FirmwareVersion info

try:
    # Update FirmwareVersion
    api_response = api_instance.update_firmware_version(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling FirmwareManagementApi->update_firmware_version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**FirmwareVersion**](FirmwareVersion.md)| FirmwareVersion info | 

### Return type

[**FirmwareVersion**](FirmwareVersion.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

