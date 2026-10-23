from argparse import ArgumentParser
from pathlib import Path
import json
import sys
from .rsa_demo import demo
from .evidence import correlate, inspect_jwt, extract_lsb


def main(argv=None):
    parser = ArgumentParser(description="Offline synthetic reconstructions of CTF learning outcomes")
    parser.add_argument("demo", choices=["rsa", "forensics", "jwt", "lsb"])
    args = parser.parse_args(argv)
    if args.demo == "rsa":
        result = demo()
    elif args.demo == "forensics":
        result = correlate([
            {"timestamp": "2026-01-01T10:00:00Z", "subject": "analyst-a", "location": "entry"},
            {"timestamp": "2026-01-01T10:00:03Z", "subject": "analyst-a", "location": "vault"}],
            {"entry": ["hall"], "hall": ["entry", "vault"], "vault": ["hall"]})
    elif args.demo == "jwt":
        import base64
        enc = lambda data: base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
        result = inspect_jwt(enc({"alg": "RS256", "kid": "synthetic"}) + "." +
                             enc({"role": "reader"}) + ".ZGVtbw")
    else:
        payload = b"SYNTHETIC"
        samples = [128 | ((b >> shift) & 1) for b in payload for shift in range(7, -1, -1)]
        result = {"payload": extract_lsb(samples, len(payload)).decode(),
                  "scope": "Synthetic channel samples; no original camera frames or key"}
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
