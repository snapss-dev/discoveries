# v_p of a(p) (A332786) and b(p) (A330718) for a prime p: T = p*S(p) = sum_{k<p} p 2^(k-1)/k + 2^(p-1) - 1, modulo p^6
import sys
for p in (5, 7, 11, 13, 16843, 2124679):
    M = p**6
    s = h = 0; t = 1
    for k in range(1, p):
        u = pow(k, -1, M)
        s = (s + p*t*u) % M; h = (h + p*u) % M
        t = t*2 % M
    s = (s + t - 1) % M      # k = p term: 2^(p-1)/p * p, and -1/p * p
    hb = (s - h) % M         # A330718: subtract p*H(p-1)
    def v(x):
        if x == 0: return 99
        n = 0
        while x % p == 0: x //= p; n += 1
        return n
    print(p, "v_p(a(p)) =", v(s)-1, "  v_p(b(p)) =", v(hb)-1, flush=True)
