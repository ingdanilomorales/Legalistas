from datetime import date

from app.repositories import CsvRepository
from app.services import client_installments, create_plan, dashboard, delete_client, monthly_report, record_payment, update_client


def test_create_plan_registers_down_payment_and_installments(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Ana Pérez",
        "familia",
        1_000_000,
        True,
        2,
        date(2026, 9, 10),
        date(2026, 9, 5),
    )

    installments = client_installments(repository, client_id)
    assert len(installments) == 3
    assert installments[0]["scheduled_amount"] == 300_000
    assert installments[1]["scheduled_amount"] == 350_000
    assert installments[2]["scheduled_amount"] == 350_000
    assert installments[0]["status"] == "paid"


def test_create_plan_records_receipt_for_initial_payment(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Cliente con boleta",
        "familia",
        500_000,
        True,
        1,
        date(2026, 9, 10),
        date(2026, 9, 5),
        receipt_issued=True,
    )

    payment = next(row for row in repository.read("payments") if row["client_id"] == client_id)
    assert payment["receipt_issued"] == "si"


def test_single_payment_receipt_is_recorded(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Cliente pago único",
        "asesoria",
        150_000,
        False,
        0,
        None,
        date(2026, 9, 22),
        receipt_issued=True,
    )

    payment = next(row for row in repository.read("payments") if row["client_id"] == client_id)
    assert payment["amount"] == "150000"
    assert payment["receipt_issued"] == "si"


def test_payment_updates_status_and_monthly_dashboard(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Luis Soto",
        "laboral",
        500_000,
        True,
        1,
        date(2026, 9, 1),
        date(2026, 9, 1),
    )
    installment = client_installments(repository, client_id)[1]
    record_payment(repository, client_id, installment["installment_id"], date(2026, 9, 22), 350_000, True, "Transferencia")

    report = monthly_report(repository, date(2026, 9, 22))
    summary = dashboard(repository, date(2026, 9, 22))
    row = next(item for item in report if item["installment_id"] == installment["installment_id"])
    assert row["status"] == "paid"
    assert row["paid"] == 350_000
    assert summary["income"] == 500_000
    assert summary["projected"] == 350_000
    assert summary["paid_count"] == 1


def test_installments_can_be_below_previous_minimum(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Marta Díaz",
        "otro",
        100_000,
        True,
        2,
        date(2026, 9, 1),
        date(2026, 9, 1),
    )

    installments = client_installments(repository, client_id)
    assert installments[1]["scheduled_amount"] == 35_000
    assert installments[2]["scheduled_amount"] == 35_000


def test_update_client_changes_profile_and_rebuilds_unpaid_plan(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Marta Díaz",
        "otro",
        100_000,
        True,
        2,
        date(2026, 9, 1),
        date(2026, 9, 1),
    )

    update_client(repository, client_id, "Marta González", "familia", 200_000, True, 1, date(2026, 10, 1), date(2026, 9, 5))

    installments = client_installments(repository, client_id)
    assert installments[0]["scheduled_amount"] == 60_000
    assert installments[1]["scheduled_amount"] == 140_000
    assert repository.read("clients")[0]["full_name"] == "Marta González"
    assert repository.read("clients")[0]["matter"] == "familia"


