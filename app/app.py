from flask import Flask, render_template, request, redirect, url_for, flash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "replace-me-in-prod"

USERS = {
    "juan": {"password": "admin", "role": "administrador"},
    "pepe": {"password": "user", "role": "usuario"},
}

PAINT_PRICE = 9000


def compute_discount(age: int) -> float:
    if 18 <= age <= 30:
        return 0.15
    if age > 30:
        return 0.25
    return 0.0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        edad_raw = request.form.get("edad", "").strip()
        tarros_raw = request.form.get("tarros", "").strip()

        errors = []
        if not nombre:
            errors.append("El nombre es obligatorio.")
        try:
            edad = int(edad_raw)
            if edad < 0:
                errors.append("La edad no puede ser negativa.")
        except ValueError:
            errors.append("La edad debe ser un número entero.")
            edad = 0
        try:
            tarros = int(tarros_raw)
            if tarros < 0:
                errors.append("La cantidad de tarros no puede ser negativa.")
        except ValueError:
            errors.append("La cantidad de tarros debe ser un número entero.")
            tarros = 0

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("ejercicio1.html", nombre=nombre, edad=edad_raw, tarros=tarros_raw)

        total_sin_desc = PAINT_PRICE * tarros
        desc = compute_discount(edad)
        total_con_desc = int(round(total_sin_desc * (1 - desc)))

        return render_template(
            "ejercicio1_resultado.html",
            nombre=nombre,
            edad=edad,
            tarros=tarros,
            total_sin_desc=total_sin_desc,
            descuento=int(desc * 100),
            total_con_desc=total_con_desc,
        )

    return render_template("ejercicio1.html")


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    message = None
    ok = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        password = request.form.get("password", "")
        record = USERS.get(usuario)
        if record and record["password"] == password:
            role = record["role"]
            message = f"Bienvenido {role} {usuario}"
            ok = True
        else:
            message = "Usuario o contraseña incorrectos"
            ok = False
    return render_template("ejercicio2.html", message=message, ok=ok)


if __name__ == "__main__":
    # For local debug. In production use a proper WSGI server.
    app.run(debug=True)
