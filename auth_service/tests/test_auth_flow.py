import pytest


@pytest.mark.asyncio
async def test_register_then_login(client):
    register_payload = {
        "name": "Bohdan",
        "surname": "Mykyichuk",
        "email": "bohdan@example.com",
        "date_of_birth": "2000-01-01",
        "password": "secret123",
    }
    r = await client.post("/auth/register", json=register_payload)
    assert r.status_code == 201, r.text

    login_payload = {"email": "bohdan@example.com", "password": "secret123"}
    r = await client.post("/auth/login", json=login_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
