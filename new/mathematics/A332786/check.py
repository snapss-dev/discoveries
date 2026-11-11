"""A332786: a(n) = numerator(-1/n + Sum_{k=1..n} 2^(k-1)/k).
For n = p^2 this computes the p-adic valuation of S(n) = -1/n + Sum_{k<=n} 2^(k-1)/k through
T = p^2 * S(n) modulo a power of p. If the valuation is at least 0 it is the valuation of a(n).
  Method A: numba, 64-bit arithmetic modulo p^4, in parallel blocks.
  Method B: gmpy2 big integers modulo p^5, sequential, with the terms grouped differently.
  Method X: exact fractions (small p only).
Run:  python check.py 7          (the known case 49: valuation 2)
      python check.py 16843      (about four minutes)
"""
import sys, time
import numpy as np
from numba import njit, prange
import gmpy2


@njit(cache=True)
def mulmod(a, b, m):
    # a, b < m < 2^57: Horner over 6-bit limbs of b, so every intermediate stays < 2^63
    r = 0
    for sh in range(54, -1, -6):
        limb = (b >> sh) & 63
        r = (r * 64) % m
        r = (r + a * limb) % m
    return r


@njit(cache=True)
def powmod(a, e, m):
    r = 1; a %= m
    while e:
        if e & 1:
            r = mulmod(r, a, m)
        a = mulmod(a, a, m); e >>= 1
    return r


@njit(cache=True)
def inv(a, m):
    t, newt, r, newr = 0, 1, m, a % m
    while newr:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    return t % m


@njit(parallel=True, cache=True)
def method_a(p):
    M = p * p * p * p
    n = p * p
    nb = 4096
    blk = (n + nb - 1) // nb
    parts = np.zeros(nb, dtype=np.int64)
    p2 = p * p
    for b in prange(nb):
        lo = 1 + b * blk
        hi = min(n, (b + 1) * blk)
        if lo > hi:
            continue
        acc = 0
        pw = powmod(2, lo - 1, M)  # 2^(k-1)
        for k in range(lo, hi + 1):
            if k % p != 0:
                acc = (acc + mulmod(mulmod(p2, pw, M), inv(k, M), M)) % M
            elif k != n:
                j = k // p
                acc = (acc + mulmod(mulmod(p, pw, M), inv(j, M), M)) % M
            else:
                acc = (acc + pw) % M
            pw = (pw * 2) % M
        parts[b] = acc
    tot = 0
    for b in range(nb):
        tot = (tot + parts[b]) % M
    return (tot - 1) % M  # the -1/n term times p^2


def method_b(p):
    E = 5
    M = gmpy2.mpz(p) ** E
    n = p * p
    p2 = gmpy2.mpz(p) ** 2
    # group k = p*q + r, r = 1..p-1 (unit part), and k = p*j (j=1..p)
    acc = gmpy2.mpz(0)
    two_p = gmpy2.powmod(2, p, M)
    for r in range(1, p):
        # sum over q=0..p-1 of 2^(p q + r - 1) / (p q + r)
        s = gmpy2.mpz(0)
        t = gmpy2.powmod(2, r - 1, M)
        for q in range(p):
            s += t * gmpy2.invert(p * q + r, M)
            t = t * two_p % M
        acc = (acc + p2 * (s % M)) % M
    two_pp = gmpy2.powmod(2, p, M)
    t = gmpy2.powmod(2, p - 1, M)  # 2^(p*j - 1) for j=1
    for j in range(1, p):
        acc = (acc + p * t * gmpy2.invert(j, M)) % M
        t = t * two_pp % M
    acc = (acc + gmpy2.powmod(2, n - 1, M) - 1) % M
    return int(acc), E


def method_x(p):
    from fractions import Fraction
    n = p * p
    s = Fraction(-1, n) + sum(Fraction(2 ** (k - 1), k) for k in range(1, n + 1))
    v = 0; num = s.numerator
    while num % p == 0:
        num //= p; v += 1
    return v


def vp(x, p, cap):
    v = 0
    while x % p == 0 and v < cap:
        x //= p; v += 1
    return v


if __name__ == '__main__':
    p = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else 'all'
    print('p =', p, ' n = p^2 =', p * p)
    if mode in ('X', 'all') and p < 40:
        print('X exact: v_p(a(p^2)) =', method_x(p))
    if mode in ('A', 'all'):
        t = time.time(); T = method_a(p)
        print('A numba: T = p^2*S mod p^4 =', T, ' => v_p(S) =', (vp(T, p, 4) - 2) if T else '>= 2', '[%.1f s]' % (time.time() - t), flush=True)
    if mode in ('B', 'all'):
        t = time.time(); T, E = method_b(p)
        print('B gmpy2: T = p^2*S mod p^%d =' % E, T, ' => v_p(S) =', (vp(T, p, E) - 2) if T else '>= %d' % (E - 2), '[%.1f s]' % (time.time() - t))
