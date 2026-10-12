#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KaanDGN M-DOS Local Lab
"""Bounded HTTP response-time sampler for loopback development services.

This tool intentionally accepts only localhost/loopback targets. It is not a
network stress tool and does not support remote hosts, floods, proxies,
multiple workers, or port scanning.
"""

from __future__ import annotations

import argparse
import ipaddress
import json
import statistics
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import ProxyHandler, Request, build_opener

MAX_DURATION_SECONDS = 30
MAX_REQUESTS = 60
REQUEST_INTERVAL_SECONDS = 0.5
REQUEST_TIMEOUT_SECONDS = 2


def validate_target(url: str) -> str:
    """Return a normalized URL only when it points to a loopback host."""
    parsed = urlparse(url.strip())
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only http:// and https:// URLs are supported.")
    if not parsed.hostname:
        raise ValueError("A hostname is required.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed.")
    if parsed.hostname.lower() == "localhost":
        pass
    else:
        try:
            address = ipaddress.ip_address(parsed.hostname)
        except ValueError as exc:
            raise ValueError("Target must be localhost, 127.0.0.1, or ::1.") from exc
        if not address.is_loopback:
            raise ValueError("Remote targets are blocked; use a loopback address only.")
    if parsed.port is not None and not 1 <= parsed.port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")
    return url.strip()


def validate_duration(duration: int) -> int:
    if not 1 <= duration <= MAX_DURATION_SECONDS:
        raise ValueError(f"Duration must be between 1 and {MAX_DURATION_SECONDS} seconds.")
    return duration


def sample(url: str, duration: int) -> dict:
    """Make at most two requests per second for at most 30 seconds."""
    target = validate_target(url)
    duration = validate_duration(duration)
    opener = build_opener(ProxyHandler({}))
    results: list[dict] = []
    deadline = time.monotonic() + duration
    next_request = time.monotonic()

    print(f"Local lab target: {target}")
    print(f"Safety limits: <= {MAX_DURATION_SECONDS}s, <= {MAX_REQUESTS} requests, one worker.")
    while time.monotonic() < deadline and len(results) < MAX_REQUESTS:
        delay = next_request - time.monotonic()
        if delay > 0:
            time.sleep(min(delay, max(0, deadline - time.monotonic())))
        if time.monotonic() >= deadline:
            break

        started = time.monotonic()
        status = None
        error = None
        try:
            request = Request(target, headers={"User-Agent": "M-DOS-Local-Lab/1.0"})
            with opener.open(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
                status = response.status
                response.read(1024)
        except HTTPError as exc:
            status = exc.code
        except (URLError, TimeoutError, OSError) as exc:
            error = type(exc).__name__

        elapsed_ms = round((time.monotonic() - started) * 1000, 2)
        results.append({"status": status, "elapsed_ms": elapsed_ms, "error": error})
        print(f"{len(results):02d} status={status or '-'} latency={elapsed_ms}ms error={error or '-'}")
        next_request = started + REQUEST_INTERVAL_SECONDS

    latencies = [item["elapsed_ms"] for item in results]
    summary = {
        "target": target,
        "requests": len(results),
        "successful_http_responses": sum(item["status"] is not None for item in results),
        "errors": sum(item["error"] is not None for item in results),
        "latency_ms": {
            "min": min(latencies) if latencies else None,
            "max": max(latencies) if latencies else None,
            "mean": round(statistics.mean(latencies), 2) if latencies else None,
        },
        "results": results,
    }
    print("\nSummary:")
    print(json.dumps(summary, indent=2))
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bounded HTTP response-time sampler for localhost services only."
    )
    parser.add_argument("--url", required=True, help="Local URL, e.g. http://127.0.0.1:8000/")
    parser.add_argument("--duration", type=int, default=10, help="Duration in seconds (1-30; default: 10)")
    args = parser.parse_args()
    try:
        sample(args.url, args.duration)
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
