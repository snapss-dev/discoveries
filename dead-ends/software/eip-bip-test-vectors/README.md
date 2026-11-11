# Worked examples in core EIPs and in BIPs: about 1,050 recomputed, none wrong

Status: **dead end** (nothing found). This is not an audit. Produced with AI assistance; see the
repository README.

## The idea

Specifications print worked examples that implementers test against: hashes, derived addresses,
checksums, fork identifiers, activation times. A wrong example costs everyone who trusts it, and it
can be found by recomputing. The same sweep found errors in application-level documents (see the
pages on ERC-165 identifiers, on the ERC-7857 storage constant and on SLIP-0132). In the core
protocol documents listed here it found none.

## What was recomputed, and the outcome

Repositories as of 10 November 2026: `ethereum/EIPs` at `bd93d240b727`, `ethereum/ERCs` at
`6504eb9dbd3f`, `bitcoin/bips` at `b34d9f751791`.

| document | what | values | outcome |
|---|---|---|---|
| EIP-1014 | the seven CREATE2 examples: address, and its mixed-case form | 14 | all reproduce |
| EIP-2124 | fork hashes (CRC32) in the test lists for Mainnet, Ropsten, Rinkeby, Görli | 23 | all reproduce |
| EIP-6122 | timestamp-based fork hashes in the example and in the Mainnet test list | 9 | all reproduce |
| EIP-7607 (Fusaka) | 12 table rows: epoch to timestamp, timestamp to UTC time, fork id | 36 | all reproduce |
| EIP-7600, EIP-7569, EIP-7773, EIP-6953 | activation epoch to timestamp (and UTC time in EIP-7773) | 13 | all reproduce |
| ERC-55, ERC-1191 | mixed-case checksum test addresses, including the chain-id variants | 39 | all reproduce |
| ERC and EIP texts and assets | `keccak256("...")` written next to a 32-byte constant: plain, minus one (ERC-1967 style), and the ERC-7201 formula | 51 | 50 reproduce; the other is ERC-7857, on its own page |
| ERC and EIP texts | 32-byte values that are the hash of an event or function signature in the same document | 40 | all reproduce |
| ERC-137, ERC-777, ERC-1967, ERC-6551, ERC-7201, ERC-7955, ERC-8074, ERC-8444, EIP-6110, EIP-7784 | name hashes, interface-name hashes, a storage slot, an example bytecode, two derived addresses, type and kind hashes | 16 | all reproduce |
| BIP-32 | extended public and private keys of test vectors 1 to 4 | 34 | all reproduce |
| BIP-85 | derived entropy, and the mnemonic, WIF, XPRV and password outputs | 19 | all reproduce, two after reading the text closely (below) |
| all BIP texts and vector files | Base58Check strings that look like addresses or keys | 607 | 567 valid; 40 explained below |
| all BIP texts and vector files | segwit address strings: checksum, and bech32 or bech32m as the witness version requires | 146 | 125 valid; 21 explained below |
| all BIP texts and vector files | output descriptor checksums (BIP-380) | 8 | 6 valid; 2 are listed by BIP-380 as invalid examples |

The strings that do not validate, and why none counts as an error:

- Base58Check: 22 occurrences of the example address `175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W` in BIP-21
  and BIP-321 (BIP-321 says its example addresses "are intentionally invalid to prevent accidental
  transactions"); 1 extended key that BIP-32 lists as "invalid checksum"; 15 fragments of hex or
  Base64 data that only resemble a key; and 2 occurrences of `1Hd44nkJfNAcPJeZyrGC5sKJS1TzgmCTjjZ`
  in BIP-15, an illustration in a Deferred 2011 document, which has 35 characters and no valid
  checksum.
- Segwit: 8 in BIP-321 (intentionally invalid, as above); 10 in the lists of invalid addresses of
  BIP-173 and BIP-350; 3 in BIP-173's list of valid addresses with witness version 1 or higher,
  an encoding that BIP-350 later replaced.

Two remarks on BIP-85 that are not errors in the values: the XPRV test vector prints, under the
label "DERIVED ENTROPY", bytes 32 to 63 of the 64-byte result (the part used as the private key),
where the other vectors print the leading bytes; and one test block labels a derivation path as
"MASTER BIP32 ROOT KEY".

One slip outside the specifications proper: the empirical analysis attached to EIP-7976
(`assets/eip-7976/eip7976_empirical_analysis.md`) labels selectors with function names, and three
of the seven fully written signatures do not hash to the selector beside them (`0x5e10b3f0`,
`0x415e2848`, `0x13d79a0b`). The table is supporting material and does not affect the EIP.

## How to check

    python check.py

`check.py` recomputes the EIP-1014, EIP-2124, EIP-6122 and EIP-7607 rows (82 values) from
`vectors.json`, with Keccak-256 and CRC32 written from their specifications and compared with
pycryptodome and zlib. The other rows were recomputed with scripts that read the repositories
directly and are not included here; they used secp256k1 from two libraries (coincurve and ecdsa),
HMAC-SHA512 from the standard library, and Base58, bech32 and descriptor-checksum routines written
from the BIP texts.

## Why this is weak evidence

- These are the examples that everyone tests against, so finding none wrong is the expected result.
- Only examples that a pattern could extract, or that were picked by hand, were recomputed. Not
  covered: BIP-340, BIP-341, BIP-327 and PSBT vector files, EIP-712 signing examples, EIP-155 and
  typed-transaction examples, precompile input and output examples, gas-cost arithmetic in prose,
  RLP and SSZ examples, and all IETF RFCs.
- The chain constants used for fork identifiers (genesis hashes, genesis times, earlier fork
  points) were supplied from memory of the public chain configurations, not read from the EIPs.
  All rows reproduce with them, which would be unlikely if one were wrong.
- The classification of the strings that do not validate was done by reading their context.
- This result comes from one agent and was not re-run by a second one.
