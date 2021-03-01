# swagger_client.PortalUsersApi

All URIs are relative to *https://localhost:9091*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_portal_user**](PortalUsersApi.md#create_portal_user) | **POST** /portal/portalUser | Create new Portal User
[**delete_portal_user**](PortalUsersApi.md#delete_portal_user) | **DELETE** /portal/portalUser | Delete PortalUser
[**get_portal_user_by_id**](PortalUsersApi.md#get_portal_user_by_id) | **GET** /portal/portalUser | Get portal user By Id
[**get_portal_user_by_username**](PortalUsersApi.md#get_portal_user_by_username) | **GET** /portal/portalUser/byUsernameOrNull | Get portal user by user name
[**get_portal_users_by_customer_id**](PortalUsersApi.md#get_portal_users_by_customer_id) | **GET** /portal/portalUser/forCustomer | Get PortalUsers By customerId
[**get_portal_users_by_set_of_ids**](PortalUsersApi.md#get_portal_users_by_set_of_ids) | **GET** /portal/portalUser/inSet | Get PortalUsers By a set of ids
[**get_users_for_username**](PortalUsersApi.md#get_users_for_username) | **GET** /portal/portalUser/usersForUsername | Get Portal Users for username
[**update_portal_user**](PortalUsersApi.md#update_portal_user) | **PUT** /portal/portalUser | Update PortalUser

# **create_portal_user**
> PortalUser create_portal_user(body)

Create new Portal User

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.PortalUser() # PortalUser | portal user info

try:
    # Create new Portal User
    api_response = api_instance.create_portal_user(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->create_portal_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PortalUser**](PortalUser.md)| portal user info | 

### Return type

[**PortalUser**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_portal_user**
> PortalUser delete_portal_user(portal_user_id)

Delete PortalUser

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
portal_user_id = 789 # int | 

try:
    # Delete PortalUser
    api_response = api_instance.delete_portal_user(portal_user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->delete_portal_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portal_user_id** | **int**|  | 

### Return type

[**PortalUser**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portal_user_by_id**
> PortalUser get_portal_user_by_id(portal_user_id)

Get portal user By Id

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
portal_user_id = 789 # int | 

try:
    # Get portal user By Id
    api_response = api_instance.get_portal_user_by_id(portal_user_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->get_portal_user_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portal_user_id** | **int**|  | 

### Return type

[**PortalUser**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portal_user_by_username**
> PortalUser get_portal_user_by_username(customer_id, username)

Get portal user by user name

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
customer_id = 56 # int | 
username = 'username_example' # str | 

try:
    # Get portal user by user name
    api_response = api_instance.get_portal_user_by_username(customer_id, username)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->get_portal_user_by_username: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**|  | 
 **username** | **str**|  | 

### Return type

[**PortalUser**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portal_users_by_customer_id**
> PaginationResponsePortalUser get_portal_users_by_customer_id(customer_id, pagination_context, sort_by=sort_by)

Get PortalUsers By customerId

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
customer_id = 789 # int | customer id
pagination_context = swagger_client.PaginationContextPortalUser() # PaginationContextPortalUser | pagination context
sort_by = [swagger_client.SortColumnsPortalUser()] # list[SortColumnsPortalUser] | sort options (optional)

try:
    # Get PortalUsers By customerId
    api_response = api_instance.get_portal_users_by_customer_id(customer_id, pagination_context, sort_by=sort_by)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->get_portal_users_by_customer_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **customer_id** | **int**| customer id | 
 **pagination_context** | [**PaginationContextPortalUser**](.md)| pagination context | 
 **sort_by** | [**list[SortColumnsPortalUser]**](SortColumnsPortalUser.md)| sort options | [optional] 

### Return type

[**PaginationResponsePortalUser**](PaginationResponsePortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portal_users_by_set_of_ids**
> list[PortalUser] get_portal_users_by_set_of_ids(portal_user_id_set)

Get PortalUsers By a set of ids

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
portal_user_id_set = [56] # list[int] | set of portalUser ids

try:
    # Get PortalUsers By a set of ids
    api_response = api_instance.get_portal_users_by_set_of_ids(portal_user_id_set)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->get_portal_users_by_set_of_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **portal_user_id_set** | [**list[int]**](int.md)| set of portalUser ids | 

### Return type

[**list[PortalUser]**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_for_username**
> list[PortalUser] get_users_for_username(username)

Get Portal Users for username

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
username = 'username_example' # str | 

try:
    # Get Portal Users for username
    api_response = api_instance.get_users_for_username(username)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->get_users_for_username: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **username** | **str**|  | 

### Return type

[**list[PortalUser]**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_portal_user**
> PortalUser update_portal_user(body)

Update PortalUser

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.PortalUsersApi(swagger_client.ApiClient(configuration))
body = swagger_client.PortalUser() # PortalUser | PortalUser info

try:
    # Update PortalUser
    api_response = api_instance.update_portal_user(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalUsersApi->update_portal_user: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**PortalUser**](PortalUser.md)| PortalUser info | 

### Return type

[**PortalUser**](PortalUser.md)

### Authorization

[tip_wlan_ts_auth](../README.md#tip_wlan_ts_auth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

