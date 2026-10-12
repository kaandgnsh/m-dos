# M-DOS Local Lab

A small, bounded HTTP response-time sampler for **local development services**. This repository is being refocused from its original flood-oriented implementation into a safer learning project for Python, HTTP, input validation, and basic performance observation.

> **Scope by design:** only `localhost` and loopback IP addresses (`127.0.0.1`, `::1`) are accepted. Remote targets, flood modes, proxies, multiple workers, and port scanning are not supported.

## Features

- Measures HTTP response latency against a local service
- Records HTTP status codes and request errors
- Prints a JSON summary with minimum, maximum, and mean latency
- Uses only the Python standard library
- Enforces a maximum duration of 30 seconds, a maximum of 60 requests, and a fixed interval of at least 0.5 seconds between requests
- Includes input-validation unit tests

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Run a local test service

In one terminal, start Python's built-in HTTP server:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

In another terminal, run the sampler from the repository root:

```bash
python m-dos/m-dos.py --url http://127.0.0.1:8000/ --duration 10
```

Use only services you own or are explicitly authorized to test. The program rejects non-loopback hosts and does not follow proxy environment settings.

## Run tests

```bash
python -m unittest discover -s m-dos -p 'test_*.py' -v
```

## Project structure

```text
m-dos/
├── m-dos.py
└── test_m_dos.py
```

## Limitations

This is a learning tool, not a load-testing benchmark or a security scanner. Latency results depend on the local machine, service, and operating system. The tool does not attempt to estimate production capacity and deliberately caps request rate and total work.

## Roadmap

- [x] Restrict targets to loopback addresses
- [x] Add bounded runtime and request count
- [x] Remove flood, proxy, and multi-target functionality
- [x] Add validation tests
- [ ] Add CI checks for supported Python versions
- [ ] Add optional CSV export and richer latency percentiles

## Security

Please report potential security issues privately to the repository owner. Do not use this project to send traffic to systems you do not own or have explicit permission to test.

## Author

**KaanDGN** · [GitHub](https://github.com/kaandgnsh)
