import requests


def test_index(server):
    r = requests.get(server.url)
    assert r.ok
    assert "dotjs is working!" in r.text


def test_default_js(tmpdir, server):
    tmpdir.join("default.js").write("// This is default.js\n")
    tmpdir.join("example.com.js").write("// This is example.com.js\n")
    tmpdir.join("example.org.js").write("// This is example.org.js\n")

    r = requests.get(f"{server.url}example.com.js")
    assert r.ok
    assert "// This is default.js\n" in r.text
    assert "// This is example.com.js\n" in r.text
    assert "// This is example.org.js\n" not in r.text


def test_multiple_subdomains(tmpdir, server):
    tmpdir.join("www.example.com.js").write("// This is www.example.com\n")
    tmpdir.join("example.com.js").write("// This is example.com\n")
    tmpdir.join("com.js").write("// This is com\n")
    tmpdir.join("example.org.js").write("// This is example.org.js\n")

    r = requests.get(f"{server.url}www.example.com.js")
    assert r.ok
    assert "// This is www.example.com\n" in r.text
    assert "// This is example.com\n" in r.text
    assert "// This is com\n" in r.text
    assert "// This is example.org.js\n" not in r.text
