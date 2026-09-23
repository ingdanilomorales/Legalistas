from pathlib import Path

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
    app.repository = CsvRepository(Path(app.config["DATA_DIR"]))
    register_routes(app)
    return app
