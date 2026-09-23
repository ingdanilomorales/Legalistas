from pathlib import Path
import os

from flask import Flask

from .repositories import CsvRepository
from .routes import register_routes


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="legalistas-local",
        DATA_DIR=Path(app.root_path).parent / "data",
    )
    if test_config:
        app.config.update(test_config)
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY")
    if supabase_url and supabase_key:
        from .supabase_repository import SupabaseRepository

        app.repository = SupabaseRepository(supabase_url, supabase_key)
        app.config["STORAGE_BACKEND"] = "supabase"
    else:
        app.repository = CsvRepository(Path(app.config["DATA_DIR"]))
        app.config["STORAGE_BACKEND"] = "csv"
    register_routes(app)
    return app
