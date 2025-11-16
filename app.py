from flask import Flask, render_template, request, redirect, url_for, flash, abort
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "change-this-secret"  # necesario para mensajes flash


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    if request.method == "POST":
        try:
            n1 = float(request.form.get("nota1", ""))
            n2 = float(request.form.get("nota2", ""))
            n3 = float(request.form.get("nota3", ""))
            asistencia = float(request.form.get("asistencia", ""))
        except ValueError:
            flash("Ingrese valores numéricos válidos.", "error")
            return redirect(url_for("ejercicio1"))

        # Validaciones de rango
        if not (10 <= n1 <= 70 and 10 <= n2 <= 70 and 10 <= n3 <= 70):
            flash("Las notas deben estar entre 10 y 70.", "error")
            return redirect(url_for("ejercicio1"))
        if not (0 <= asistencia <= 100):
            flash("La asistencia debe estar entre 0 y 100.", "error")
            return redirect(url_for("ejercicio1"))

        promedio = round((n1 + n2 + n3) / 3, 2)
        estado = "Aprobado" if (promedio >= 40 and asistencia >= 75) else "Reprobado"
        return render_template("ejercicio1_resultado.html", promedio=promedio, asistencia=asistencia, estado=estado)

    return render_template("ejercicio1.html")


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    if request.method == "POST":
        n1 = request.form.get("nombre1", "").strip()
        n2 = request.form.get("nombre2", "").strip()
        n3 = request.form.get("nombre3", "").strip()
        if not (n1 and n2 and n3):
            flash("Debe ingresar los 3 nombres.", "error")
            return redirect(url_for("ejercicio2"))
        # nombres diferentes según enunciado
        if len({n1.lower(), n2.lower(), n3.lower()}) < 3:
            flash("Ingrese 3 nombres diferentes.", "error")
            return redirect(url_for("ejercicio2"))
        # Determinar el más largo (si empatan, el primero con esa longitud)
        nombres = [n1, n2, n3]
        mayor = max(nombres, key=lambda s: len(s))
        longitud = len(mayor)
        return render_template("ejercicio2_resultado.html", mayor=mayor, longitud=longitud, nombres=nombres)

    return render_template("ejercicio2.html")


# Rutas adicionales para demostrar enrutamiento con parámetros y abort/redirecciones
@app.route("/saludo/<nombre>")
def saludo(nombre: str):
    return f"Hola, {escape(nombre)}!"


@app.route("/abortar")
def abortar():
    abort(404)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)