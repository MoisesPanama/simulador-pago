from flask import Flask, render_template, request, redirect, url_for

from models.procesador_pagos import procesador_pagos

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def pedido():
    """RF-01, RF-02, RNF-01: formulario de pedido y selección de pasarela."""
    if request.method == "POST":
        pasarela = request.form["pasarela"]
        monto = float(request.form["monto"])

        # RF-03: procesar el pago a través del Facade (Adapter común por debajo)
        resultado = procesador_pagos.pagar(pasarela, monto)
        return redirect(url_for("confirmacion", id_transaccion=resultado.id_transaccion))

    return render_template("pedido.html", pasarelas=list(procesador_pagos.adaptadores.keys()))


@app.route("/confirmacion/<id_transaccion>")
def confirmacion(id_transaccion):
    """Pantalla de confirmación: resultado devuelto por el Facade."""
    tx = procesador_pagos.transacciones.get(id_transaccion)
    return render_template("confirmacion.html", tx=tx)


@app.route("/admin")
def admin():
    """RF-06: panel administrativo con lista de transacciones."""
    return render_template("admin.html", transacciones=procesador_pagos.listar_transacciones())


@app.route("/admin/reembolsar/<id_transaccion>", methods=["POST"])
def reembolsar(id_transaccion):
    """RF-05: reembolsar solo si la pasarela lo soporta (ISP en tiempo de ejecución)."""
    procesador_pagos.reembolsar(id_transaccion)
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
