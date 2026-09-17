# URL Monitor

A lightweight asynchronous CLI tool for checking the HTTP status and response time of multiple URLs.

## Features

- reads URLs from a JSON file
- asynchronous HTTP requests using `httpx.AsyncClient`
- concurrent execution with `asyncio.gather()`
- configurable request timeout
- reports HTTP status and response time
- handles timeout and connection errors
- unit and integration tests with `pytest`

## Requirements

- Python 3.14+
- runtime dependencies from `requirements.txt`
- development dependencies from `requirements-dev.txt`

## Installation

Create and activate a virtual environment in Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
py -3.14 -m pip install -r requirements.txt
```

For development and testing, install the development dependencies instead:

```powershell
py -3.14 -m pip install -r requirements-dev.txt
```

## Usage

```powershell
python app.py urls.json
python app.py urls.json --timeout 2
```

## Input file

The input file must be a JSON array of URLs:

```json
[
  "https://google.com",
  "https://github.com",
  "https://example.com"
]
```

## Testing

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest
```

## Docker

Build the container image:

```powershell
docker build -t url-monitor .
```

Run the application in a container:

```powershell
docker run --rm url-monitor
```

## Project structure

```text
url-monitor/
├── .dockerignore
├── .gitignore
├── Dockerfile
├── app.py
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── urls.json
└── tests/
    └── test_app.py
```
