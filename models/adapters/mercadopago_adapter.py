import random
import uuid

from models.interfaces import IPagoProcesable, IPagoConsultable
from models.resultados import ResultadoPago, EstadoPago


class MercadoPagoAdapter(IPagoProcesable, IPagoConsultable):
    """
    Simula el API de MercadoPago. A diferencia de PayPal y Stripe, esta
    pasarela NO expone reembolso automático en el simulador, por lo que
    -siguiendo el ISP- simplemente no implementa IPagoReembolsable.
    Ningún método vacío ni excepción "NotImplemented": la restricción
    queda expresada en el propio tipo de la clase.
    """

    def procesar_pago(self, monto: float, detalle: dict) -> ResultadoPago:
        aprobado = random.random() > 0.15
        return ResultadoPago(
            id_transaccion=str(uuid.uuid4())[:8],
            pasarela="MercadoPago",
            monto=monto,
            aprobado=aprobado,
            mensaje="Pago aprobado por MercadoPago" if aprobado else "Pago rechazado (simulado)",
            codigo_autorizacion=f"MP-{random.randint(100000, 999999)}" if aprobado else "",
        )

    def consultar_estado(self, id_transaccion: str) -> EstadoPago:
        return EstadoPago(id_transaccion=id_transaccion, estado_actual="aprobado")
