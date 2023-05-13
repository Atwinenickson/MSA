*** Settings ***
Library    RequestsLibrary
Library    Collections
Library             Process
Library             OperatingSystem
Suite Setup    Authenticate as Admin

*** Variables ***
#ENDPOINTS              ---
${BASE_URL}             https://restful-booker.herokuapp.com
${AUTH}                 /auth
${BOOKING}              /booking
#LOOP COUNTER           ---
${COUNTER}              ${1}
#HEADERS                ---
${CONTENT_TYPE}         application/json
#AUTH                   ---
${USERNAME}             admin
${PASSWORD}             password123
#BOOKING DETAILS        ---
${FIRSTNAME}            Atwine
${LASTNAME}             Nickson
${TOTALPRICE}           500
${DEPOSITPAID}          true
${CHECKIN}              2022-05-13
${CHECKOUT}             2023-05-14
${ADDITIONALNEEDS}      Clearly Defined Requirements


***Test Cases***

Add New Booking
    [Tags]  Post
    Create a Booking for MFS

Get The Created Booking
    [Tags]  Get
    Get New Booking By Name


Update The Booking
    [Tags]  Put
    Update New Booking


*** Keywords ***


Create a Booking for MFS
    Create Session      Add Booking     ${BASE_URL}     verify=True
    ${booking_dates}    Create Dictionary    checkin=${CHECKIN}   checkout=${CHECKOUT}
    ${body}    Create Dictionary    firstname=${FIRSTNAME}    lastname=${LASTNAME}    totalprice=${TOTALPRICE}     depositpaid=${DEPOSITPAID}    bookingdates=${booking_dates}
    ${response}    POST On Session    Add Booking     ${BOOKING}    json=${body}
    Log To Console    ${response.json()}
    ${id}    Set Variable   ${response.json()}[bookingid]
    ${created_user_id}    Convert to String    ${id}
    Log To Console     ${id}
    Set Suite Variable    ${id}
    ${response}    GET On Session    Add Booking     ${BOOKING}/${created_user_id}
    Should Be Equal    ${response.json()}[lastname]    ${LASTNAME}
    Should Be Equal    ${response.json()}[firstname]    ${FIRSTNAME}   
    Should Be Equal As Numbers    ${response.json()}[totalprice]    ${TOTALPRICE}
    Dictionary Should Contain Value     ${response.json()}    ${FIRSTNAME}
    Set Suite Variable      ${NEW_ID}       ${id}
    Log To Console    ${response.json()}
    Log To Console    ${NEW_ID}



Get New Booking By Name
    Create Session      Get ID By Name      ${BASE_URL}     verify=True
    ${url}=  Catenate  SEPARATOR=/  ${BASE_URL}/booking/?firstname=${FIRSTNAME}&lastname=${LASTNAME}
    ${response}=        GET        ${url}
    Should Be Equal As Strings      ${response.status_code}     200
    # Should Contain Any        ${response.content}     .bookingid:(${NEW_ID})
    # Log To Console    ${response.content}
    ${response_json}=    Set Variable    ${response.json()}
    @{booking_ids}=    Create List
    FOR    ${booking}    IN    @{response_json}
        Append To List    ${booking_ids}    ${booking['bookingid']}
    END
    Should Contain    ${booking_ids}    ${NEW_ID}
    Log To Console    ${response.content}

Update New Booking
    ${updatebooking}=        Create Dictionary
    ...                             checkin=2022-05-16    checkout=2022-05-17
    ${HEADERS}=          Create Dictionary
    ...                  Content-Type=${CONTENT_TYPE}
    ...                  Cookie=token=${token}
    Create Session  Update Booking      ${BASE_URL}     verify=True
    ${response}=        Patch Request       Update Booking      uri=${BOOKING}/${NEWID}     data=${updatebooking}        headers=${HEADERS}
    Should Be Equal As Strings      ${response.status_code}     200
    

Authenticate as Admin
    Ping Server
    ${HEADERS}=         Create Dictionary
    ...                 Content-Type=${CONTENT_TYPE}
    ...                 User-Agent=MFS
    Create Session      Obtain Token        ${BASE_URL}     verify=True
    ${body}    Create Dictionary    username=admin    password=password123
    ${response}    POST On Session    Obtain Token    ${AUTH}    json=${body}    headers=${HEADERS}
    Log    ${response.json()}
    ${token}    Set Variable    ${response.json()}[token]
    Log    ${token}
    Set Suite Variable    ${token}
    Log To Console    ${token}

Ping Server
    Create Session      ping        ${BASE_URL}     verify=True
    ${response}=        GET On Session     ping        /ping 
    Should Be Equal As Strings      ${response.status_code}     201
