"""A337385: odd k with sigma(A003961(k)) >= 2*A003961(k), A003961 = shift every prime to the next prime.
Run:  python check.py
"""
from sympy import factorint, nextprime, divisor_sigma

def A003961(n):
    r = 1
    for p, e in factorint(n).items(): r *= int(nextprime(p)) ** e
    return r

k = 8562829275
m = A003961(k); s = int(divisor_sigma(m))
print("k =", k, "=", factorint(k), "| odd:", k % 2 == 1)
print("A003961(k) =", m, "| sigma =", s, "| 2*A003961(k) =", 2 * m, "| term:", s >= 2 * m)
print("17 divides k:", k % 17 == 0, "| 255255 divides k:", k % 255255 == 0)
