*** Settings ***
Documentation       Simple example using AppiumLibrary
Library             AppiumLibrary
Resource            ${CURDIR}/xpath.resource


*** Variables ***
${ANDROID_AUTOMATION_NAME}      UIAutomator2
${ANDROID_PLATFORM_NAME}        Android
${ANDROID_PLATFORM_VERSION}     %{ANDROID_PLATFORM_VERSION=13}
${DEVICE_NAME}                 %{DEVICE_NAME=258e7ccc}
${UID}                         %{UID=258e7ccc}

*** Keywords ***
Back To HomeScreen
    Press Keycode               keycode=3

Test Setup To Go To Setting App
    Back To HomeScreen
    Back To HomeScreen
    Open Setting App
    Sleep                       1s

Swipe Right
    Swipe
    ...                         start_x=900
    ...                         start_y=800
    ...                         end_x=200
    ...                         end_y=800
    ...                         duration=1s
    Sleep                       1s
    
Open Setting App
    Swipe Right
    Click Element               ${SETTING_APPS}

Get Tab Text
    [Arguments]                 @{locator}
    ${text}=                    Get Text          @{locator}
    Log                         ${text}
    Click Element               @{locator}
    
Open Test Application
    Open Application            http://127.0.0.1:4723
    ...                         automationName=${ANDROID_AUTOMATION_NAME}
    ...                         platformName=${ANDROID_PLATFORM_NAME}
    ...                         platformVersion=${ANDROID_PLATFORM_VERSION}
    ...                         deviceName=${DEVICE_NAME}
    ...                         udid=${UID}   

Close Test Application
    Close Application