"""
Facade (patrón Facade).

El resto de la aplicación (rutas Flask / controlador) solo conoce los
tres métodos públicos de ProcesadorPagos. No conoce qué adaptador
concreto se ejecuta ni los detalles de cada API externa.
"""
from models.interfaces import IPagoReembolsable
from models.adapters.paypal_adapter import PayPalAdapter
from models.adapters.stripe_adapter import StripeAdapter
from models.adapters.mercadopago_adapter import MercadoPagoAdapter
from models.resultados import ResultadoReembolso, Transaccion


class ProcesadorPagos:
    def __init__(self):
        # Mapa de pasarela -> adaptador (fácil de extender: RNF-03)
        self.adaptadores = {
            "PayPal": PayPalAdapter(),
            "Stripe": StripeAdapter(),
            "MercadoPago": MercadoPagoAdapter(),
        }
        # "Base de datos" en memoria para el panel administrativo (RF-06)
        self.transacciones: dict[str, Transaccion] = {}

    def pagar(self, pasarela: str, monto: float, detalle: dict | None = None):
        adaptador = self.adaptadores[pasarela]
        resultado = adaptador.procesar_pago(monto, detalle or {})

        tx = Transaccion(
            id_pedido=resultado.id_transaccion,
            pasarela=pasarela,
            monto=monto,
            estado="aprobado" if resultado.aprobado else "rechazado",
            codigo_autorizacion=resultado.codigo_autorizacion,
            # El ISP se evidencia aquí: isinstance() detecta en tiempo de
            # ejecución si ESTE adaptador soporta reembolso.
            puede_reembolsar=resultado.aprobado and isinstance(adaptador, IPagoReembolsable),
        )
        self.transacciones[tx.id_pedido] = tx
        return resultado

    def reembolsar(self, id_transaccion: str) -> ResultadoReembolso:
        tx = self.transacciones.get(id_transaccion)
        if tx is None:
            return ResultadoReembolso(id_transaccion, 0, "no_encontrado", "Transacción inexistente")

        adaptador = self.adaptadores[tx.pasarela]

        # --- Aquí el Facade rechaza la operación SIN invocar al adaptador ---
        if not isinstance(adaptador, IPagoReembolsable):
            return ResultadoReembolso(
                id_transaccion=id_transaccion,
                monto_reembolsado=0,
                estado="no_soportado",
                mensaje=f"{tx.pasarela} no soporta reembolso automático en este simulador.",
            )

        resultado = adaptador.reembolsar_pago(id_transaccion, tx.monto)
        tx.estado = "reembolsado"
        return resultado

    def consultar_estado(self, pasarela: str, id_transaccion: str):
        return self.adaptadores[pasarela].consultar_estado(id_transaccion)

    def listar_transacciones(self):
        return sorted(self.transacciones.values(), key=lambda t: t.fecha, reverse=True)


# Instancia única compartida por toda la aplicación (equivalente a un singleton simple)
procesador_pagos = ProcesadorPagos()
