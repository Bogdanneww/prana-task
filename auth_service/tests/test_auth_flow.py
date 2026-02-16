import uuid
import pytest


@pytest.mark.asyncio
async def test_register_then_login(client):
    unique_email = f"bohdan+{uuid.uuid4().hex}@example.com"

    register_payload = {
        "name": "Bobbi",
        "surname": "Myk",
        "email": unique_email,
        "date_of_birth": "2000-02-02",
        "password": "secret123",
    }

    r = await client.post("/auth/register", json=register_payload)
    assert r.status_code == 201, r.text

    r = await client.post("/auth/login", json={"email": unique_email, "password": "secret123"})
    assert r.status_code == 200, r.text
    assert "access_token" in r.json()
