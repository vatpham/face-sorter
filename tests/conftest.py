import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app


@pytest.fixture(autouse=True)
def app_context():
    app = create_app()
    with app.app_context():
        yield
