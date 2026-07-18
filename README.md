# Simulador de Pago con Múltiples Pasarelas

Aplicación web en Python (Flask) que simula el cobro a través de tres pasarelas de pago distintas — **PayPal**, **Stripe** y **MercadoPago** — sin que el código cliente conozca los detalles internos de cada una. El proyecto aplica arquitectura **MVC** y los patrones de diseño **Adapter**, **Facade** e **ISP (Interface Segregation Principle)**.

## Contexto de negocio

Una tienda en línea necesita cobrar a través de varias pasarelas de pago de forma unificada. Cada pasarela tiene su propia API simulada, pero el cliente (el controlador Flask) solo interactúa con un punto de entrada común: el **Facade**.

Regla de negocio clave: **MercadoPago no soporta reembolso automático** en este simulador, mientras que **PayPal y Stripe sí**. Esta restricción está modelada a nivel de arquitectura, no con validaciones sueltas.

## Patrones de diseño aplicados

- **Adapter**: cada pasarela (`paypal_adapter.py`, `stripe_adapter.py`, `mercadopago_adapter.py`) traduce su lógica interna a una interfaz común que el resto del sistema entiende.
- **ISP (Interface Segregation Principle)**: las interfaces están separadas en `IPagoProcesable`, `IPagoReembolsable` e `IPagoConsultable` (ABCs). Un adaptador solo implementa las interfaces que realmente soporta — por eso `mercadopago_adapter.py` **no hereda** de `IPagoReembolsable`, en vez de lanzar `NotImplementedError`.
- **Facade**: `ProcesadorPagos` (en `procesador_pagos.py`) expone una API simple (`pagar()`, `reembolsar()`, `consultar_estado()`, `listar_transacciones()`) y decide internamente, con `isinstance(adaptador, IPagoReembolsable)`, si un adaptador soporta reembolso antes de delegarlo. Se instancia una sola vez como `procesador_pagos` (singleton simple) y esa instancia es compartida por todas las rutas de Flask.

Esta restricción de arquitectura también es **visible en la interfaz**: el botón "Reembolsar" del panel `/admin` aparece deshabilitado (con tooltip explicativo) cuando la transacción fue procesada por una pasarela que no soporta reembolsos.

## Estructura del proyecto

```
simulador-pago/
├── app.py                          # Controlador Flask (rutas)
├── requirements.txt
├── models/
│   ├── interfaces.py               # IPagoProcesable, IPagoReembolsable, IPagoConsultable
│   ├── resultados.py               # ResultadoPago, ResultadoReembolso, EstadoPago, Transaccion
│   ├── procesador_pagos.py         # Facade: ProcesadorPagos
│   └── adapters/
│       ├── paypal_adapter.py       # Implementa las 3 interfaces
│       ├── stripe_adapter.py       # Implementa las 3 interfaces
│       └── mercadopago_adapter.py  # Implementa solo Procesable + Consultable
├── templates/
│   ├── base.html
│   ├── pedido.html                 # Formulario: monto + selección de pasarela
│   ├── confirmacion.html           # Resultado devuelto por el Facade
│   └── admin.html                  # Lista de transacciones + botón "Reembolsar"
└── static/
    └── style.css
```

## Rutas principales

| Ruta | Método | Descripción |
|---|---|---|
| `/` | GET, POST | Formulario de pedido (monto + pasarela) y procesamiento del pago vía el Facade |
| `/confirmacion/<id_transaccion>` | GET | Resultado del pago devuelto por el Facade |
| `/admin` | GET | Panel administrativo con historial de transacciones |
| `/admin/reembolsar/<id_transaccion>` | POST | Reembolso (el Facade rechaza la operación sin tocar el adaptador si la pasarela no implementa `IPagoReembolsable`) |

Las transacciones se guardan **en memoria**, dentro de un diccionario `self.transacciones` en `ProcesadorPagos` — no hay base de datos ni persistencia entre reinicios del servidor.

## Identidad visual

Tema oscuro tipo fintech: fondo azul-marino profundo, verde menta para pagos aprobados, coral para rechazados, dorado para montos. Tipografías: Space Grotesk (títulos), Inter (texto), JetBrains Mono (IDs y códigos de autorización).

## Cómo ejecutar el proyecto

### Requisitos previos

- Python 3.10 o superior instalado y agregado al PATH.

### Pasos

1. Clona o descarga este repositorio.
2. Abre una terminal en la carpeta del proyecto.
3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

   > Si `pip` no se reconoce como comando en Windows, usa `python -m pip install -r requirements.txt`.

4. Levanta el servidor:

   ```bash
   flask run
   ```

   > Si `flask` no se reconoce como comando, usa `python -m flask run`.

5. Abre tu navegador en:

   ```
   http://127.0.0.1:5000
   ```

No se requieren dependencias externas más allá de Flask.

## Autor

Proyecto desarrollado por Moisés Panamá — Universidad Técnica Estatal de Quevedo (UTEQ), Facultad de Ciencias de la Ingeniería, carrera de Software Engineering.