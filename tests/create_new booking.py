import allure
import pytest
import requests

#Каждая функция проверяет разные сценарии:
# успешное создание брони
# ошибка из-за отсутствия полей
# ошибка с сервером (некорректные данные)


@allure.feature('Test Create Booking')
@allure.story('Test successful booking creation')
def test_create_booking_success(apiclient, mocker):
    mock_response = mocker.Mock()
    mockresponse.statuscode = 200
    mockresponse.json.return_value = {"booking_id": 2}
    mocker.patch.object(apiclient.session, 'post', return_value=mock_response)

    response = apiclient.createbooking({
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 133,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-10-01",
            "checkout": "2025-10-10"
        },
        "additionalneeds": "Breakfast"
    })

    assert response['booking_id'] == 2, f"Expected booking_id 1 but got {response['booking_id']}"


@allure.feature('Test Create Booking')
@allure.story('Test booking creation with missing fields')
def test_create_booking_missing_fields(api_client, mocker):
    mock_response = mocker.Mock()
    mockresponse.statuscode = 404
    mocker.patch.object(apiclient.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 404"):
        apiclient.createbooking({
            "firstname": "Jimmy",
            "lastname": "Dimple",
            "totalprice": 100,
        })


@allure.feature('Test Create Booking')
@allure.story('Test server error during booking creation')
def test_create_booking_server_error(api_client, mocker):
    mock_response = mocker.Mock()
    mockresponse.statuscode = 500
    mocker.patch.object(apiclient.session, 'post', return_value=mock_response)

    with pytest.raises(AssertionError, match="Expected status 200 but got 500"):
        apiclient.createbooking({
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 132,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-10-01",
                "checkout": "2024-10-10"
            }
        })


@allure.feature('Test Create Booking')
@allure.story('Test timeout during booking creation')
def test_create_booking_timeout(apiclient, mocker):
    mocker.patch.object(apiclient.session, 'post', side_effect=requests.Timeout)

    with pytest.raises(requests.Timeout):
        apiclient.createbooking({
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 111,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2023-10-02",
                "checkout": "2023-10-10"
            }
        })
