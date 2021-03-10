from typing import Optional, List

from swagger_server.models.payment_provider import PaymentProvider  # noqa: E501


class FakeDB:
    def __init__(self):
        self.payment_providers = {}

    def add_payment_provider(self, payment_provider: PaymentProvider):
        if payment_provider.provider_name in self.payment_providers:
            raise ValueError(f"Provider with name {payment_provider.provider_name} already defined")
        self.payment_providers[payment_provider.provider_name] = payment_provider

    def delete_payment_provider(self, provider_name: str):
        del self.payment_providers[provider_name]

    def get_payment_provider(self, provider_name: str) -> Optional[PaymentProvider]:
        return self.payment_providers.get(provider_name)

    def get_payment_providers(self) -> List[PaymentProvider]:
        return list(self.payment_providers.values())


DB = FakeDB()
