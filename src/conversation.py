PRIORITIES = {
    'SYSTEM': 0x00,
    'NORMAL': 0x01,
    'URGENT': 0x02,
    'LOW'   : 0x03
}

TPCI_TYPES = {
    'UNNUMBERED_DATA_PACKET': 'UDP',
    'NUMBERED_DATA_PACKET': 'NDP',
    'UNNUMBERED_CONTROL_DATA': 'UCD',
    'NUMBERED_CONTROL_DATA': 'NCD'
}

APCI_TYPES = {
    'A_GROUP_VALUE_READ': 'A_GroupValue_Read',
    'A_GROUP_VALUE_RESPONSE': 'A_GroupValue_Response',
    'A_GROUP_VALUE_WRITE': 'A_GroupValue_Write',

    'A_INDIVIDUAL_ADDRESS_WRITE': 'A_IndividualAddress_Write',
    'A_INDIVIDUAL_ADDRESS_READ': 'A_IndividualAddress_Read',
    'A_INDIVIDUAL_ADDRESS_RESPONSE': 'A_IndividualAddress_Response',
    'A_INDIVIDUAL_ADDRESS_SERIAL_NUMBER_READ': 'A_IndividualAddressSerialNumber_Read',
    'A_INDIVIDUAL_ADDRESS_SERIAL_NUMBER_RESPONSE': 'A_IndividualAddressSerialNumber_Response',
    'A_INDIVIDUAL_ADDRESS_SERIAL_NUMBER_WRITE': 'A_IndividualAddressSerialNumber_Write',

    'A_DOMAIN_ADDRESS_WRITE': 'A_DomainAddress_Write',
    'A_DOMAIN_ADDRESS_READ': 'A_DomainAddress_Read',
    'A_DOMAIN_ADDRESS_RESPONSE': 'A_DomainAddress_Response',

    'A_PROPERTY_VALUE_READ': 'A_PropertyValue_Read',
    'A_PROPERTY_VALUE_RESPONSE': 'A_PropertyValue_Response',
    'A_PROPERTY_VALUE_WRITE': 'A_PropertyValue_Write',

    'A_PROPERTY_DESCRIPTION_READ': 'A_PropertyDescription_Read',
    'A_PROPERTY_DESCRIPTION_RESPONSE': 'A_PropertyDescription_Response',

    'A_USER_MEMORY_READ': 'A_UserMemory_Read',
    'A_USER_MEMORY_RESPONSE': 'A_UserMemory_Response',
    'A_USER_MEMORY_WRITE': 'A_UserMemory_Write',

    'A_USER_MANUFACTURE_INFO_READ': 'A_UserManufacturerInfo_Read',
    'A_USER_MANUFACTURE_INFO_RESPONSE': 'A_UserManufacturerInfo_Response',

    'A_ADC_READ': 'A_ADC_Read',
    'A_ADC_RESPONSE': 'A_ADC_Response',

    'A_MEMORY_READ': 'A_Memory_Read',
    'A_MEMORY_RESPONSE': 'A_Memory_Response',
    'A_MEMORY_WRITE': 'A_Memory_Write',

    'A_DEVICE_DESCRIPTOR_READ': 'A_DeviceDescriptor_Read',
    'A_DEVICE_DESCRIPTOR_RESPONSE': 'A_DeviceDescriptor_Response',

    'A_RESTART': 'A_Restart',

    'A_AUTHORIZE_REQUEST': 'A_Authorize_Request',
    'A_AUTHORIZE_RESPONSE': 'A_Authorize_Response',
    'A_KEY_WRITE': 'A_Key_Write',
    'A_KEY_RESPONSE': 'A_Key_Response',

    'A_NETWORK_PARAMETER_READ': 'A_NetworkParameter_Read',
    'A_NETWORK_PARAMETER_RESPONSE': 'A_NetworkParameter_Response',
    'A_NETWORK_PARAMETER_WRITE': 'A_NetworkParameter_Write',

    'A_LINK_READ': 'A_Link_Read',
    'A_LINK_RESPONSE': 'A_Link_Response',
    'A_LINK_WRITE': 'A_Link_Write',

    'A_DOMAIN_ADDRESS_SELECTIVE_READ': 'A_DomainAddressSelective_Read'
}
