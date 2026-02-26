*** Settings ***
Resource                    ${CURDIR}/setting_keywords.resource
Suite Setup                 Open Test Application
Suite Teardown              Close Test Application
Test Setup                  Test Setup To Go To Setting App

*** Test Cases ***
Test Go To About Phone Tab And Get Title
    [Tags]        test
    Get Tab Text  ${ABOUT_PHONE_TAB}

Test Go To Update System Tab And Get Title
    Get Tab Text  ${UPDATE_SYSTEM_TAB}

Test Go To Security Status Tab And Get Title
    Get Tab Text  ${SECURITY_STATUS_TAB}

Test Go To Wifi Tab And Get Title
    Get Tab Text  ${WIFI_TAB}

Test Go To Bluetooth Tab And Get Title
    Get Tab Text  ${BLUETOOTH_TAB}

Test Go To Mobile Network Tab And Get Title
    Get Tab Text  ${MOBILE_NETWORK_TAB}

Test Go To Mobile Hotspot Tab And Get Title
    Get Tab Text  ${MOBILE_HOTSPOT_TAB}

Test Go To Other Connectivity Options Tab And Get Title
    Get Tab Text  ${OTHER_CONNECTIVITY_OPTIONS_TAB}