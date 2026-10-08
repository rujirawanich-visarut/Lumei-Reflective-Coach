#!/usr/bin/env python3
"""
Pre-flight check for the Code Interpreter Sandbox environment.
Ensures air-gapped isolation and required Python stdlib modules.
Exit 0 = Ready, Exit 3 = Violation.
"""
import sys
import json
import socket

EGRESS_PROBE = ("1.1.1.1", 443)
REQUIRED_MODULES = ("json", "re", "sys", "os")

def is_egress_blocked() -> bool:
    try:
        with socket.create_connection(EGRESS_PROBE, timeout=1.5):
            return False
    except OSError:
        return True

def check_modules() -> list:
    missing = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    return missing

def main() -> int:
    blocked = is_egress_blocked()
    missing = check_modules()
    ready = blocked and not missing
    payload = {
        "status": "READY" if ready else "SANDBOX_VIOLATION",
        "egress_blocked": blocked,
        "missing_modules": missing,
        "python_version": ".".join(map(str, sys.version_info[:3]))
    }
    print(json.dumps(payload))
    return 0 if ready else 3

if __name__ == "__main__":
    sys.exit(main())
