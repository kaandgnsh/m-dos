# M-DOS · LOCAL LAB

<p align="center">
  <strong>A minimal HTTP response-time analyzer for local development environments.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/KAAN%20DO%C4%9EAN-SECURITY%20LAB-151515?style=for-the-badge&logo=linux&logoColor=white" alt="Kaan DOĞAN Security Lab">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Dependencies-Standard%20Library-444444?style=for-the-badge" alt="Standard library only">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/SCOPE-LOOPBACK%20ONLY-315C45?style=flat-square" alt="Loopback only">
  <img src="https://img.shields.io/badge/REQUEST%20CAP-60-555555?style=flat-square" alt="Maximum 60 requests">
  <img src="https://img.shields.io/badge/RUNTIME%20CAP-30s-555555?style=flat-square" alt="Maximum 30 seconds">
  <a href="https://github.com/kaandgnsh/m-dos/actions/workflows/tests.yml">
    <img src="https://github.com/kaandgnsh/m-dos/actions/workflows/tests.yml/badge.svg?branch=main" alt="GitHub Actions">
  </a>
</p>

---

## Overview

**M-DOS Local Lab** is a small Python learning project for measuring HTTP response times and observing basic behavior from services running on your own machine.

It focuses on practical fundamentals: HTTP, input validation, timing, error handling, testable code, and safe-by-default tooling.

> **Educational use only:** This project is for learning HTTP behavior and measuring response times in a controlled local lab. Run it only against services on your own machine or targets you are explicitly authorized to test. It intentionally does not support remote hosts, traffic flooding, or denial-of-service activity. This notice does not exempt users from applicable laws or service terms.

> **Safety by design:** M-DOS accepts loopback targets only. Remote hosts, flood modes, proxies, port scanning, and concurrent workers are intentionally unsupported.

## Features

| Feature | Details |
|:--|:--|
| Response-time sampling | Measures each request's elapsed time in milliseconds |
| HTTP status tracking | Records response status codes, including HTTP errors |
| Summary output | Reports request count, errors, and min/max/mean latency |
| JSON summary | Prints machine-readable summary data to the terminal |
| Bounded execution | Maximum 30 seconds and 60 requests |
| Loopback validation | Accepts `localhost` and loopback IP addresses only |
| Zero dependencies | Uses Python's standard library |
| Unit tests | Covers target and duration validation |

## Quick Start

### Requirements

- Python 3.10 or newer
- Git

No third-party Python packages are required.

### 1 · Clone the repository

```bash
git clone https://github.com/kaandgnsh/m-dos.git
cd m-dos
```

### 2 · Start a local test server

In your first terminal:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

This server binds to the loopback interface and is intended for local testing.

### 3 · Run M-DOS

In a second terminal, from the repository root:

```bash
python m-dos/m-dos.py --url http://127.0.0.1:8000/ --duration 10
```

### 4 · Run the tests

```bash
python -m unittest discover -s m-dos -p 'test_*.py' -v
```

## CLI Reference

| Argument | Required | Description |
|:--|:--:|:--|
| `--url` | Yes | Local HTTP or HTTPS URL to sample |
| `--duration` | No | Sampling duration in seconds; range: 1–30, default: 10 |
| `-h, --help` | No | Display help and exit |

## Example Output

```text
Local lab target: http://127.0.0.1:8000/
Safety limits: <= 30s, <= 60 requests, one worker.
01 status=200 latency=3.42ms error=-
02 status=200 latency=2.81ms error=-

Summary:
{
  "target": "http://127.0.0.1:8000/",
  "requests": 2,
  "successful_http_responses": 2,
  "errors": 0,
  "latency_ms": {
    "min": 2.81,
    "max": 3.42,
    "mean": 3.12
  }
}
```

*Illustrative output only. Actual timings depend on your machine and local service.*

## Safety Limits

| Control | Limit |
|:--|:--|
| Allowed targets | `localhost` and loopback IP addresses |
| Runtime | 1–30 seconds |
| Total requests | At most 60 |
| Workers | One |
| Request start interval | At least 0.5 seconds |
| Proxy handling | Environment proxies are disabled |

Use this tool only with local services you control. This project is a learning utility, not a production load-testing benchmark or a security scanner.

## Project Structure

```text
m-dos/
├── .github/
│   └── workflows/
│       └── tests.yml
├── m-dos/
│   ├── m-dos.py
│   └── test_m_dos.py
└── README.md
```

## Testing & CI

GitHub Actions is configured to compile the source and run the unit tests on Python 3.10, 3.11, and 3.12.

The tests currently cover:
- Valid loopback hostnames and IP addresses
- Rejection of remote targets
- Rejection of unsupported URL schemes
- Rejection of credentials embedded in URLs
- Duration boundaries

A passing test suite is useful evidence, not a guarantee that every possible defect has been found.

## Troubleshooting

### Connection refused

Make sure the local HTTP server is running and listening on port 8000:

```bash
ss -ltn
```

### Target rejected

Only loopback addresses are allowed. For example:

```bash
python m-dos/m-dos.py --url http://127.0.0.1:8000/ --duration 5
```

### Python version

Check your interpreter:

```bash
python --version
```

Use Python 3.10 or newer.

## Roadmap

- [x] Loopback-only target validation
- [x] Runtime and request-count limits
- [x] Remove flood-oriented functionality
- [x] Add input-validation unit tests
- [x] Add GitHub Actions workflow
- [ ] Export reports to CSV
- [ ] Add median and percentile latency metrics
- [ ] Expand HTTP error-handling tests

## Contributing

Focused improvements are welcome. Please keep changes documented, tested, and consistent with the local-only safety model.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Open a pull request with a concise description.

## Security

Please report security concerns privately to the repository owner. Do not publish sensitive details in a public issue.

## Author

**Kaan DOĞAN** · [GitHub Profile](https://github.com/kaandgnsh) · [LinkedIn](https://www.linkedin.com/in/kaan-do%C4%9Fan-911663280/) · [Instagram](https://instagram.com/kaandgn.sh)

<p align="center">
  <sub>Built to learn. Designed with safety in mind.</sub>
</p>
