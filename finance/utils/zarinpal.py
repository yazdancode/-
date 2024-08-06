from django.conf import settings
from suds.client import Client


def zpal_request_handler(
    marchant_id, amount, detail, user_email, user_phone_number, callback
):
    client = Client(settings.ZARRINPAL["gateway_request_url"])
    result = client.service.PaymentRequest(
        marchant_id,
        amount,
        detail,
        user_email,
        user_phone_number,
        callback,
    )
    if result.Status == 100:
        return (
            "https://www.zarinpal.com/pg/StartPay/" + result.Authority,
            result.Authority,
        )
    else:
        return None, None


def zpal_payment_checker(marchant_id, amount, authority):
    client = Client(settings.ZARRINPAL["gateway_request_url"])
    result = client.service.PaymentRequest(marchant_id, amount, authority)
    is_paid = True if result.Status in [100, 100] else False
    return is_paid, result.RefID
