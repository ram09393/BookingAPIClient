import allure
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client, booking_response, bookingresponse):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivanovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response['booking']['firstname'] == booking_data['firstname']
    assert response['booking']['lastname'] == booking_data['lastname']
    assert response['booking']['totalprice'] == booking_data['totalprice']
    assert response['booking']['depositpaid'] == booking_data['depositpaid']
    assert response['booking']['bookingdates'] == booking_data['bookingdates']
    assert response['booking']['bookingdates'] == booking_data['bookingdates']
    assert response['booking']['additionalneeds'] == booking_data['additionalneeds']

    #_______________________________________________________________________________________________________________________
    # Проверка диапазона дат

    assert 'bookingid' in response, "Response should contain 'bookingid'."
    assert 'booking' in response, "Response should contain 'booking'."
    checkindate = booking_response.booking.booking_dates.checkin
    checkoutdate = booking_response.booking.booking_dates.checkout
    assert checkindate < checkoutdate, "Checkin date should be before checkout date."

    # Проверка формата bookingid

    assert isinstance(booking_response.bookingid, int), "Booking ID should be an integer."
    assert booking_response.bookingid > 0, "Booking ID should be a positive integer."

    # Проверка наличия обязательных полей в booking

    assert booking_response.booking.firstname == booking_data['firstname']
    assert booking_response.booking.lastname == booking_data['lastname']
    assert booking_response.booking.totalprice == booking_data['totalprice']
    assert booking_response.booking.depositpaid == booking_data['depositpaid']
    assert booking_response.booking.bookingdates.dict() == booking_data['bookingdates']

    # Проверка на отсутствие лишних полей
    assert all(field in booking_response.booking.dict() for field in
               booking_data.keys()), "Response should not contain extra fields."

