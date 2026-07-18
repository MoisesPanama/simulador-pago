"""
Interfaces segregadas (Principio ISP).

Cada pasarela implementa solo las interfaces que su API realmente soporta.
Esto evita que una clase quede obligada a implementar métodos que no le
corresponden (por ejemplo, MercadoPagoAdapter NO implementa
IPagoReembolsable en este simulador).
"""
from abc import ABC, abstractmethod


class IPagoProcesable(ABC):
    """Toda pasarela capaz de cobrar un pago debe implementar esto."""

    @abstractmethod
    def procesar_pago(self, monto: float, detalle: dict):
        ...


class IPagoReembolsable(ABC):
    """Solo las pasarelas que soportan reembolso automático implementan esto."""

    @abstractmethod
    def reembolsar_pago(self, id_transaccion: str, monto: float):
        ...


class IPagoConsultable(ABC):
    """Toda pasarela capaz de reportar el estado de una transacción."""

    @abstractmethod
    def consultar_estado(self, id_transaccion: str):
        ...
