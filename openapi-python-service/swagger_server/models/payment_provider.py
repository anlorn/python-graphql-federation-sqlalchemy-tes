# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PaymentProvider(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, provider_name: str = None, provider_url: str = None, is_enabled: bool = False):  # noqa: E501
        """PaymentProvider - a model defined in Swagger
        """
        self.swagger_types = {
            'provider_name': str,
            'provider_url': str,
            'is_enabled': bool,
        }

        self.attribute_map = {
            'provider_name': 'provider_name',
            'provider_url': 'provider_url',
            'is_enabled': 'is_enabled',
            'username': 'username'
        }
        self._provider_name = provider_name
        self._provider_url = provider_url
        self._is_enabled = is_enabled

    @classmethod
    def from_dict(cls, dikt) -> 'PaymentProvider':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PaymentProvider of this PaymentProvider.  # noqa: E501
        :rtype: PaymentProvider
        """
        return util.deserialize_model(dikt, cls)

    @property
    def provider_name(self) -> str:
        return self._provider_name

    @provider_name.setter
    def provider_name(self, provider_name: str):
        self._provider_name = provider_name

    @property
    def provider_url(self):
        return self._provider_url

    @provider_url.setter
    def provider_url(self, provider_url: str):
        self._provider_url = provider_url

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    @is_enabled.setter
    def is_enabled(self, is_enabled: bool):
        self._is_enabled = is_enabled
