import csv
from pathlib import Path
from typing import Iterable


CLIENT_FIELDS = [
    "client_id",
    "full_name",
    "matter",
    "total_amount",
    "pays_in_installments",
    "installment_count",
    "first_installment_date",
    "created_at",
    "status",
]
INSTALLMENT_FIELDS = [
    "installment_id",
    "client_id",
    "number",
    "kind",
    "scheduled_amount",
    "due_date",
    "reference_month",
]
PAYMENT_FIELDS = [
    "payment_id",
    "client_id",
    "installment_id",
    "payment_date",
    "amount",
    "receipt_issued",
    "note",
]


class CsvRepository:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.paths = {
            "clients": self.data_dir / "clientes.csv",
            "installments": self.data_dir / "cuotas.csv",
            "payments": self.data_dir / "pagos.csv",
        }
        self.fields = {
            "clients": CLIENT_FIELDS,
            "installments": INSTALLMENT_FIELDS,
            "payments": PAYMENT_FIELDS,
        }
        self.ensure_files()

    def ensure_files(self) -> None:
        for name, path in self.paths.items():
            if not path.exists() or path.stat().st_size == 0:
                with path.open("w", newline="", encoding="utf-8") as file:
                    csv.DictWriter(file, fieldnames=self.fields[name]).writeheader()

    def read(self, name: str) -> list[dict[str, str]]:
        with self.paths[name].open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def append(self, name: str, row: dict[str, object]) -> None:
        with self.paths[name].open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields[name])
            writer.writerow({field: row.get(field, "") for field in self.fields[name]})

    def append_many(self, name: str, rows: Iterable[dict[str, object]]) -> None:
        with self.paths[name].open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields[name])
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in self.fields[name]})

    def replace(self, name: str, rows: Iterable[dict[str, object]]) -> None:
        temporary_path = self.paths[name].with_suffix(".tmp")
        with temporary_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fields[name])
            writer.writeheader()
            for row in rows:
                writer.writerow({field: row.get(field, "") for field in self.fields[name]})
        temporary_path.replace(self.paths[name])
