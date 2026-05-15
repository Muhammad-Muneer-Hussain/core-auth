import pytest
from httpx import AsyncClient

# 1. Test Registration
@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    response = await async_client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data
    assert data["is_active"] is True

# 2. Test Login
@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    response = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

# 3. Test Protected Route Access
@pytest.mark.asyncio
async def test_protected_route_access(async_client: AsyncClient):
    # Login first
    login_resp = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    token = login_resp.json()["access_token"]
    
    # Access protected route
    response = await async_client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

# 4. Test Token Refresh
@pytest.mark.asyncio
async def test_token_refresh(async_client: AsyncClient):
    login_resp = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    refresh_token = login_resp.json()["refresh_token"]
    
    response = await async_client.post("/auth/refresh", json={
        "refresh_token": refresh_token
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

# 5. & 6. Test Logout & Zero Trust Validation
@pytest.mark.asyncio
async def test_logout_and_zero_trust(async_client: AsyncClient):
    login_resp = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "strongpassword123"
    })
    token = login_resp.json()["access_token"]
    
    # Logout
    logout_resp = await async_client.post("/auth/logout", headers={
        "Authorization": f"Bearer {token}"
    })
    assert logout_resp.status_code == 200
    assert logout_resp.json()["detail"] == "Revocation complete"
    
    # Zero Trust: Try using the same token again
    protected_resp = await async_client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert protected_resp.status_code == 401
    assert protected_resp.json()["detail"] == "Could not validate credentials"