def test_update_client_preserves_history_by_rejecting_financial_changes(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(repository, "Luis Soto", "laboral", 500_000, True, 1, date(2026, 9, 1), date(2026, 9, 1))
    installment = client_installments(repository, client_id)[1]
    record_payment(repository, client_id, installment["installment_id"], date(2026, 9, 22), 350_000, True, "Transferencia")

    try:
        update_client(repository, client_id, "Luis Soto", "familia", 600_000, True, 1, date(2026, 9, 1), date(2026, 9, 1))
    except ValueError as error:
        assert "pagos registrados" in str(error)
    else:
        raise AssertionError("Se esperaba bloquear el cambio financiero con pagos manuales")


def test_delete_client_removes_related_records(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(repository, "Ana Pérez", "familia", 300_000, True, 1, date(2026, 9, 1), date(2026, 9, 1))

    delete_client(repository, client_id)

    assert repository.read("clients") == []
    assert repository.read("installments") == []
    assert repository.read("payments") == []


def test_single_payment_does_not_require_first_installment_date(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(repository, "Paula Rojas", "asesoria", 300_000, False, 0, None, date(2026, 9, 22))

    client = repository.read("clients")[0]
    installments = client_installments(repository, client_id)
    assert client["created_at"] == "2026-09-22"
    assert client["first_installment_date"] == ""
    assert len(installments) == 1
    assert installments[0]["scheduled_amount"] == 300_000


def test_single_payment_counts_as_monthly_income_not_installment_projection(tmp_path):
    repository = CsvRepository(tmp_path)
    create_plan(repository, "Paula Rojas", "asesoria", 300_000, False, 0, None, date(2026, 9, 22))

    summary = dashboard(repository, date(2026, 9, 22))

    assert summary["income"] == 300_000
    assert summary["projected"] == 0
    assert summary["paid_count"] == 0
    assert summary["pending_count"] == 0
    assert summary["overdue_count"] == 0


def test_historical_down_payment_is_not_current_month_income(tmp_path):
    repository = CsvRepository(tmp_path)
    client_id = create_plan(
        repository,
        "Cliente antiguo",
        "familia",
        1_000_000,
        True,
        2,
        date(2026, 9, 1),
        date(2026, 8, 20),
    )

    summary_before_payment = dashboard(repository, date(2026, 9, 22))
    assert summary_before_payment["income"] == 0
    assert summary_before_payment["projected"] == 350_000
    assert summary_before_payment["pending_count"] == 1

    installment = client_installments(repository, client_id)[1]
    record_payment(repository, client_id, installment["installment_id"], date(2026, 9, 22), 350_000, False, "Pago septiembre")
    summary_after_payment = dashboard(repository, date(2026, 9, 22))
    assert summary_after_payment["income"] == 350_000
    assert summary_after_payment["projected"] == 350_000
    assert summary_after_payment["paid_count"] == 1


def test_monthly_report_supports_previous_and_future_months(tmp_path):
    repository = CsvRepository(tmp_path)
    create_plan(
        repository,
        "Cliente con historial",
        "familia",
        1_000_000,
        True,
        2,
        date(2026, 9, 1),
        date(2026, 8, 20),
    )

    previous_report = monthly_report(repository, date(2026, 8, 1), date(2026, 9, 22))
    future_report = monthly_report(repository, date(2026, 10, 1), date(2026, 9, 22))

    assert [row["kind"] for row in previous_report] == ["pie"]
    assert future_report[0]["number"] == 2
    assert future_report[0]["status"] == "pending"


def test_unpaid_previous_installment_is_carried_into_current_arrears(tmp_path):
    repository = CsvRepository(tmp_path)
    create_plan(
        repository,
        "Cliente con atraso",
        "laboral",
        1_000_000,
        True,
        2,
        date(2026, 8, 1),
        date(2026, 7, 20),
    )

    summary = dashboard(repository, date(2026, 9, 22))

    assert summary["projected"] == 350_000
    assert summary["pending_count"] == 1
    assert summary["overdue_count"] == 1
    assert summary["overdue_amount"] == 350_000


def test_dashboard_lists_delinquent_clients_and_total_overdue(tmp_path):
    repository = CsvRepository(tmp_path)
    create_plan(
        repository,
        "Cliente moroso",
        "laboral",
        1_000_000,
        True,
        3,
        date(2026, 7, 1),
        date(2026, 6, 20),
    )

    summary = dashboard(repository, date(2026, 9, 22))

    assert len(summary["overdue_clients"]) == 1
    assert summary["overdue_clients"][0]["full_name"] == "Cliente moroso"
    assert summary["overdue_clients"][0]["installment_count"] == 2
    assert summary["overdue_clients"][0]["amount"] == 466_667
