import pathlib
import typing

import requests

import dotjs

if typing.TYPE_CHECKING:
    from conftest import SecureTestServer


def test_https(
    tmp_path: pathlib.Path, secure_server: "SecureTestServer"
) -> None:
    ca_file = tmp_path / "ca.pem"
    ca_file.write_bytes(dotjs.cert)

    r = requests.get(secure_server.url, verify=str(ca_file))
    assert r.ok
    assert "dotjs is working!" in r.text
