import calendar
from collections import defaultdict
from datetime import date
from uuid import uuid4

from .repositories import CsvRepository


MATTERS = {
    "familia": "Familia",
    "laboral": "Laboral",
    "asesoria": "Asesoría",
    "mediacion": "Mediación",
    "otro": "Otro",
}
MONTH_NAMES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def format_money(value: int | float) -> str:
    return f"${int(round(value)):,}".replace(",", ".")


def month_label(reference: str) -> str:
    year, month = reference.split("-")
    return f"{MONTH_NAMES[int(month) - 1].capitalize()} {year}"


def due_date_for_month(year: int, month: int) -> date:
    return date(year, month, min(30, calendar.monthrange(year, month)[1]))


def distribute_amount(amount: int, count: int) -> list[int]:
    base, remainder = divmod(amount, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def create_plan(
    repository: CsvRepository,
    full_name: str,
    matter: str,
    total_amount: int,
    pays_in_installments: bool,
    installment_count: int,
    first_installment_date: date | None,
    client_entry_date: date | None = None,
    receipt_issued: bool = False,
) -> str:
    full_name = " ".join(full_name.split())
    if not full_name:
        raise ValueError("El nombre completo es obligatorio.")
    if matter not in MATTERS:
        raise ValueError("La materia seleccionada no es válida.")
    if total_amount <= 0:
        raise ValueError("El monto total debe ser mayor que cero.")
    if installment_count < 0:
        raise ValueError("La cantidad de cuotas no puede ser negativa.")
    if pays_in_installments and installment_count < 1:
        raise ValueError("Indique al menos una cuota posterior al pie.")
    if not pays_in_installments:
        installment_count = 0
        first_installment_date = None
    if pays_in_installments and first_installment_date is None:
        raise ValueError("La fecha de la primera cuota es obligatoria cuando el cliente paga en cuotas.")
    if client_entry_date is None:
        raise ValueError("La fecha de ingreso del cliente es obligatoria.")

    client_id = uuid4().hex
    today = date.today()
    first_date = first_installment_date
    repository.append("clients", {
        "client_id": client_id,
        "full_name": full_name,
        "matter": matter,
        "total_amount": total_amount,
        "pays_in_installments": "si" if pays_in_installments else "no",
        "installment_count": installment_count,
        "first_installment_date": first_date.isoformat() if first_date else "",
        "created_at": client_entry_date.isoformat(),
        "status": "active",
    })

    down_payment = total_amount if not pays_in_installments else round(total_amount * 0.30)
    installment_rows = [{
        "installment_id": uuid4().hex,
        "client_id": client_id,
        "number": 0,
        "kind": "unico" if not pays_in_installments else "pie",
        "scheduled_amount": down_payment,
        "due_date": client_entry_date.isoformat(),
        "reference_month": client_entry_date.strftime("%Y-%m"),
    }]
    if installment_count and first_date is not None:
        remaining = total_amount - down_payment
        amounts = distribute_amount(remaining, installment_count)
        for index, amount in enumerate(amounts, start=1):
            month_offset = first_date.month - 1 + index - 1
            year = first_date.year + month_offset // 12
            month = month_offset % 12 + 1
            due_date = due_date_for_month(year, month)
            installment_rows.append({
                "installment_id": uuid4().hex,
                "client_id": client_id,
                "number": index,
                "kind": "mensual",
                "scheduled_amount": amount,
                "due_date": due_date.isoformat(),
                "reference_month": due_date.strftime("%Y-%m"),
            })
    repository.append_many("installments", installment_rows)
    repository.append("payments", {
        "payment_id": uuid4().hex,
        "client_id": client_id,
        "installment_id": installment_rows[0]["installment_id"],
        "payment_date": client_entry_date.isoformat(),
        "amount": down_payment,
        "receipt_issued": "si" if receipt_issued else "no",
        "note": "Pie inicial registrado automáticamente.",
    })
    return client_id


def all_clients(repository: CsvRepository) -> list[dict[str, object]]:
    clients = []
    for row in repository.read("clients"):
        row["total_amount"] = int(row["total_amount"])
        row["installment_count"] = int(row["installment_count"])
        row["matter_label"] = MATTERS.get(row["matter"], row["matter"])
        row["total_display"] = format_money(row["total_amount"])
        clients.append(row)
    return clients


def find_client(repository: CsvRepository, client_id: str) -> dict[str, object] | None:
    return next((client for client in all_clients(repository) if client["client_id"] == client_id), None)


def _build_installments(client_id: str, total_amount: int, installment_count: int, first_date: date | None, entry_date: date) -> tuple[list[dict[str, object]], int]:
    down_payment = total_amount if installment_count == 0 else round(total_amount * 0.30)
    rows = [{
        "installment_id": uuid4().hex,
        "client_id": client_id,
        "number": 0,
        "kind": "unico" if installment_count == 0 else "pie",
        "scheduled_amount": down_payment,
        "due_date": entry_date.isoformat(),
        "reference_month": entry_date.strftime("%Y-%m"),
    }]
    if installment_count:
        amounts = distribute_amount(total_amount - down_payment, installment_count)
        for index, amount in enumerate(amounts, start=1):
            month_offset = first_date.month - 1 + index - 1
            year = first_date.year + month_offset // 12
            month = month_offset % 12 + 1
            due_date = due_date_for_month(year, month)
            rows.append({
                "installment_id": uuid4().hex,
                "client_id": client_id,
                "number": index,
                "kind": "mensual",
                "scheduled_amount": amount,
                "due_date": due_date.isoformat(),
                "reference_month": due_date.strftime("%Y-%m"),
            })
    return rows, down_payment


def update_client(
    repository: CsvRepository,
    client_id: str,
    full_name: str,
    matter: str,
    total_amount: int,
    pays_in_installments: bool,
    installment_count: int,
    first_installment_date: date | None,
    client_entry_date: date | None,
) -> None:
    client = find_client(repository, client_id)
    if not client:
        raise ValueError("El cliente no existe.")
    full_name = " ".join(full_name.split())
    if not full_name:
        raise ValueError("El nombre completo es obligatorio.")
    if matter not in MATTERS:
        raise ValueError("La materia seleccionada no es válida.")
    if total_amount <= 0:
        raise ValueError("El monto total debe ser mayor que cero.")
    if installment_count < 0:
        raise ValueError("La cantidad de cuotas no puede ser negativa.")
    if pays_in_installments and installment_count < 1:
        raise ValueError("Indique al menos una cuota posterior al pie.")
    if not pays_in_installments:
        installment_count = 0
        first_installment_date = None
    if pays_in_installments and first_installment_date is None:
        raise ValueError("La fecha de la primera cuota es obligatoria cuando el cliente paga en cuotas.")
    if client_entry_date is None:
        raise ValueError("La fecha de ingreso del cliente es obligatoria.")

    financial_change = (
        int(client["total_amount"]) != total_amount
        or client["pays_in_installments"] != ("si" if pays_in_installments else "no")
        or int(client["installment_count"]) != installment_count
        or client["first_installment_date"] != (first_installment_date.isoformat() if first_installment_date else "")
    )
    payments = repository.read("payments")
    client_payments = [row for row in payments if row["client_id"] == client_id]
    manual_payments = [row for row in client_payments if row["note"] != "Pie inicial registrado automáticamente."]
    if financial_change and manual_payments:
        raise ValueError("No se puede cambiar el plan porque el cliente ya tiene pagos registrados. Modifique solo sus datos personales.")

    clients = repository.read("clients")
    updated_client = {
        **next(row for row in clients if row["client_id"] == client_id),
        "full_name": full_name,
        "matter": matter,
        "total_amount": total_amount,
        "pays_in_installments": "si" if pays_in_installments else "no",
        "installment_count": installment_count,
        "first_installment_date": first_installment_date.isoformat() if first_installment_date else "",
        "created_at": client_entry_date.isoformat(),
    }
    repository.replace("clients", [updated_client if row["client_id"] == client_id else row for row in clients])

    if financial_change:
        today = date.today()
        new_installments, down_payment = _build_installments(client_id, total_amount, installment_count, first_installment_date, client_entry_date)
        repository.replace("installments", [row for row in repository.read("installments") if row["client_id"] != client_id] + new_installments)
        remaining_payments = [row for row in payments if row["client_id"] != client_id]
        remaining_payments.append({
            "payment_id": uuid4().hex,
            "client_id": client_id,
            "installment_id": new_installments[0]["installment_id"],
            "payment_date": client_entry_date.isoformat(),
            "amount": down_payment,
            "receipt_issued": "no",
            "note": "Pie inicial registrado automáticamente.",
        })
        repository.replace("payments", remaining_payments)


def delete_client(repository: CsvRepository, client_id: str) -> None:
    if not find_client(repository, client_id):
        raise ValueError("El cliente no existe.")
    repository.replace("clients", [row for row in repository.read("clients") if row["client_id"] != client_id])
    repository.replace("installments", [row for row in repository.read("installments") if row["client_id"] != client_id])
    repository.replace("payments", [row for row in repository.read("payments") if row["client_id"] != client_id])


def client_installments(repository: CsvRepository, client_id: str) -> list[dict[str, object]]:
    payments = payments_for_client(repository, client_id)
    paid_by_installment = defaultdict(int)
    for payment in payments:
        paid_by_installment[payment["installment_id"]] += payment["amount"]
    result = []
    today = date.today()
    for row in repository.read("installments"):
        if row["client_id"] != client_id:
            continue
        scheduled = int(row["scheduled_amount"])
        paid = paid_by_installment[row["installment_id"]]
        due = parse_date(row["due_date"])
        status = installment_status(scheduled, paid, due, today)
        result.append({
            **row,
            "number": int(row["number"]),
            "scheduled_amount": scheduled,
            "paid_amount": paid,
            "balance": max(scheduled - paid, 0),
            "due_date_display": due.strftime("%d-%m-%Y"),
            "scheduled_display": format_money(scheduled),
            "paid_display": format_money(paid),
            "balance_display": format_money(max(scheduled - paid, 0)),
            "status": status,
            "status_label": status_label(status),
        })
    return sorted(result, key=lambda item: item["number"])


def installment_status(scheduled: int, paid: int, due: date, today: date) -> str:
    if paid >= scheduled:
        return "paid"
    if paid > 0:
        return "overdue" if today > due else "partial"
    return "overdue" if today > due else "pending"


def status_label(status: str) -> str:
    return {
        "paid": "Pagada",
        "partial": "Abono parcial",
        "pending": "Pendiente",
        "overdue": "Atrasada",
        "not_applicable": "No aplica",
    }.get(status, status)


def payments_for_client(repository: CsvRepository, client_id: str) -> list[dict[str, object]]:
    rows = []
    for row in repository.read("payments"):
        if row["client_id"] == client_id:
            row["amount"] = int(row["amount"])
            rows.append(row)
    return rows


def record_payment(repository: CsvRepository, client_id: str, installment_id: str, payment_date: date, amount: int, receipt_issued: bool, note: str) -> None:
    client = find_client(repository, client_id)
    installment = next((row for row in repository.read("installments") if row["installment_id"] == installment_id and row["client_id"] == client_id), None)
    if not client or not installment:
        raise ValueError("El cliente o la cuota seleccionada no existe.")
    if amount <= 0:
        raise ValueError("El monto pagado debe ser mayor que cero.")
    paid = sum(int(row["amount"]) for row in repository.read("payments") if row["installment_id"] == installment_id)
    balance = int(installment["scheduled_amount"]) - paid
    if amount > balance:
        raise ValueError(f"El pago no puede superar el saldo pendiente de {format_money(balance)}.")
    repository.append("payments", {
        "payment_id": uuid4().hex,
        "client_id": client_id,
        "installment_id": installment_id,
        "payment_date": payment_date.isoformat(),
        "amount": amount,
        "receipt_issued": "si" if receipt_issued else "no",
        "note": note.strip(),
    })


def monthly_report(repository: CsvRepository, reference_date: date | None = None, as_of: date | None = None) -> list[dict[str, object]]:
    reference_date = reference_date or date.today()
    as_of = as_of or date.today()
    month = reference_date.strftime("%Y-%m")
    clients = {row["client_id"]: row for row in all_clients(repository)}
    payments = repository.read("payments")
    paid_by_installment = defaultdict(int)
    monthly_payments = defaultdict(int)
    last_receipt = {}
    for row in payments:
        amount = int(row["amount"])
        paid_by_installment[row["installment_id"]] += amount
        if row["payment_date"].startswith(month):
            monthly_payments[row["installment_id"]] += amount
            last_receipt[row["installment_id"]] = row["receipt_issued"]
    report = []
    for row in repository.read("installments"):
        if row["reference_month"] != month:
            continue
        client = clients[row["client_id"]]
        scheduled = int(row["scheduled_amount"])
        paid = paid_by_installment[row["installment_id"]]
        due = parse_date(row["due_date"])
        status = installment_status(scheduled, paid, due, as_of)
        report.append({
            "client_id": row["client_id"],
            "client_name": client["full_name"],
            "matter_label": client["matter_label"],
            "pays_in_installments": client["pays_in_installments"],
            "installment_id": row["installment_id"],
            "number": int(row["number"]),
            "kind": row["kind"],
            "scheduled": scheduled,
            "paid": monthly_payments[row["installment_id"]],
            "balance": max(scheduled - paid_by_installment[row["installment_id"]], 0),
            "status": status,
            "status_label": status_label(status),
            "receipt_issued": last_receipt.get(row["installment_id"], "-"),
            "scheduled_display": format_money(scheduled),
            "paid_display": format_money(monthly_payments[row["installment_id"]]),
            "balance_display": format_money(max(scheduled - paid_by_installment[row["installment_id"]], 0)),
        })
    return sorted(report, key=lambda row: row["client_name"].lower())


def dashboard(repository: CsvRepository, today: date | None = None) -> dict[str, object]:
    today = today or date.today()
    report = [
        row for row in monthly_report(repository, today)
        if row["pays_in_installments"] == "si" and row["number"] > 0
    ]
    payments_this_month = sum(
        int(row["amount"]) for row in repository.read("payments") if row["payment_date"].startswith(today.strftime("%Y-%m"))
    )
    paid_by_installment = defaultdict(int)
    for row in repository.read("payments"):
        paid_by_installment[row["installment_id"]] += int(row["amount"])
    current_month_start = today.replace(day=1)
    overdue_amount = 0
    overdue_count = 0
    overdue_by_client = defaultdict(lambda: {"amount": 0, "installments": 0})
    clients_by_id = {row["client_id"]: row for row in all_clients(repository)}
    for row in repository.read("installments"):
        if row["kind"] != "mensual":
            continue
        due = parse_date(row["due_date"])
        balance = max(int(row["scheduled_amount"]) - paid_by_installment[row["installment_id"]], 0)
        if balance > 0 and due < current_month_start:
            overdue_count += 1
            overdue_amount += balance
            overdue_by_client[row["client_id"]]["amount"] += balance
            overdue_by_client[row["client_id"]]["installments"] += 1
    overdue_amount += sum(row["balance"] for row in report if row["status"] == "overdue")
    expected = sum(row["scheduled"] for row in report)
    paid_count = sum(row["status"] == "paid" for row in report)
    overdue_count += sum(row["status"] == "overdue" for row in report)
    pending_count = sum(row["status"] in {"pending", "partial"} for row in report)
    overdue_clients = []
    for client_id, values in overdue_by_client.items():
        client = clients_by_id.get(client_id)
        if client:
            overdue_clients.append({
                "client_id": client_id,
                "full_name": client["full_name"],
                "matter_label": client["matter_label"],
                "installment_count": values["installments"],
                "amount": values["amount"],
                "amount_display": format_money(values["amount"]),
            })
    overdue_clients.sort(key=lambda client: client["full_name"].lower())
    target = 4_000_000
    return {
        "month_label": month_label(today.strftime("%Y-%m")),
        "income": payments_this_month,
        "income_display": format_money(payments_this_month),
        "target": target,
        "target_display": format_money(target),
        "remaining": max(target - payments_this_month, 0),
        "remaining_display": format_money(max(target - payments_this_month, 0)),
        "projected": expected,
        "projected_display": format_money(expected),
        "paid_count": paid_count,
        "overdue_count": overdue_count,
        "overdue_amount": overdue_amount,
        "overdue_amount_display": format_money(overdue_amount),
        "overdue_clients": overdue_clients,
        "pending_count": pending_count,
    }
