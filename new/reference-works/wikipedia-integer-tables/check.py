# Recomputes the four integer statements quoted in PAGE/README from the saved wikitext excerpts
# (wikitext_excerpts.json, each with the revision id it was taken from).
# Usage: python check.py        (about 20 seconds)
import os, re, json, math
import sympy
from flint import fmpz
HERE = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(HERE, 'wikitext_excerpts.json'), encoding='utf8'))

# ---------------------------------------------------------------- 1. prime quadruplets by number of digits
x = EX['quadruplet']; print('Prime quadruplet, revision', x['revid'])
printed = [int(u) for u in re.search(r':((?:\d+, )+\d+) \{\{OEIS\|id=A120120\}\}', x['wikitext']).group(1).split(', ')]
print('  printed counts for n = 2, 3, ... digits:', printed)
N = 10 ** 8
sieve = bytearray([1]) * (N + 10); sieve[0] = sieve[1] = 0
for i in range(2, int(N ** 0.5) + 1):
    if sieve[i]: sieve[i * i::i] = bytearray(len(range(i * i, N + 10, i)))
counts = {}
starts5 = []
p = 5
while p < N:
    if sieve[p] and sieve[p + 2] and sieve[p + 6] and sieve[p + 8]:
        d = len(str(p)); counts[d] = counts.get(d, 0) + 1
        if d == 5: starts5.append(p)
    p += 1 if p < 11 else 30 if p % 30 == 11 else 1
# (after 11, the first member of a quadruplet is 11 mod 30; the stepping above lands on 11 and then moves by 30)
method1 = [counts[d] for d in range(2, 9)]
print('  sieve to 10^8, counts for 2..8 digits:  ', method1)
# independent second count for 2..6 digits with a different primality test and no mod-30 shortcut
method2 = []
for d in range(2, 7):
    c = 0
    for q in range(10 ** (d - 1), 10 ** d):
        if q % 2 and fmpz(q).is_prime() and fmpz(q + 2).is_prime() and fmpz(q + 6).is_prime() and fmpz(q + 8).is_prime(): c += 1
    method2.append(c)
print('  direct test, counts for 2..6 digits:    ', method2)
assert method1[:5] == method2
print('  the 5-digit quadruplets start at:', starts5)
assert len(starts5) == 26 and printed[3] == 27
assert printed[:3] == method1[:3] and printed[4:7] == method1[4:7]
print('  RESULT: the fourth printed term is 27; the count of 5-digit prime quadruplets is 26. Other terms up to 8 digits agree.')

# ---------------------------------------------------------------- 2. perfect totient numbers 3p, p = 4*3^k + 1
x = EX['totient']; print('Perfect totient number, revision', x['revid'])
printed = [int(u) for u in re.search(r':((?:\d+, )+\d+), \.\.\.', x['wikitext']).group(1).split(', ')]
print('  printed exponents k:', printed)
ks = [k for k in range(0, 1700) if fmpz(4 * 3 ** k + 1).is_probable_prime()]
ks2 = [k for k in range(0, 1700) if sympy.isprime(4 * 3 ** k + 1)]
assert ks == ks2
print('  k < 1700 with 4*3^k+1 prime (two libraries):', ks)
missing = [k for k in ks if k <= max(printed) and k not in printed]
print('  missing from the printed list:', missing)
assert missing == [885] and [k for k in printed if k not in ks] == []
# primality proof for p = 4*3^885 + 1 (Pocklington / Lucas: p - 1 = 2^2 * 3^885 is fully factored)
k = 885; p = 4 * 3 ** k + 1
proof = None
for a in range(2, 200):
    if pow(a, p - 1, p) != 1: raise SystemExit('composite')
    if math.gcd(pow(a, (p - 1) // 2, p) - 1, p) == 1 and math.gcd(pow(a, (p - 1) // 3, p) - 1, p) == 1:
        proof = a; break
assert proof is not None
print('  4*3^885+1 (%d digits) is prime: Lucas test with base %d, a^(p-1) = 1 and gcd(a^((p-1)/q) - 1, p) = 1 for q = 2, 3' % (len(str(p)), proof))
# 3p is a perfect totient number: iterate phi on numbers of the form 2^a 3^b (p is prime, so phi(3p) = 2(p-1) = 2^3 * 3^885)
def phi23(a, b):          # phi(2^a 3^b) as exponents
    if a == 0 and b == 0: return None
    if b == 0: return (a - 1, 0)
    if a == 0: return (1, b - 1)
    return (a, b - 1)
total = 0; cur = (3, k)
while cur is not None:
    total += 2 ** cur[0] * 3 ** cur[1]
    if cur == (0, 0): break
    cur = phi23(*cur)
assert total == 3 * p
print('  sum of the iterated totients of 3p equals 3p: True, so 3*(4*3^885+1) is a perfect totient number')

# ---------------------------------------------------------------- 3. divisors of 1002
x = EX['n1002']; print('1002 (number), revision', x['revid'])
printed = [int(u) for u in re.search(r'divisor = ([\d, ]+)', x['wikitext']).group(1).split(', ')]
true = [d for d in range(1, 1003) if 1002 % d == 0]
assert true == sympy.divisors(1002)
print('  printed:', printed); print('  divisors:', true); print('  missing:', [d for d in true if d not in printed])
assert [d for d in true if d not in printed] == [3]

# ---------------------------------------------------------------- 4. happy primes
x = EX['happy']; print('List of prime numbers, revision', x['revid'], '(happy primes)')
txt = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', x['wikitext'])
printed = [int(u) for u in re.findall(r'\d+', txt[:txt.find('({{OEIS2C|A035497')].split('\n')[-1])]
def happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n); n = sum(int(c) ** 2 for c in str(n))
    return n == 1
true = [q for q in range(2, 1100) if sympy.isprime(q) and happy(q)]
tail = printed[printed.index(563):]
print('  printed tail:', tail); print('  happy primes from 563 to 1093:', [q for q in true if q >= 563])
dups = sorted(set(q for q in tail if tail.count(q) > 1))
print('  repeated entries:', dups)
assert dups == [1039] and sorted(set(tail)) == [q for q in true if q >= 563]
print('ALL CHECKS PASSED')
