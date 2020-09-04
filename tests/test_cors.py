import pytest

import requests


@pytest.mark.parametrize("domain, origin", [
    ("example.com", "http://example.com"),
    ("example.com", "https://example.com"),
    ("example.com", "http://example.com:1234"),
    ("example.com", "https://example.com:1234"),
])
def test_cors_valid_origin(server, domain, origin):
    r = requests.get(f"{server.url}{domain}.js", headers={"Origin": origin})
    assert r.ok
    assert r.headers["Access-Control-Allow-Origin"] == origin


@pytest.mark.parametrize("domain, origin", [
    ("example.com", "http://example.org"),
    ("example.com", "https://www.example.com"),
    ("example.com", "null"),
])
def test_cors_invalid_origin(server, domain, origin):
    r = requests.get(f"{server.url}{domain}.js", headers={"Origin": origin})
    assert r.ok
    assert "Access-Control-Allow-Origin" not in r.headers
