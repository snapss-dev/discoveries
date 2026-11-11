# ERC-7857: the storage constant in the reference contract is not the ERC-7201 slot of the namespace it names

Status: **new** (no earlier report found, see the novelty check). A documentation erratum in a Final
ERC, not a vulnerability. Produced with AI assistance; see the repository README.

## The source and what it says

ERC-7857, "AI Agents NFT with Private Metadata" (Ming Wu, Jason Zeng, Wei Wu, Michael Heinrich;
status Final since 4 November 2025), prints a reference contract `AgentNFT` in its Reference
Implementation section. The contract keeps its state in a namespaced storage struct, as defined by
ERC-7201 (Francisco Giordano, Hadrien Croubois, Ernesto García, Eric Lau, 2023). In
`ERCS/erc-7857.md` of the repository `ethereum/ERCs` at commit
`6504eb9dbd3f42c685f057fd2a7e7cd20b5bc391` (10 November 2026), line 653 reads

    /// @custom:storage-location erc7201:agent.storage.AgentNFT

and lines 673 to 675 read

    // keccak256(abi.encode(uint(keccak256("agent.storage.AgentNFT")) - 1)) & ~bytes32(uint(0xff))
    bytes32 private constant AGENT_NFT_STORAGE_LOCATION =
        0x4aa80aaafbe0e5fe3fe1aa97f3c1f8c65d61f96ef1aab2b448154f4e07594600;

ERC-7201 defines the slot of a namespace `id` as
`keccak256(abi.encode(uint256(keccak256(id)) - 1)) & ~bytes32(uint256(0xff))`, the expression in the
comment.

## The result

The expression in the comment, evaluated for `agent.storage.AgentNFT`, is

    0xaef0528c8e96d44c4fb121fd648f9a91b53cb890a08fb8040090fcd3cc553200

and not the printed `0x4aa80aaa…594600`. The constant is therefore not the ERC-7201 slot of the
namespace that the annotation and the comment name. Five other simple readings of the comment do not
give the printed constant either: the plain hash; the hash minus one, with and without the mask; the
double hash without the subtraction; and the full formula without the mask. Where the constant comes
from was not determined.

A contract of the same name, with the same comment and constant, is in the public repository
`0glabs/0g-agent-nft` (`contracts/AgentNFT.sol`, there since the commit "make contract upgradeable"
of 25 February 2025). That repository has eight constants of this form. Four match their comment
(`0g.storage.ERC7857`, `0g.storage.ERC7857Authorize`, `0g.storage.ERC7857Cloneable`,
`0g.storage.ERC7857IDataStorage`) and four do not (`agent.storage.AgentNFT`,
`agent.storage.AgentMarket`, `0g.storage.TEEVerifier`, `0g.storage.Verifier`). Only the first of
these eight is printed in the ERC.

## What follows from it, and what does not

- The contract still works. Any fixed 32-byte slot can serve as the root of the struct. No collision
  of the printed value with another slot was looked for or found.
- The `@custom:storage-location erc7201:…` annotation exists so that tools can find a contract's
  namespaced storage from its source. A tool that derives the slot from the annotation looks at
  `0xaef0…3200`, where a contract built from this text keeps nothing.
- Someone who notices the mismatch must not "correct" the constant in an upgrade of a contract that
  is already deployed behind a proxy: the new implementation would read its state from an empty
  location.
- Whether any deployed contract uses this constant was not examined.

## How to check

    python check.py

`check.py` implements Keccak-256 from the specification, cross-checks it against pycryptodome if that
is installed, reproduces five known ERC-7201 slots (the example in ERC-7201 and four constants of
OpenZeppelin Contracts), and then evaluates the formula for the ERC-7857 namespace and for the eight
constants of the repository above. Output is in `check.log`. By hand: with Foundry's `cast`,
`cast index-erc7201 agent.storage.AgentNFT` should print the value above (not run here).

## Limits

- Nothing was compiled or run on an EVM. The formula was evaluated in Python only, by two Keccak
  implementations that share no code.
- The ERC text does not itself cite the `0glabs/0g-agent-nft` repository; the link between the two is
  the contract name, the comment and the constant. The two files were not compared line by line.
- The search for the origin of the constant was short (five formula variants and about 300 guessed
  namespace strings).
- This result comes from one agent and was not re-run by a second one.

## Novelty check (11 November 2026)

- `ethereum/ERCs`, current default branch: the constant is present. It entered the text between the
  first version of the file (16 June 2025) and the move to Review (10 September 2025) and was not
  changed afterwards. The four pull requests with ERC-7857 in the title (#1160, #1207, #1222, #1284)
  are status moves and a rename.
- `0glabs/0g-agent-nft`: the eleven issues and pull requests, open and closed, by title; none is
  about storage locations. The default branch at commit `b86e108a` (2 February 2026) still has the
  constant.
- Web search for the constant itself and for "agent.storage.AgentNFT" with "ERC-7201": no result
  that discusses it.
- The Ethereum Magicians thread of ERC-7857 (8 posts, the last of 10 September 2025), read through a
  summarising fetch: no post mentions the constant or ERC-7201.
