
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import random
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional


def env_info() -> Dict[str, Any]:
    """Collect basic environment information."""
    return {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "cwd": os.getcwd(),
        "time": datetime.now().isoformat(timespec="seconds"),
    }


def fib(n: int) -> List[int]:
    """Return the first n Fibonacci numbers (starting at 0)."""
    seq: List[int] = []
    a, b = 0, 1
    for _ in range(max(0, n)):
        seq.append(a)
        a, b = b, a + b
    return seq


def is_prime(n: int) -> bool:
    """Basic primality test (sufficient for small numbers)."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def random_payload(seed: Optional[int] = None) -> Dict[str, Any]:
    """Generate a small random payload and a short checksum.

    If seed is provided, output becomes deterministic.
    """
    rng = random.Random(seed)
    data: Dict[str, Any] = {
        "int": rng.randint(1, 100),
        "float": round(rng.random(), 6),
        "choice": rng.choice(["apple", "banana", "cherry", "durian"]),
    }
    raw = json.dumps(data, sort_keys=True).encode("utf-8")
    data["sha256"] = hashlib.sha256(raw).hexdigest()[:16]
    return data


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Tiny script to test GitHub commits and CI."
    )
    parser.add_argument("--name", default="World", help="Name to greet")
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed for deterministic output"
    )
    parser.add_argument(
        "--count", type=int, default=10, help="Length of Fibonacci sequence"
    )
    args = parser.parse_args(argv)

    print("=" * 64)
    print(f"GitHub test run at {datetime.now().isoformat(timespec='seconds')}")
    print("=" * 64)

    info = env_info()
    print(f"Hello, {args.name} 👋")
    print(f"- Python:   {info['python']}")
    print(f"- Platform: {info['platform']}")
    print(f"- CWD:      {info['cwd']}")

    payload = random_payload(args.seed)
    print("\nRandom payload:")
    print(json.dumps(payload, indent=2))

    seq = fib(args.count)
    ssum = sum(seq)
    primes = [n for n in seq if is_prime(n)]
    print(f"\nFibonacci({args.count}) = {seq}")
    print(f"Sum = {ssum} | Primes in sequence = {primes}")

    print("\nDone. Commit this change to test your GitHub setup.")
    return 0


if __name__ == "__main__":

    raise SystemExit(main(sys.argv[1:]))
