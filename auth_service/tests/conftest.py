import pytest
from httpx import AsyncClient

from auth_service.app.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
