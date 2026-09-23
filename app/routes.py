from datetime import date

from flask import Flask, flash, redirect, render_template, request, url_for

from .services import (
    MATTERS,
    all_clients,
    client_installments,
    create_plan,
    dashboard,
    delete_client,
    find_client,
    monthly_report,
    month_label,
    parse_date,
    record_payment,
    update_client,
)


def register_routes(app: Flask) -> None:
    @app.context_processor
    def inject_globals():
        return {"matters": MATTERS}

    @app.template_filter("money")
    def money_filter(value):
        from .services import format_money
        return format_money(value)

    @app.get("/")
    def index():
        return render_template("inicio.html", dashboard=dashboard(app.repository))

    @app.get("/clientes")
    def clients():
        query = request.args.get("q", "").strip().lower()
        matter = request.args.get("matter", "").strip()
        filtered = [
            client for client in all_clients(app.repository)
            if (not query or query in client["full_name"].lower())
            and (not matter or matter == client["matter"])
        ]
        return render_template("clientes.html", clients=filtered, query=query, selected_matter=matter)

    @app.route("/clientes/nuevo", methods=["GET", "POST"])
    def new_client():
        if request.method == "POST":
            try:
                pays_in_installments = request.form.get("pays_in_installments") == "si"
                installment_count = int(request.form.get("installment_count", "0") or 0)
                client_entry_date = parse_date(request.form.get("client_entry_date", ""))
                first_date_value = request.form.get("first_installment_date", "")
                first_installment_date = parse_date(first_date_value) if pays_in_installments else None
                client_id = create_plan(
                    app.repository,
                    request.form.get("full_name", ""),
                    request.form.get("matter", ""),
                    int(request.form.get("total_amount", "0") or 0),
                    pays_in_installments,
                    installment_count,
                    first_installment_date,
                    client_entry_date=client_entry_date,
                    receipt_issued=request.form.get("receipt_issued") == "si",
                )
                flash("Cliente y plan de pago creados correctamente.", "success")
                return redirect(url_for("client_detail", client_id=client_id))
            except (ValueError, TypeError) as error:
                flash(str(error), "danger")
        return render_template("cliente_form.html")

    @app.get("/clientes/<client_id>")
    def client_detail(client_id: str):
        client = find_client(app.repository, client_id)
        if not client:
            flash("Cliente no encontrado.", "danger")
            return redirect(url_for("clients"))
        return render_template(
            "cliente_detalle.html",
            client=client,
            installments=client_installments(app.repository, client_id),
        )

    @app.route("/clientes/<client_id>/editar", methods=["GET", "POST"])
    def edit_client(client_id: str):
        client = find_client(app.repository, client_id)
        if not client:
            flash("Cliente no encontrado.", "danger")
            return redirect(url_for("clients"))
        if request.method == "POST":
            try:
                pays_in_installments = request.form.get("pays_in_installments") == "si"
                installment_count = int(request.form.get("installment_count", "0") or 0)
                client_entry_date = parse_date(request.form.get("client_entry_date", ""))
                first_date_value = request.form.get("first_installment_date", "")
                first_installment_date = parse_date(first_date_value) if pays_in_installments else None
                update_client(
                    app.repository,
                    client_id,
                    request.form.get("full_name", ""),
                    request.form.get("matter", ""),
                    int(request.form.get("total_amount", "0") or 0),
                    pays_in_installments,
                    installment_count,
                    first_installment_date,
                    client_entry_date,
                )
                flash("Ficha del cliente actualizada correctamente.", "success")
                return redirect(url_for("client_detail", client_id=client_id))
            except (ValueError, TypeError) as error:
                flash(str(error), "danger")
                client = find_client(app.repository, client_id)
        return render_template("cliente_editar.html", client=client)

    @app.post("/clientes/<client_id>/eliminar")
    def remove_client(client_id: str):
        try:
            delete_client(app.repository, client_id)
            flash("Cliente y registros relacionados eliminados correctamente.", "success")
        except ValueError as error:
            flash(str(error), "danger")
        return redirect(url_for("clients"))

    @app.post("/clientes/<client_id>/pagos")
    def add_payment(client_id: str):
        try:
            record_payment(
                app.repository,
                client_id,
                request.form.get("installment_id", ""),
                parse_date(request.form.get("payment_date", "")),
                int(request.form.get("amount", "0") or 0),
                request.form.get("receipt_issued") == "si",
                request.form.get("note", ""),
            )
            flash("Pago registrado correctamente.", "success")
        except (ValueError, TypeError) as error:
            flash(str(error), "danger")
        return redirect(url_for("client_detail", client_id=client_id))

    @app.get("/informe")
    def report():
        selected_month = request.args.get("month", "").strip()
        try:
            reference_date = date.fromisoformat(f"{selected_month}-01") if selected_month else date.today()
        except ValueError:
            flash("El mes seleccionado no es válido.", "danger")
            return redirect(url_for("report"))
        return render_template(
            "informe_mensual.html",
            report=monthly_report(app.repository, reference_date),
            dashboard=dashboard(app.repository),
            report_month=reference_date.strftime("%Y-%m"),
            report_month_label=month_label(reference_date.strftime("%Y-%m")),
        )
