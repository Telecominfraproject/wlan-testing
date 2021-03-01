# swagger_client.EquipmentGatewayApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**request_ap_factory_reset**](EquipmentGatewayApi.md#request_ap_factory_reset) | **POST** /portal/equipmentGateway/requestApFactoryReset | Request factory reset for a particular equipment.
[**request_ap_reboot**](EquipmentGatewayApi.md#request_ap_reboot) | **POST** /portal/equipmentGateway/requestApReboot | Request reboot for a particular equipment.
[**request_ap_switch_software_bank**](EquipmentGatewayApi.md#request_ap_switch_software_bank) | **POST** /portal/equipmentGateway/requestApSwitchSoftwareBank | Request switch of active/inactive sw bank for a particular equipment.
[**request_channel_change**](EquipmentGatewayApi.md#request_channel_change) | **POST** /portal/equipmentGateway/requestChannelChange | Request change of primary and/or backup channels for given frequency bands.
[**request_firmware_update**](EquipmentGatewayApi.md#request_firmware_update) | **POST** /portal/equipmentGateway/requestFirmwareUpdate | Request firmware update for a particular equipment.

# **request_ap_factory_reset**
> GenericResponse request_ap_factory_reset(equipment_id)

Request factory reset for a particular equipment.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentGatewayApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | Equipment id for which the factory reset is being requested.

try:
    # Request factory reset for a particular equipment.
    api_response = api_instance.request_ap_factory_reset(equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentGatewayApi->request_ap_factory_reset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| Equipment id for which the factory reset is being requested. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_ap_reboot**
> GenericResponse request_ap_reboot(equipment_id)

Request reboot for a particular equipment.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentGatewayApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | Equipment id for which the reboot is being requested.

try:
    # Request reboot for a particular equipment.
    api_response = api_instance.request_ap_reboot(equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentGatewayApi->request_ap_reboot: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| Equipment id for which the reboot is being requested. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_ap_switch_software_bank**
> GenericResponse request_ap_switch_software_bank(equipment_id)

Request switch of active/inactive sw bank for a particular equipment.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentGatewayApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | Equipment id for which the switch is being requested.

try:
    # Request switch of active/inactive sw bank for a particular equipment.
    api_response = api_instance.request_ap_switch_software_bank(equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentGatewayApi->request_ap_switch_software_bank: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| Equipment id for which the switch is being requested. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_channel_change**
> GenericResponse request_channel_change(body, equipment_id)

Request change of primary and/or backup channels for given frequency bands.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentGatewayApi(swagger_client.ApiClient(configuration))
body = swagger_client.RadioChannelChangeSettings() # RadioChannelChangeSettings | RadioChannelChangeSettings info
equipment_id = 789 # int | Equipment id for which the channel changes are being performed.

try:
    # Request change of primary and/or backup channels for given frequency bands.
    api_response = api_instance.request_channel_change(body, equipment_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentGatewayApi->request_channel_change: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RadioChannelChangeSettings**](RadioChannelChangeSettings.md)| RadioChannelChangeSettings info | 
 **equipment_id** | **int**| Equipment id for which the channel changes are being performed. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **request_firmware_update**
> GenericResponse request_firmware_update(equipment_id, firmware_version_id)

Request firmware update for a particular equipment.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.EquipmentGatewayApi(swagger_client.ApiClient(configuration))
equipment_id = 789 # int | Equipment id for which the firmware update is being requested.
firmware_version_id = 789 # int | Id of the firmware version object.

try:
    # Request firmware update for a particular equipment.
    api_response = api_instance.request_firmware_update(equipment_id, firmware_version_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling EquipmentGatewayApi->request_firmware_update: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **equipment_id** | **int**| Equipment id for which the firmware update is being requested. | 
 **firmware_version_id** | **int**| Id of the firmware version object. | 

### Return type

[**GenericResponse**](GenericResponse.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

