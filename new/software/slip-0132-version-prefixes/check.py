"""SLIP-0132: does each printed prefix follow from the printed version bytes?

A BIP-32 extended key is 78 bytes (4 version bytes, then depth, fingerprint, child number, chain
code and key) followed by a 4-byte checksum, written in Base58. The first four characters of the
text depend only on the version bytes when the smallest and the largest possible 82-byte values with
those version bytes start with the same four characters. This script computes both for every row of
the table (rows.json, extracted from slip-0132.md) and compares with the printed prefix.

Base58 is implemented twice: by repeated division of one big integer, and by the digit-array method.

Run:  python check.py
"""
import json, os

B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def b58_bigint(raw):
    n = int.from_bytes(raw, 'big')
    s = ''
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    return '1' * (len(raw) - len(raw.lstrip(b'\0'))) + s

def b58_digits(raw):
    digits = [0]
    for byte in raw:
        carry = byte
        for i in range(len(digits)):
            carry += digits[i] << 8
            digits[i] = carry % 58
            carry //= 58
        while carry:
            digits.append(carry % 58)
            carry //= 58
    zeros = len(raw) - len(raw.lstrip(b'\0'))
    body = ''.join(B58[d] for d in reversed(digits)).lstrip('1') if any(digits) else ''
    return '1' * zeros + body

def prefix_range(version_hex):
    v = bytes.fromhex(version_hex)
    lo, hi = v + b'\x00' * 78, v + b'\xff' * 78     # 74 payload bytes + 4 checksum bytes, any value
    a, b = b58_bigint(lo), b58_bigint(hi)
    assert a == b58_digits(lo) and b == b58_digits(hi)
    assert len(a) == len(b)
    return a[:4], b[:4]

def main():
    # calibration: Bitcoin's own values from BIP-32
    assert prefix_range('0488b21e') == ('xpub', 'xpub')
    assert prefix_range('0488ade4') == ('xprv', 'xprv')
    assert prefix_range('043587cf') == ('tpub', 'tpub')
    here = os.path.dirname(os.path.abspath(__file__))
    rows = json.load(open(os.path.join(here, 'rows.json'), encoding='utf-8'))
    cells = bad = 0
    for r in rows:
        for kind in ('pub', 'prv'):
            ver, printed = r[kind + '_version'], r[kind + '_prefix']
            lo, hi = prefix_range(ver)
            cells += 1
            ok = lo == hi == printed
            if not ok:
                bad += 1
                print('line %d  %-16s 0x%s  printed %s  the version bytes give %s' % (
                    r['line'], r['coin'], ver, printed, lo if lo == hi else lo + ' to ' + hi))
    print('%d rows, %d cells checked, %d cells where the printed prefix does not follow from the version bytes' % (len(rows), cells, bad))
    assert (len(rows), cells, bad) == (34, 68, 6)

if __name__ == '__main__':
    main()
