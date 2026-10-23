import base64
import json
import unittest
from ctf_lab.rsa_demo import demo, recover_small_rsa
from ctf_lab.evidence import correlate, inspect_jwt, extract_lsb
from ctf_lab.__main__ import main

class LabTests(unittest.TestCase):
    def test_tiny_rsa_recovers_known_plaintext(self):
        self.assertEqual(demo()["plaintext"], "ok")

    def test_rsa_rejects_large_invalid_and_prime_moduli(self):
        for n, e, c in [(10**13, 3, 0), (17, 3, 0), (49, 5, 1), (15, 3, 20), (8, 3, 1)]:
            with self.subTest(n=n), self.assertRaises(ValueError):
                recover_small_rsa(n, e, c)

    def test_reconstruction_remains_partial(self):
        result = correlate([
            {"timestamp": "2026-01-01T10:00:03Z", "subject": "a", "location": "vault"},
            {"timestamp": "2026-01-01T10:00:00Z", "subject": "a", "location": "entry"}], {"entry": ["hall"]})
        self.assertFalse(result["final_flag_obtained"])
        self.assertIsNone(result["trace_anchor"])
        self.assertEqual(result["findings"][0]["evidence_rows"], [2, 1])

    def test_legal_movement_is_not_flagged(self):
        self.assertFalse(correlate([
            {"timestamp": "2026-01-01T10:00:00Z", "subject": "a", "location": "entry"},
            {"timestamp": "2026-01-01T10:00:03Z", "subject": "a", "location": "hall"}], {"entry": ["hall"]})["findings"])

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            correlate([{"timestamp": "2026-01-01T10:00:00", "subject": "a", "location": "entry"}], {})

    def test_decode_never_claims_verified_signature(self):
        enc = lambda x: base64.urlsafe_b64encode(json.dumps(x).encode()).decode().rstrip("=")
        result = inspect_jwt(enc({"alg": "RS256"}) + "." + enc({"sub": "fictional"}) + ".Zg")
        self.assertFalse(result["signature_verified"])
        self.assertNotIn("fictional", json.dumps(result))

    def test_jwt_rejects_malformed_nonobjects_and_oversized(self):
        for token in ("a.b", "!.e30.sig", "W10.e30.sig", "x" * 20000):
            with self.assertRaises(ValueError):
                inspect_jwt(token)

    def test_lsb_byte_order(self):
        samples = [200 | ((value >> shift) & 1) for value in b"demo" for shift in range(7, -1, -1)]
        self.assertEqual(extract_lsb(samples, 4), b"demo")

    def test_lsb_truncation_and_invalid_channel(self):
        for samples, size in [([0], 1), ([256] * 8, 1), ([1] * 8, -1)]:
            with self.assertRaises(ValueError):
                extract_lsb(samples, size)

    def test_all_cli_demos(self):
        from unittest.mock import patch
        for name in ("rsa", "forensics", "jwt", "lsb"):
            with patch("builtins.print"):
                self.assertEqual(main([name]), 0)

if __name__ == "__main__":
    unittest.main()
