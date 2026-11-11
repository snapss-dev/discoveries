"""A229324: composite squarefree n with (p + tau(n)) | (n - phi(n)) for every prime p | n.
Run:  python check.py
"""
from sympy import factorint

def is_term(n):
    f = factorint(n)
    if len(f) < 2 or any(e > 1 for e in f.values()): return False
    tau = 2 ** len(f); phi = 1
    for p in f: phi *= p - 1
    return all((n - phi) % (p + tau) == 0 for p in f)

for n in (10419754, 188371849):
    f = factorint(n); phi = 1
    for p in f: phi *= p - 1
    print(f"{n} = {' * '.join(map(str, f))}: term {is_term(n)}, n mod 5 = {n % 5}, "
          f"n - phi(n) = {n - phi}, divisors required: {[p + 2 ** len(f) for p in f]}")
terms = [n for n in range(2, 200001) if is_term(n)]
print("first terms:", terms[:8], "(entry: 115, 205, 295, 565, 655, 745, 835, 1195)")
print(f"terms below 200000: {len(terms)}; all multiples of 5: {all(t % 5 == 0 for t in terms)}")
