import pathlib
import threading
import typing
from http.server import HTTPServer, ThreadingHTTPServer

import pytest

import dotjs


class TestServer(ThreadingHTTPServer):
    @property
    def url(self) -> str:
        return f"http://localhost:{self.server_address[-1]}/"


class SecureTestServer(dotjs.ThreadingSecureHTTPServer):
    @property
    def url(self) -> str:
        return f"https://localhost:{self.server_address[-1]}/"


def make_handler(directory: str) -> typing.Type[dotjs.Handler]:
    return type("TestHandler", (dotjs.Handler,), {"directory": directory})


Server = typing.TypeVar("Server", bound=HTTPServer)


def run_server(server: Server) -> typing.Iterable[Server]:
    thread = threading.Thread(target=server.serve_forever)
    thread.start()

    yield server

    server.shutdown()
    thread.join()


@pytest.fixture(name="server")
def server_fixture(tmp_path: pathlib.Path) -> typing.Iterable[TestServer]:
    server = TestServer(("127.0.0.1", 0), make_handler(str(tmp_path)))
    yield from run_server(server)


@pytest.fixture(name="secure_server")
def secure_server_fixture(
    tmp_path: pathlib.Path,
) -> typing.Iterable[SecureTestServer]:
    certificate = tmp_path / "dotjs.pem"
    certificate.write_bytes(dotjs.cert + dotjs.key)

    server = SecureTestServer(
        ("127.0.0.1", 0),
        make_handler(str(tmp_path)),
        certfile=str(certificate),
    )

    yield from run_server(server)
