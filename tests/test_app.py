import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import httpx
import pytest

import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
async def test_check_url_returns_status_200():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.return_value = Mock(status_code=200)

    result = await app.check_url(client, "https://example.com", 5.0)

    assert "200" in result
    client.get.assert_awaited_once_with("https://example.com", timeout=5.0)


@pytest.mark.anyio
async def test_check_url_returns_timeout():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.side_effect = httpx.TimeoutException("Request timed out")

    result = await app.check_url(client, "https://example.com", 5.0)

    assert result == "https://example.com: TIMEOUT"


@pytest.mark.anyio
async def test_check_url_returns_connection_error():
    client = AsyncMock(spec=httpx.AsyncClient)
    client.get.side_effect = httpx.ConnectError("Connection failed")

    result = await app.check_url(client, "https://example.com", 5.0)

    assert "CONNECTION_ERROR" in result


def test_cli_returns_status_200_with_mocked_httpx(tmp_path):
    input_file = tmp_path / "urls.json"
    input_file.write_text(json.dumps(["https://example.com"]), encoding="utf-8")

    mock_httpx = tmp_path / "httpx.py"
    mock_httpx.write_text(
        """
class TimeoutException(Exception):
    pass


class ConnectError(Exception):
    pass


class Response:
    status_code = 200


class AsyncClient:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def get(self, url, timeout):
        return Response()
""",
        encoding="utf-8",
    )

    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(tmp_path) + os.pathsep + environment.get("PYTHONPATH", "")
    app_path = Path(app.__file__)
    process = subprocess.run(
        [sys.executable, str(app_path), str(input_file), "--timeout", "5"],
        capture_output=True,
        text=True,
        env=environment,
    )

    assert process.returncode == 0
    assert "200" in process.stdout
