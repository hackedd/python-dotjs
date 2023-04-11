import pathlib
import typing

import requests

if typing.TYPE_CHECKING:
    from conftest import TestServer


def test_index(server: "TestServer") -> None:
    r = requests.get(server.url)
    assert r.ok
    assert "dotjs is working!" in r.text


def test_default_js(tmp_path: pathlib.Path, server: "TestServer") -> None:
    (tmp_path / "default.js").write_text("// This is default.js\n")
    (tmp_path / "example.com.js").write_text("// This is example.com.js\n")
    (tmp_path / "example.org.js").write_text("// This is example.org.js\n")

    r = requests.get(f"{server.url}example.com.js")
    assert r.ok
    assert "// This is default.js\n" in r.text
    assert "// This is example.com.js\n" in r.text
    assert "// This is example.org.js\n" not in r.text


def test_multiple_subdomains(
    tmp_path: pathlib.Path, server: "TestServer"
) -> None:
    (tmp_path / "www.example.com.js").write_text(
        "// This is www.example.com\n"
    )
    (tmp_path / "example.com.js").write_text("// This is example.com\n")
    (tmp_path / "com.js").write_text("// This is com\n")
    (tmp_path / "example.org.js").write_text("// This is example.org.js\n")

    r = requests.get(f"{server.url}www.example.com.js")
    assert r.ok
    assert "// This is www.example.com\n" in r.text
    assert "// This is example.com\n" in r.text
    assert "// This is com\n" in r.text
    assert "// This is example.org.js\n" not in r.text
