from typing import Iterable

from supabase import Client, create_client

from .repositories import CLIENT_FIELDS, INSTALLMENT_FIELDS, PAYMENT_FIELDS


class SupabaseRepository:
    """Repository compatible with the CSV repository, backed by Supabase."""

    TABLES = {
        "clients": ("clients", "client_id", CLIENT_FIELDS),
        "installments": ("installments", "installment_id", INSTALLMENT_FIELDS),
        "payments": ("payments", "payment_id", PAYMENT_FIELDS),
    }

    def __init__(self, url: str, key: str):
        self.client: Client = create_client(url, key)

    def read(self, name: str) -> list[dict[str, object]]:
        table, _, _ = self.TABLES[name]
        rows = self.client.table(table).select("*").execute().data or []
        for row in rows:
            if name == "clients" and row.get("first_installment_date") is None:
                row["first_installment_date"] = ""
        return rows

    def append(self, name: str, row: dict[str, object]) -> None:
        self.append_many(name, [row])

    def append_many(self, name: str, rows: Iterable[dict[str, object]]) -> None:
        table, _, fields = self.TABLES[name]
        payload = []
        for row in rows:
            item = {field: row.get(field, "") for field in fields}
            if name == "clients" and item["first_installment_date"] == "":
                item["first_installment_date"] = None
            payload.append(item)
        if payload:
            self.client.table(table).insert(payload).execute()

    def replace(self, name: str, rows: Iterable[dict[str, object]]) -> None:
        table, primary_key, fields = self.TABLES[name]
        self.client.table(table).delete().neq(primary_key, "").execute()
        self.append_many(name, rows)
