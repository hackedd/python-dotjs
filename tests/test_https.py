import requests

import dotjs


def test_https(tmpdir, secure_server):
    ca_file = tmpdir.join("ca.pem")
    ca_file.write(dotjs.cert)

    r = requests.get(secure_server.url, verify=ca_file)
    assert r.ok
    assert "dotjs is working!" in r.text
