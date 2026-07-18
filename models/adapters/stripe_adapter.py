import random
import uuid

from models.interfaces import IPagoProcesable, IPagoReembolsable, IPagoConsultable
from models.resultados import ResultadoPago, ResultadoReembolso, EstadoPago


class StripeAdapter(IPagoProcesable, IPagoReembolsable, IPagoConsultable):
    """
    Simula el API REST de Stripe. Al igual que PayPal, soporta las tres
    operaciones, por lo que implementa las tres interfaces.
    """

    def procesar_pago(self, monto: float, detalle: dict) -> ResultadoPago:
        aprobado = random.random() > 0.1  # 90% de aprobación simulada
        return ResultadoPago(
            id_transaccion=str(uuid.uuid4())[:8],
            pasarela="Stripe",
            monto=monto,
            aprobado=aprobado,
            mensaje="Pago aprobado por Stripe" if aprobado else "Tarjeta declinada (simulado)",
            codigo_autorizacion=f"ST-{random.randint(100000, 999999)}" if aprobado else "",
        )

    def reembolsar_pago(self, id_transaccion: str, monto: float) -> ResultadoReembolso:
        return ResultadoReembolso(
            id_transaccion=id_transaccion,
            monto_reembolsado=monto,
            estado="completado",
            mensaje="Reembolso procesado por Stripe",
        )

    def consultar_estado(self, id_transaccion: str) -> EstadoPago:
        return EstadoPago(id_transaccion=id_transaccion, estado_actual="aprobado")
