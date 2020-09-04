import threading
from http.server import ThreadingHTTPServer

import pytest

import dotjs


def make_handler(directory):
    return type("TestHandler", (dotjs.Handler, ), {"directory": directory})


def run_server(server):
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()
    thread.join()


@pytest.fixture(name="server")
def server_fixture(tmpdir):
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(tmpdir))

    server.url = f"http://localhost:{server.server_address[-1]}/"

    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()
    thread.join()


@pytest.fixture(name="secure_server")
def secure_server_fixture(tmpdir):
    certificate = tmpdir.join("dotjs.pem")
    certificate.write(dotjs.cert + dotjs.key)

    server = dotjs.ThreadingSecureHTTPServer(
        ("127.0.0.1", 0),
        make_handler(tmpdir),
        certfile=str(certificate),
    )

    server.url = f"https://localhost:{server.server_address[-1]}/"

    yield from run_server(server)
