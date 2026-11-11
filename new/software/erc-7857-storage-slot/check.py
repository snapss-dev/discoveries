"""ERC-7857: the storage constant in the reference contract is not the ERC-7201 slot of its namespace.

ERC-7201 defines erc7201(id) = keccak256(abi.encode(uint256(keccak256(id)) - 1)) & ~bytes32(uint256(0xff)).
Keccak-256 is implemented here from the Keccak specification; if pycryptodome is installed every
hash is also computed with it and the two must agree.

Run:  python check.py
"""

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
    SECOND = 'pycryptodome'
except Exception:
    _lib = None
    SECOND = None

def keccak256(data):
    h = keccak256_own(data)
    if _lib is not None:
        assert h == _lib.new(digest_bits=256, data=data).digest()
    return h

def erc7201(namespace):
    inner = int.from_bytes(keccak256(namespace.encode()), 'big') - 1
    outer = int.from_bytes(keccak256(inner.to_bytes(32, 'big')), 'big')   # abi.encode(uint256) is 32 bytes, big-endian
    return '0x%064x' % (outer & ~0xff)

# Calibration: constants printed in ERC-7201 itself and in OpenZeppelin Contracts (upgradeable) 5.x
CALIBRATION = [
    ('example.main', '0x183a6125c38840424c4a85fa12bab2ab606c4b6d0e7cc73c0c06ba5300eab500', 'ERC-7201, example'),
    ('openzeppelin.storage.ERC20', '0x52c63247e1f47db19d5ce0460030c497f067ca4cebf71ba98eeadabe20bace00', 'OpenZeppelin ERC20Upgradeable'),
    ('openzeppelin.storage.Initializable', '0xf0c57e16840df040f15088dc2f81fe391c3923bec73e23a9662efc9c229c6a00', 'OpenZeppelin Initializable'),
    ('openzeppelin.storage.Ownable', '0x9016d09d72d40fdae2fd8ceac6b6234c7706214fd39c1cd1e609a0528c199300', 'OpenZeppelin OwnableUpgradeable'),
    ('openzeppelin.storage.AccessControl', '0x02dd7bc7dec4dceedda775e58dd541e08a116c6c53815c0bd028192f7b626800', 'OpenZeppelin AccessControlUpgradeable'),
]

# The claim under test: ERCS/erc-7857.md, lines 653 and 673 to 675
ERC_NAMESPACE = 'agent.storage.AgentNFT'
ERC_PRINTED = '0x4aa80aaafbe0e5fe3fe1aa97f3c1f8c65d61f96ef1aab2b448154f4e07594600'

# Context: every constant of this form in the public repository 0glabs/0g-agent-nft, which holds the
# same contract (commit b86e108a49bf3601bf57f1f0b3166dce2cb15928, files under contracts/)
UPSTREAM = [
    ('AgentNFT.sol', 'agent.storage.AgentNFT', '0x4aa80aaafbe0e5fe3fe1aa97f3c1f8c65d61f96ef1aab2b448154f4e07594600'),
    ('AgentMarket.sol', 'agent.storage.AgentMarket', '0xdf1beedbd3d3bce86b126f6986f1edd5f2fcd885f76d774cda1ccb33ea72b400'),
    ('TeeVerifier.sol', '0g.storage.TEEVerifier', '0x51af5f1073ffa8c7a0dc3cb06ba2dbe8e5167b3efac5cd47b999a7ce04613400'),
    ('verifiers/Verifier.sol', '0g.storage.Verifier', '0xbecdd708b48a40f3aa8e2248844b430477e64ef60f94c9d0bf26b790ba82a300'),
    ('ERC7857Upgradeable.sol', '0g.storage.ERC7857', '0xa2b40c657abdbf180a6038c081d3a0af6206dcea36f4558f991bf8c787ef3c00'),
    ('extensions/ERC7857AuthorizeUpgradeable.sol', '0g.storage.ERC7857Authorize', '0xf386e9faca35fbde2fe950510f665060c1dd15a136a76c268b6e6459b9945700'),
    ('extensions/ERC7857CloneableUpgradeable.sol', '0g.storage.ERC7857Cloneable', '0x03de6cf14ecf4575e0ed0cc2fdb9b7ee13500cb3c0c403254fc893bf6e0c8000'),
    ('extensions/ERC7857IDataStorageUpgradeable.sol', '0g.storage.ERC7857IDataStorage', '0xcee27158032fdbe7e1246476ff878669b520bc82ee1a949d22135b88cc5f5b00'),
]

def main():
    assert keccak256(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    print('second implementation:', SECOND or 'not installed (own implementation only)')
    print()
    print('Calibration')
    for ns, want, src in CALIBRATION:
        got = erc7201(ns)
        print('  %-36s %s  %s  (%s)' % (ns, got, 'ok' if got == want else 'DIFFERENT', src))
        assert got == want
    print()
    got = erc7201(ERC_NAMESPACE)
    print('ERC-7857 reference contract, namespace "%s"' % ERC_NAMESPACE)
    print('  printed constant        ', ERC_PRINTED)
    print('  erc7201 of the namespace', got)
    assert got != ERC_PRINTED
    assert got == '0xaef0528c8e96d44c4fb121fd648f9a91b53cb890a08fb8040090fcd3cc553200'
    # other simple readings of the comment that also do not give the printed constant
    h = int.from_bytes(keccak256(ERC_NAMESPACE.encode()), 'big')
    others = {
        'keccak256(id)': '0x%064x' % h,
        'keccak256(id) - 1': '0x%064x' % (h - 1),
        '(keccak256(id) - 1) & ~0xff': '0x%064x' % ((h - 1) & ~0xff),
        'keccak256(abi.encode(keccak256(id))) & ~0xff': '0x%064x' % (int.from_bytes(keccak256(h.to_bytes(32, 'big')), 'big') & ~0xff),
        'keccak256(abi.encode(keccak256(id) - 1)), unmasked': '0x%064x' % int.from_bytes(keccak256((h - 1).to_bytes(32, 'big')), 'big'),
    }
    for k, v in others.items():
        print('  %-52s %s' % (k, 'equals the printed constant' if v == ERC_PRINTED else 'differs'))
        assert v != ERC_PRINTED
    print('  result: the printed constant is not the ERC-7201 slot of the namespace in the comment and annotation')
    print()
    print('Context: the same pattern in the repository 0glabs/0g-agent-nft')
    n_ok = 0
    for f, ns, printed in UPSTREAM:
        got = erc7201(ns)
        ok = got == printed
        n_ok += ok
        print('  %-46s %-30s %s' % (f, ns, 'matches' if ok else 'differs, formula gives ' + got))
    print('  %d of %d constants match their comment' % (n_ok, len(UPSTREAM)))
    assert n_ok == 4

if __name__ == '__main__':
    main()
