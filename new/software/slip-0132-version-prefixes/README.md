# SLIP-0132: three rows print a key prefix that their version bytes cannot produce

Status: **new** (no earlier report found, see the novelty check). A small erratum in a registry table.
Produced with AI assistance; see the repository README.

## The source and what it says

SLIP-0132, "Registered HD version bytes for BIP-0032" (Clark Moody, created 8 February 2018, status
Active), in the public repository `satoshilabs/slips`, is a table of the 4-byte version values that
wallets put in front of BIP-32 extended keys, each printed with the text prefix it leads to, for
example "`0x0488b21e` - `xpub`". Its motivation says: "The `xpub` prefix is an artifact of Base58
encoding the four version bytes of the serialization format." The prefix is therefore a function of
the version bytes and can be recomputed. The file was read at commit
`238dd690ab326b23b316292e71d0cbdb1900b879` (the latest change to it, 15 June 2026).

## The result

An extended key is 78 bytes plus a 4-byte checksum, written in Base58. For each version value, the
smallest and the largest 82-byte strings that start with it were encoded; when both start with the
same four characters, every key with that version starts with them. This holds for all 68 cells of
the 34 rows. In 62 cells the printed prefix is the computed one. In 6 cells, on 3 rows, it is not:

| line | coin | printed | the version bytes give |
|---|---|---|---|
| 59 | Nexa | `0x42696720` - `xpub` | `F6iY` |
| 59 | Nexa | `0x426c6b73` - `xprv` | `F6rx` |
| 60 | Nexa Testnet | `0x043587cf` - `xpub` | `tpub` |
| 60 | Nexa Testnet | `0x04358394` - `xprv` | `tprv` |
| 61 | Vertcoin | `0x0488b21e` - `vtcp` | `xpub` |
| 61 | Vertcoin | `0x0488ade4` - `vtcv` | `xprv` |

The Vertcoin row has been in the table since the first version of the document (8 February 2018).
The Nexa rows were added in January 2023 (pull request #1481, "Add Nexa coin").

The table does not say which half of a cell is wrong. Vertcoin's version bytes are Bitcoin's, so its
keys start with `xpub` and `xprv`, and `vtcp` and `vtcv` would need other bytes. Nexa Testnet's bytes
are Bitcoin Testnet's, which the same table lists further up as `tpub` and `tprv`.

## Why it matters

Software that recognises a coin by the prefix column, or that builds a prefix-to-version map from
this table, gets a wrong entry for these rows: no key with these version bytes starts with `vtcp`,
and a Nexa main-network key does not start with `xpub` if the registered bytes are the ones in use.

## How to check

    python check.py

`check.py` reads `rows.json` (the 34 table rows, extracted from the Markdown), encodes the two
extreme values for each version with two Base58 routines that share no code, reproduces Bitcoin's
`xpub`, `xprv` and `tpub` first, and prints the cells that differ. Output is in `check.log`.

## Limits

- The check assumes the standard BIP-32 serialization (78 bytes, 4-byte checksum, Base58), which is
  what the document registers version bytes for. If a coin serializes extended keys differently, its
  row describes something this check does not model. Groestlcoin replaces the checksum hash; that
  does not change the leading characters.
- Which values the Nexa and Vertcoin software actually uses was not checked against their source.
- This result comes from one agent and was not re-run by a second one.

## Novelty check (11 November 2026)

- The file on the default branch has the rows as listed. Its 27 commits were listed by title; none
  announces a correction of them.
- Issue and pull request search in `satoshilabs/slips` for "vtcp" (nothing), "Nexa" (the pull
  request that added the rows, and one unrelated) and "Vertcoin 132" (unrelated).
- Web search for "SLIP-0132 Vertcoin vtcp vtcv 0x0488b21e": nothing that discusses the mismatch.
