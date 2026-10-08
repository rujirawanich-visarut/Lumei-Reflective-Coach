#!/usr/bin/env python3
"""
Air-Gapped Sandbox Pre-Flight Check for Lumei STAR-L Decoder.
Python Standard Library only. Exit 0 = Ready, Exit 3 = Sandbox Violation.
"""
import json
import socket
import sys

EGRESS_PROBE = ("1.1.1.1", 443)
REQUIRED_MODULES = ("json", "re", "os", "sys")


def egress_is_blocked(timeout_seconds: float = 1.5) -> bool:
    try:
        with socket.create_connection(EGRESS_PROBE, timeout=timeout_seconds):
            return False
    except OSError:
        return True


def check_missing_modules() -> list[str]:
    missing = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing


def main() -> int:
    findings = {
        "python_version": ".".join(map(str, sys.version_info[:3])),
        "egress_blocked": egress_is_blocked(),
        "missing_modules": check_missing_modules(),
    }
    ready = findings["egress_blocked"] and not findings["missing_modules"]
    findings["status"] = "READY" if ready else "SANDBOX_CONTRACT_VIOLATION"
    print(json.dumps(findings, indent=2))
    return 0 if ready else 3


if __name__ == "__main__":
    sys.exit(main())
