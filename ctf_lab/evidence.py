"""Read-only JWT structure, synthetic log correlation and LSB reconstruction."""
import base64
import binascii
import json


def inspect_jwt(token: str) -> dict:
    if len(token) > 16384:
        raise ValueError("token too large")
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("expected three JWT segments")
    def decode(segment):
        if any(c not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_" for c in segment):
            raise ValueError("invalid base64url")
        try:
            value = json.loads(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
        except (ValueError, UnicodeError, binascii.Error) as exc:
            raise ValueError("invalid JWT JSON") from exc
        if not isinstance(value, dict):
            raise ValueError("JWT claims and header must be objects")
        return value
    header, claims = decode(parts[0]), decode(parts[1])
    return {"algorithm": header.get("alg"), "has_kid": "kid" in header,
            "claim_names": sorted(claims), "signature_verified": False,
            "warning": "Decoding is not signature verification or authorization. No tokens are forged."}


def extract_lsb(samples: list[int], byte_count: int) -> bytes:
    """Extract MSB-first bytes from a supplied synthetic RGB-channel sample list."""
    if not 0 <= byte_count <= 4096 or len(samples) < byte_count * 8:
        raise ValueError("invalid byte count or truncated samples")
    if any(type(x) is not int or not 0 <= x <= 255 for x in samples):
        raise ValueError("samples must be channel bytes")
    return bytes(sum((samples[i * 8 + bit] & 1) << (7 - bit) for bit in range(8))
                 for i in range(byte_count))


def correlate(events: list[dict], adjacency: dict[str, list[str]]) -> dict:
    """Flag direct transitions absent from the supplied model, without declaring guilt."""
    from datetime import datetime
    parsed = []
    for i, event in enumerate(events):
        timestamp = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
        if timestamp.tzinfo is None:
            raise ValueError("timezone required")
        parsed.append((timestamp, i + 1, event))
    last, findings = {}, []
    for timestamp, row, event in sorted(parsed):
        subject, location = event["subject"], event["location"]
        if subject in last:
            prev_time, prev_location, prev_row = last[subject]
            if location != prev_location and location not in adjacency.get(prev_location, []):
                findings.append({"subject": subject, "from": prev_location, "to": location,
                                 "elapsed_seconds": (timestamp - prev_time).total_seconds(),
                                 "evidence_rows": [prev_row, row],
                                 "interpretation": "Transition outside supplied adjacency model; investigate missing events and map assumptions."})
        last[subject] = timestamp, location, row
    return {"status": "partial", "findings": findings, "trace_anchor": None,
            "final_flag_obtained": False, "scope": "Synthetic reproduction, not a completed original challenge"}
