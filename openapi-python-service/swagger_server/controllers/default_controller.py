import connexion
import six

from swagger_server.models.inline_response400 import InlineResponse400  # noqa: E501
from swagger_server.models.payment_provider import PaymentProvider  # noqa: E501
from swagger_server import util
from swagger_server.db import DB


def payemnt_providers_get():  # noqa: E501
    return DB.get_payment_providers()


def payemnt_providers_post(body):  # noqa: E501
    if connexion.request.is_json:
        body = PaymentProvider.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        DB.add_payment_provider(body)
    except ValueError:
        return (InlineResponse400("Provider with such name already exsists"), 400, )
    return (None, 200)


def payment_provider_provider_name_delete(provider_name):  # noqa: E501
    provider = DB.get_payment_provider(provider_name)
    if not provider:
        return (InlineResponse400("Prodiver with such name doesn't exists"), 404,)
    DB.delete_payment_provider(provider_name)
    return (None, 200)


def payment_provider_provider_name_get(provider_name):  # noqa: E501
    provider = DB.get_payment_provider(provider_name)
    if not provider:
        return (InlineResponse400("Prodiver with such name doesn't exists"), 404)
    return provider


def payment_provider_provider_name_put(provider_name, body):  # noqa: E501
    if connexion.request.is_json:
        body = PaymentProvider.from_dict(connexion.request.get_json())  # noqa: E501
    provider = DB.get_payment_provider(provider_name)
    if not provider:
        return (InlineResponse400("Prodiver with such name doesn't exists"), 404,)
    DB.delete_payment_provider(provider_name)
    DB.add_payment_provider(body)
    return (None, 200)
