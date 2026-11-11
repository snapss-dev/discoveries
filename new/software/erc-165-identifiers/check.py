"""Recompute ERC-165 identifiers and 4-byte selectors printed in ERC documents.

Reads cases.json from its own folder. Each case holds the function signatures as the document
declares them, the 4-byte value the document prints, and, where a cause was found, the changed
signature list that reproduces the printed value.

Keccak-256 is implemented here from the Keccak specification. If pycryptodome is installed, every
hash is also computed with it and the two must agree.

Run:  python check.py
"""
import json, os, sys

# ---------------------------------------------------------------- Keccak-256, from the specification
RC = []
_r = 1
for _ in range(24):
    _c = 0
    for _j in range(7):
        _bit = _r & 1
        _r = ((_r << 1) ^ ((_r >> 7) * 0x71)) & 0xFF
        if _bit:
            _c ^= 1 << ((1 << _j) - 1)
    RC.append(_c)
ROT = [[0] * 5 for _ in range(5)]
_x, _y = 1, 0
for _t in range(24):
    ROT[_x][_y] = ((_t + 1) * (_t + 2) // 2) % 64
    _x, _y = _y, (2 * _x + 3 * _y) % 5
M64 = (1 << 64) - 1

def _rol(v, n):
    return ((v << n) | (v >> (64 - n))) & M64 if n else v

def _permute(A):
    for rnd in range(24):
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x - 1) % 5] ^ _rol(C[(x + 1) % 5], 1) for x in range(5)]
        A = [[A[x][y] ^ D[x] for y in range(5)] for x in range(5)]
        B = [[0] * 5 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                B[y][(2 * x + 3 * y) % 5] = _rol(A[x][y], ROT[x][y])
        A = [[B[x][y] ^ ((~B[(x + 1) % 5][y]) & B[(x + 2) % 5][y]) for y in range(5)] for x in range(5)]
        A[0][0] ^= RC[rnd]
    return A

def keccak256_own(data):
    rate = 136
    p = bytearray(data)
    p.append(0x01)
    while len(p) % rate:
        p.append(0)
    p[-1] |= 0x80
    A = [[0] * 5 for _ in range(5)]
    for off in range(0, len(p), rate):
        for i in range(rate // 8):
            A[i % 5][i // 5] ^= int.from_bytes(p[off + 8 * i:off + 8 * i + 8], 'little')
        A = _permute(A)
    return b''.join(A[i % 5][i // 5].to_bytes(8, 'little') for i in range(4))

try:
    from Crypto.Hash import keccak as _lib
    def keccak256_lib(data):
        return _lib.new(digest_bits=256, data=data).digest()
    SECOND = 'pycryptodome'
except Exception:
    keccak256_lib = None
    SECOND = None

NHASH = 0
def selector(sig):
    global NHASH
    h = keccak256_own(sig.encode())
    if keccak256_lib is not None:
        assert h == keccak256_lib(sig.encode()), sig
    NHASH += 1
    return int.from_bytes(h[:4], 'big')

def ident(sigs):
    x = 0
    for s in sigs:
        x ^= selector(s)
    return '%08x' % x

def main():
    assert keccak256_own(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    here = os.path.dirname(os.path.abspath(__file__))
    data = json.load(open(os.path.join(here, 'cases.json'), encoding='utf-8'))
    print('second implementation:', SECOND or 'not installed (own implementation only)')
    print()
    print('Calibration: identifiers that the documents print and that do reproduce')
    for c in data['calibration']:
        got = ident(c['signatures'])
        print('  %-36s printed 0x%s  recomputed 0x%s  %s' % (c['what'], c['printed'], got, 'ok' if got == c['printed'] else 'DIFFERENT'))
        assert got == c['printed']
    print()
    bad = 0
    for g, title in (('A', 'Group A: Final and Last Call documents'),
                     ('B', 'Group B: other statuses, cause identified'),
                     ('C', 'Group C: other statuses, cause not determined')):
        print(title)
        for c in data['cases']:
            if c['group'] != g:
                continue
            got = ident(c['signatures'])
            assert got != c['printed'], 'case no longer differs: %r' % c['what']
            bad += 1
            print('  ERC-%d (%s), line %d: %s' % (c['erc'], c['status'], c['line'], c['what']))
            print('      printed 0x%s   from the %d declared signature(s) 0x%s' % (c['printed'], len(c['signatures']), got))
            if c['alt_signatures']:
                alt = ident(c['alt_signatures'])
                assert alt == c['printed'], c['what']
                print('      printed value is reproduced by: %s (0x%s)' % (c['alt_note'], alt))
            if c['note']:
                print('      note: %s' % c['note'])
        print()
    print('Group D: interface in the text against the reference interface in the assets folder (no identifier printed)')
    nd = 0
    for c in data['cases']:
        if c['group'] != 'D':
            continue
        a, b = ident(c['signatures']), ident(c['alt_signatures'])
        assert a != b, c['what']
        nd += 1
        only_text = [s for s in c['signatures'] if s not in c['alt_signatures']]
        only_asset = [s for s in c['alt_signatures'] if s not in c['signatures']]
        print('  ERC-%d (%s), line %d: %s' % (c['erc'], c['status'], c['line'], c['what']))
        print('      identifier from the text 0x%s   from the reference interface 0x%s' % (a, b))
        print('      only in the text: %s' % (', '.join('%s 0x%08x' % (s, selector(s)) for s in only_text) or 'nothing'))
        print('      only in the reference interface: %s' % (', '.join('%s 0x%08x' % (s, selector(s)) for s in only_asset) or 'nothing'))
        print('      note: %s' % c['note'])
    print()
    print('Group E: interface against the implementation printed in the same document')
    ne = 0
    for c in data['cases']:
        if c['group'] != 'E':
            continue
        a, b = c['signatures'][0], c['alt_signatures'][0]
        assert selector(a) != selector(b)
        ne += 1
        print('  ERC-%d (%s), line %d: interface %s 0x%08x, implementation %s 0x%08x' % (
            c['erc'], c['status'], c['line'], a, selector(a), b, selector(b)))
        if c['note']:
            print('      note: %s' % c['note'])
    print()
    print('%d printed values differ from the value recomputed from the declared signatures' % bad)
    print('%d interfaces differ between the text and the reference interface' % nd)
    print('%d functions differ between an interface and the implementation in the same document' % ne)
    print('%d signature hashes computed' % NHASH)

if __name__ == '__main__':
    main()
