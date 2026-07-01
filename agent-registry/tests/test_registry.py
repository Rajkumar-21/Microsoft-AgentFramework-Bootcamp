"""API tests — run fully in-memory with dev auth (no cloud needed)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

ADMIN = {"Authorization": "Bearer dev"}
READER = {"Authorization": "Bearer dev Registry.Read"}
PUBLISHER = {"Authorization": "Bearer dev Registry.Read Registry.Publish"}


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    with TestClient(app) as c:  # triggers lifespan (seed + store init)
        yield c


def test_health_is_ok(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["store"] == "memory"
    assert body["auth_mode"] == "dev"


def test_requires_auth(client: TestClient) -> None:
    assert client.get("/agents").status_code == 401


def test_me_reports_scopes(client: TestClient) -> None:
    resp = client.get("/me", headers=READER)
    assert resp.status_code == 200
    assert resp.json()["scopes"] == ["Registry.Read"]


def test_seeded_catalog_is_listed(client: TestClient) -> None:
    for path in ("/agents", "/mcp-servers", "/skills"):
        resp = client.get(path, headers=READER)
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1


def test_search_and_tag_filter(client: TestClient) -> None:
    resp = client.get("/agents", headers=READER, params={"q": "support"})
    assert resp.status_code == 200
    names = [a["name"] for a in resp.json()["items"]]
    assert any("Atlas" in n for n in names)

    resp = client.get("/agents", headers=READER, params={"tag": "capstone"})
    assert resp.json()["total"] == 1


def test_reader_cannot_publish(client: TestClient) -> None:
    payload = {
        "name": "Blocked Agent",
        "summary": "Should not be created.",
        "endpoint": "https://example.com/a2a",
    }
    resp = client.post("/agents", headers=READER, json=payload)
    assert resp.status_code == 403


def test_publish_get_update_delete_agent(client: TestClient) -> None:
    payload = {
        "name": "Orion Planner",
        "summary": "Plans multi-step tasks.",
        "endpoint": "https://orion.contoso.com/a2a",
        "protocol": "a2a",
        "tags": ["planner"],
    }
    created = client.post("/agents", headers=PUBLISHER, json=payload)
    assert created.status_code == 201
    agent_id = created.json()["id"]
    assert created.json()["publisher"]["id"] == "dev-user"

    got = client.get(f"/agents/{agent_id}", headers=READER)
    assert got.status_code == 200

    patched = client.patch(
        f"/agents/{agent_id}",
        headers=PUBLISHER,
        json={"summary": "Updated summary.", "version": "1.1.0"},
    )
    assert patched.status_code == 200
    assert patched.json()["version"] == "1.1.0"

    # Publisher lacks Manage → cannot delete.
    assert client.delete(f"/agents/{agent_id}", headers=PUBLISHER).status_code == 403
    # Admin (bare dev) can delete.
    assert client.delete(f"/agents/{agent_id}", headers=ADMIN).status_code == 204
    assert client.get(f"/agents/{agent_id}", headers=READER).status_code == 404


def test_publish_mcp_server_and_skill(client: TestClient) -> None:
    server = client.post(
        "/mcp-servers",
        headers=PUBLISHER,
        json={
            "name": "Weather MCP",
            "summary": "Weather tools.",
            "url": "https://weather.contoso.com/mcp",
        },
    )
    assert server.status_code == 201

    skill = client.post(
        "/skills",
        headers=PUBLISHER,
        json={
            "name": "Summarize",
            "summary": "Summarize text.",
            "skill_kind": "prompt",
            "spec": "kind: prompt\nname: summarize\n",
        },
    )
    assert skill.status_code == 201
    assert skill.json()["skill_kind"] == "prompt"
