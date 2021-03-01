# swagger_client.ProfileApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_profile**](ProfileApi.md#create_profile) | **POST** /portal/profile | Create new Profile
[**delete_profile**](ProfileApi.md#delete_profile) | **DELETE** /portal/profile | Delete Profile
[**get_counts_of_equipment_that_use_profiles**](ProfileApi.md#get_counts_of_equipment_that_use_profiles) | **GET** /portal/profile/equipmentCounts | Get counts of equipment that use specified profiles
[**get_profile_by_id**](ProfileApi.md#get_profile_by_id) | **GET** /portal/profile | Get Profile By Id
[**get_profile_with_children**](ProfileApi.md#get_profile_with_children) | **GET** /portal/profile/withChildren | Get Profile and all its associated children
[**get_profiles_by_customer_id**](ProfileApi.md#get_profiles_by_customer_id) | **GET** /portal/profile/forCustomer | Get Profiles By customerId
[**get_profiles_by_set_of_ids**](ProfileApi.md#get_profiles_by_set_of_ids) | **GET** /portal/profile/inSet | Get Profiles By a set of ids
[**update_profile**](ProfileApi.md#update_profile) | **PUT** /portal/profile | Update Profile

# **create_profile**
> Profile create_profile(body)

Create new Profile

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
body = swagger_client.Profile() # Profile | profile info

try:
    # Create new Profile
    api_response = api_instance.create_profile(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->create_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Profile**](Profile.md)| profile info | 

### Return type

[**Profile**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_profile**
> Profile delete_profile(profile_id)

Delete Profile

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
profile_id = 789 # int | profile id

try:
    # Delete Profile
    api_response = api_instance.delete_profile(profile_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->delete_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **int**| profile id | 

### Return type

[**Profile**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_counts_of_equipment_that_use_profiles**
> list[PairLongLong] get_counts_of_equipment_that_use_profiles(profile_id_set)

Get counts of equipment that use specified profiles

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
profile_id_set = [56] # list[int] | set of profile ids

try:
    # Get counts of equipment that use specified profiles
    api_response = api_instance.get_counts_of_equipment_that_use_profiles(profile_id_set)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->get_counts_of_equipment_that_use_profiles: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id_set** | [**list[int]**](int.md)| set of profile ids | 

### Return type

[**list[PairLongLong]**](PairLongLong.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile_by_id**
> Profile get_profile_by_id(profile_id)

Get Profile By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
profile_id = 789 # int | profile id

try:
    # Get Profile By Id
    api_response = api_instance.get_profile_by_id(profile_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->get_profile_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **int**| profile id | 

### Return type

[**Profile**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile_with_children**
> list[Profile] get_profile_with_children(profile_id)

Get Profile and all its associated children

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
profile_id = 789 # int | 

try:
    # Get Profile and all its associated children
    api_response = api_instance.get_profile_with_children(profile_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->get_profile_with_children: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id** | **int**|  | 

### Return type

[**list[Profile]**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profiles_by_customer_id**
> PaginationResponseProfile get_profiles_by_customer_id(customer_id, pagination_context, profile_type=profile_type, name_substring=name_substring, sort_by=sort_by)

Get Profiles By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
customer_id = 789 # int | customer id
pagination_context = swagger_client.PaginationContextProfile() # PaginationContextProfile | pagination context
profile_type = swagger_client.ProfileType() # ProfileType | profile type (optional)
name_substring = 'name_substring_example' # str |  (optional)
sort_by = [swagger_client.SortColumnsProfile()] # list[SortColumnsProfile] | sort options (optional)

try:
    # Get Profiles By customerId
    api_response = api_instance.get_profiles_by_customer_id(customer_id, pagination_context, profile_type=profile_type, name_substring=name_substring, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->get_profiles_by_customer_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextProfile**](.md)| pagination context | 
 **profile_type** | [**ProfileType**](.md)| profile type | [optional] 
 **name_substring** | **str**|  | [optional] 
 **sort_by** | [**list[SortColumnsProfile]**](SortColumnsProfile.md)| sort options | [optional] 

### Return type

[**PaginationResponseProfile**](PaginationResponseProfile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profiles_by_set_of_ids**
> list[Profile] get_profiles_by_set_of_ids(profile_id_set)

Get Profiles By a set of ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
profile_id_set = [56] # list[int] | set of profile ids

try:
    # Get Profiles By a set of ids
    api_response = api_instance.get_profiles_by_set_of_ids(profile_id_set)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->get_profiles_by_set_of_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **profile_id_set** | [**list[int]**](int.md)| set of profile ids | 

### Return type

[**list[Profile]**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_profile**
> Profile update_profile(body)

Update Profile

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.ProfileApi(swagger_client.ApiClient(configuration))
body = swagger_client.Profile() # Profile | profile info

try:
    # Update Profile
    api_response = api_instance.update_profile(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ProfileApi->update_profile: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**Profile**](Profile.md)| profile info | 

### Return type

[**Profile**](Profile.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

