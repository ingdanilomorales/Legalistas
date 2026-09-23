from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Client:
    client_id: str
    full_name: str
    matter: str
    total_amount: int
    pays_in_installments: bool
    installment_count: int
    first_installment_date: date | None
    created_at: date
    status: str = "active"


@dataclass(frozen=True)
class Installment:
    installment_id: str
    client_id: str
    number: int
    kind: str
    scheduled_amount: int
    due_date: date
    reference_month: str


@dataclass(frozen=True)
class Payment:
    payment_id: str
    client_id: str
    installment_id: str
    payment_date: date
    amount: int
    receipt_issued: bool
    note: str = ""
