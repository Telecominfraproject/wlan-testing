# FirmwareVersion

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [optional] 
**equipment_type** | [**EquipmentType**](EquipmentType.md) |  | [optional] 
**model_id** | **str** | equipment model | [optional] 
**version_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**filename** | **str** |  | [optional] 
**commit** | **str** | commit number for the firmware image, from the source control system | [optional] 
**validation_method** | [**FirmwareValidationMethod**](FirmwareValidationMethod.md) |  | [optional] 
**validation_code** | **str** | firmware digest code, depending on validation method - MD5, etc. | [optional] 
**release_date** | **int** | release date of the firmware image, in ms epoch time | [optional] 
**created_timestamp** | **int** |  | [optional] 
**last_modified_timestamp** | **int** | must be provided for update operation, update will be rejected if provided value does not match the one currently stored in the database | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

