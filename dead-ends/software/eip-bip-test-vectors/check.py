"""Recompute three families of worked examples from core EIPs. All of them reproduce.

1. EIP-1014: the seven CREATE2 examples (address, salt, init code, resulting address).
2. EIP-2124 and EIP-6122: fork hashes, CRC32 of the genesis hash followed by the fork points.
3. EIP-7607 (Fusaka): activation epoch, timestamp, UTC time and fork id of each network.

The values printed in the EIPs are in vectors.json. The chain configurations below (genesis hashes,
genesis times, earlier fork points) are public constants that the EIPs do not print; if one of them
were wrong here, the corresponding rows would fail.

Keccak-256 and CRC32 are implemented here from their specifications; CRC32 is also compared with
zlib, and Keccak-256 with pycryptodome if that is installed.

Run:  python check.py
"""
import json, os, struct, zlib, datetime

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

def crc32(data):
    c = 0xffffffff
    for b in data:
        c ^= b
        for _ in range(8):
            c = (c >> 1) ^ (0xEDB88320 if c & 1 else 0)
    c ^= 0xffffffff
    assert c == zlib.crc32(data)
    return c

def checksum_address(a):
    a = a.lower().replace('0x', '')
    h = keccak256(a.encode()).hex()
    return '0x' + ''.join(ch.upper() if int(h[i], 16) >= 8 else ch for i, ch in enumerate(a))

GENESIS = {
    'mainnet': 'd4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3',
    'ropsten': '41941023680923e0fe4d74a34bdac8141f2540e3ae90623718e47d66d1ca4a2d',
    'rinkeby': '6341fd3daf94b748c72ced5a5b26028f2474f5f00d824504e4fa37a75767e177',
    'goerli': 'bf7e331f7f7c1dd2e05159666b3bf8bc7a8a3a9eb1d518969eab529dd9b88c1a',
}
# for EIP-7607: genesis hash, beacon genesis time, fork blocks, fork timestamps up to Prague
NET = {
    'Mainnet': ('d4e56740f876aef8c010b86a40d5f56745a118d0906a34e69aec8c0db1cb8fa3', 1606824023,
                [1150000, 1920000, 2463000, 2675000, 4370000, 7280000, 9069000, 9200000, 12244000, 12965000, 13773000, 15050000],
                [1681338455, 1710338135, 1746612311]),
    'Sepolia': ('25a5cc106eea7138acab33231d7160d69cb777ee0c2c553fcddf5138993e6dd9', 1655733600,
                [1735371], [1677557088, 1706655072, 1741159776]),
    'Holesky': ('b5f7f912443c940f21fd611f12828d75b534364ed9e95ca4e307729a4661bde4', 1695902400,
                [], [1696000704, 1707305664, 1740434112]),
    'Hoodi': ('bbe312868b376a3001692a646dd2d7d1e4406380dfd86b98aa8a34d1557c971b', 1742213400,
              [], [1742999832]),
}

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    v = json.load(open(os.path.join(here, 'vectors.json')))
    print('second Keccak implementation:', SECOND or 'not installed (own implementation only)')
    n = bad = 0

    for e in v['eip1014']:
        got = keccak256(b'\xff' + bytes.fromhex(e['address'][2:]) + bytes.fromhex(e['salt'][2:])
                        + keccak256(bytes.fromhex(e['init_code'][2:])))[12:].hex()
        for ok in (got == e['result'][2:].lower(), checksum_address(got) == e['result']):
            n += 1; bad += not ok
    print('EIP-1014: %d CREATE2 examples, address and mixed-case form' % len(v['eip1014']))

    for net, lst in v['eip2124'].items():
        data = bytes.fromhex(GENESIS[net])
        for block, printed in lst:
            if block:
                data += struct.pack('>Q', block)
            n += 1; bad += ('%08x' % crc32(data)) != printed
    data = bytes.fromhex(GENESIS['mainnet'])
    for b in (1150000, 1920000, 2463000, 2675000, 4370000, 7280000):
        data += struct.pack('>Q', b)
    for point, printed in v['eip6122']:
        data += struct.pack('>Q', point)
        n += 1; bad += ('%08x' % crc32(data)) != printed
    n += 1
    bad += ('%08x' % crc32(bytes.fromhex(GENESIS['mainnet']) + struct.pack('>QQ', 1150000, 1668000000))) != 'cb37b2ee'
    print('EIP-2124 and EIP-6122: fork hashes of four networks and the timestamp examples')

    seen = {}
    for r in v['eip7607']:
        gen, t0, blocks, times = NET[r['network']]
        seen.setdefault(r['network'], []).append(r['timestamp'])
        data = bytes.fromhex(gen)
        for p in blocks + times + seen[r['network']]:
            data += struct.pack('>Q', p)
        checks = (
            t0 + r['epoch'] * 32 * 12 == r['timestamp'],
            datetime.datetime.fromtimestamp(r['timestamp'], datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S') == r['utc'],
            '%08x' % crc32(data) == r['fork_id'],
        )
        for ok in checks:
            n += 1; bad += not ok
    print('EIP-7607: %d rows, epoch to timestamp, timestamp to UTC time, fork id' % len(v['eip7607']))
    print('%d values recomputed, %d differ from the printed value' % (n, bad))
    assert bad == 0

if __name__ == '__main__':
    main()
