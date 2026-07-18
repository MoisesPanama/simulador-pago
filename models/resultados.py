"""
Contrato común al que cada adaptador traduce la respuesta específica
de su API externa (parte del patrón Adapter).
"""
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class ResultadoPago:
    id_transaccion: str
    pasarela: str
    monto: float
    aprobado: bool
    mensaje: str
    codigo_autorizacion: str


@dataclass
class ResultadoReembolso:
    id_transaccion: str
    monto_reembolsado: float
    estado: str  # "completado" | "rechazado" | "no_soportado"
    mensaje: str


@dataclass
class EstadoPago:
    id_transaccion: str
    estado_actual: str  # "aprobado" | "pendiente" | "rechazado" | "reembolsado"


@dataclass
class Transaccion:
    """Registro interno para el panel administrativo y la auditoría (RF-06)."""
    id_pedido: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pasarela: str = ""
    monto: float = 0.0
    estado: str = "pendiente"
    codigo_autorizacion: str = ""
    puede_reembolsar: bool = False
    fecha: datetime = field(default_factory=datetime.now)
