import random
import uuid

from models.interfaces import IPagoProcesable, IPagoReembolsable, IPagoConsultable
from models.resultados import ResultadoPago, ResultadoReembolso, EstadoPago


class PayPalAdapter(IPagoProcesable, IPagoReembolsable, IPagoConsultable):
    """
    Simula el SDK de PayPal. Soporta procesar, reembolsar y consultar,
    por lo que implementa las tres interfaces segregadas.
    """

    def procesar_pago(self, monto: float, detalle: dict) -> ResultadoPago:
        # --- simulación de la llamada HTTP a la API real de PayPal ---
        aprobado = monto <= 5000  # regla simulada: PayPal rechaza montos muy altos
        return ResultadoPago(
            id_transaccion=str(uuid.uuid4())[:8],
            pasarela="PayPal",
            monto=monto,
            aprobado=aprobado,
            mensaje="Pago aprobado por PayPal" if aprobado else "Fondos insuficientes (simulado)",
            codigo_autorizacion=f"PP-{random.randint(100000, 999999)}" if aprobado else "",
        )

    def reembolsar_pago(self, id_transaccion: str, monto: float) -> ResultadoReembolso:
        return ResultadoReembolso(
            id_transaccion=id_transaccion,
            monto_reembolsado=monto,
            estado="completado",
            mensaje="Reembolso procesado por PayPal",
        )

    def consultar_estado(self, id_transaccion: str) -> EstadoPago:
        return EstadoPago(id_transaccion=id_transaccion, estado_actual="aprobado")
