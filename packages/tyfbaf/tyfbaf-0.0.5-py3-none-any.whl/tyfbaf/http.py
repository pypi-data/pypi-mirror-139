from typing import Any
import httpx

SERVER_NAME = None
PORT = 6405
BASE_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def _setup(server_name: str, port: int = 6405) -> None:
    global SERVER_NAME, PORT
    SERVER_NAME = server_name
    PORT = port


def get(endpoint: str, *, token: str = None) -> dict[str, Any]:
    response = httpx.get(
        f"http://{SERVER_NAME}:{PORT}/biprws{endpoint}",
        headers=(
            {"X-SAP-LogonToken": token, **BASE_HEADERS} if token else BASE_HEADERS
        ),
    )
    return response.json() if response.text else {}


def post(endpoint: str, *, body: dict = None, token: str = None) -> dict[str, Any]:
    response = httpx.post(
        f"http://{SERVER_NAME}:{PORT}/biprws{endpoint}",
        headers=(
            {"X-SAP-LogonToken": token, **BASE_HEADERS} if token else BASE_HEADERS
        ),
        json=body,
    )
    return response.json() if response.text else {}
