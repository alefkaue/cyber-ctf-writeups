"""Bounded textbook RSA demonstration, not a production cryptography library."""
from math import gcd, isqrt


def recover_small_rsa(n: int, e: int, ciphertext: int) -> dict:
    if not 4 <= n <= 10**12:
        raise ValueError("Only tiny educational moduli (4 <= n <= 10**12) are accepted")
    if not 1 < e < n or not 0 <= ciphertext < n:
        raise ValueError("invalid public exponent or ciphertext")
    p = next((x for x in range(2, isqrt(n) + 1) if n % x == 0), None)
    if p is None:
        raise ValueError("modulus is prime")
    q = n // p
    prime = lambda x: x >= 2 and all(x % y for y in range(2, isqrt(x) + 1))
    if p == q or not prime(q):
        raise ValueError("demonstration requires two distinct primes")
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        raise ValueError("public exponent is not invertible")
    d = pow(e, -1, phi)
    m = pow(ciphertext, d, n)
    message = m.to_bytes(max(1, (m.bit_length() + 7) // 8), "big")
    return {"n_bits": n.bit_length(), "p": p, "q": q, "plaintext_hex": message.hex(),
            "plaintext": message.decode("utf-8", errors="replace"),
            "scope": "Synthetic tiny RSA; not the original CTF modulus or flag"}


def demo() -> dict:
    p, q, e = 1009, 1013, 65537
    message = int.from_bytes(b"ok", "big")
    return recover_small_rsa(p * q, e, pow(message, e, p * q))
