import pytest
import app


@pytest.fixture
def client():
    return app.test_client()
