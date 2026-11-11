# Twenty-seven interface identifiers and selectors printed in ERC documents do not match the signatures they are printed for

Status: **new** for 26 of the 27 values (no earlier report found, see the novelty check); the ERC-6059
value was already known and is credited below. Documentation errata, not vulnerabilities. Produced with
AI assistance; see the repository README.

## The source and what it says

Ethereum's application standards (ERCs) are Markdown files in the public repository `ethereum/ERCs`.
Many of them print an ERC-165 interface identifier next to a Solidity interface, typically in the form
"Note: the ERC-165 identifier for this interface is 0x…". ERC-165 (Christian Reitwießner, Nick
Johnson, Fabian Vogelsteller, Jordi Baylina, Konrad Feldmeier, William Entriken, 2018) defines that
identifier as the XOR of the 4-byte selectors of the interface's functions, and a selector as the
first four bytes of the Keccak-256 hash of the canonical signature. So every printed identifier can
be recomputed from the interface printed beside it. A contract that follows the text and a contract
that lets the compiler compute `type(I).interfaceId` answer `supportsInterface` differently whenever
the two disagree.

All values below refer to the repository at commit `6504eb9dbd3f42c685f057fd2a7e7cd20b5bc391`
(10 November 2026). Line numbers are lines of `ERCS/erc-<number>.md`.

## The result

Every 4-byte hexadecimal value in the 626 ERC texts and the 971 EIP texts was extracted and compared
with the selectors and identifiers recomputed from the declarations in the same document. 291 values
reproduce. 27 do not.

### Group A: documents with status Final or Last Call

| ERC | status | line | printed for | printed | recomputed from the printed interface | what reproduces the printed value |
|---|---|---|---|---|---|---|
| 7401 | Final | 68 | `IERC7059` (the ERC-7401 interface) | `0x42b0e56f` | `0x14a07a0c` | `addChild` with a third parameter `bytes data`, as in the reference interface `assets/erc-7401/contracts/IERC7401.sol` |
| 6059 | Final | 64 | `IERC6059` | `0x42b0e56f` | `0xf71e99d2` | `addChild` and `nestTransferFrom` each with a trailing `bytes data`. Known, see below |
| 5007 | Final | 32 | `IERC5007` | `0xf140be0d` | `0x7a0cdf92` | not found. The text printed `0x7a0cdf92` until 25 April 2023 |
| 5507 | Final | 49 | `ERC20Refund` | `0xf0ca2917` | `0x4d1444d1` | the interface without `refundFrom` |
| 5507 | Final | 104 | `ERC721Refund` | `0xe97f3c83` | `0x54a15145` | the interface without `refundFrom` |
| 5507 | Final | 207 | `ERC1155Refund` | `0x94029f5c` | `0xebd3ba73` | the interface without `refundFrom` |
| 5496 | Last Call | 37 | `IERC5496` | `0x076e1bbb` | `0xc906a5cb` | `setPrivilege` with `uint64 expires`, as in the reference implementation printed in the same document |

What is wrong in each case, and how that is known:

- **ERC-7401.** Judged by the reference implementation, the declaration in the text is the wrong
  half and the identifier is right. The text declares
  `function addChild(uint256 parentId, uint256 childId) external;`. The reference interface in the
  same repository declares `addChild(uint256 parentId, uint256 childId, bytes memory data)`, the
  reference test asserts `0x42b0e56f`, and only the three-parameter form gives that value. ERC-7401
  exists because of this kind of slip. Its own text says: "This proposal fixes the inconsistency in
  the ERC-6059 interface specification, where interface ID doesn't match the interface specified as
  the interface evolved during the proposal's lifecycle, but one of the parameters was not added to
  it." It added the missing `data` parameter to `nestTransferFrom` and left `addChild` as it was. The
  first version of the file (26 July 2023) already has the two-parameter `addChild`. The interface is
  also still named `IERC7059` in the text.
- **ERC-6059.** Same identifier, and two declarations that lack the `data` parameter. This one is
  known: it was reported for `nestTransferFrom` in the discussion thread in July 2023 and is the
  stated reason for ERC-7401 (see Credit).
- **ERC-5007.** The identifier is wrong, the declaration is right. The interface has two functions,
  `startTime(uint256)` and `endTime(uint256)`, and their selectors XOR to `0x7a0cdf92`. The text
  printed `0x7a0cdf92` from July 2022 until the commit "Update EIP-5007: update
  ERC5007Composable.sol" (25 April 2023) replaced it with `0xf140be0d` without changing the
  interface. The reference test `assets/erc-5007/test/test.js` still calls
  `supportsInterface('0x7a0cdf92')`. No combination of the five function signatures in the document
  gives `0xf140be0d`.
- **ERC-5507.** The identifiers are stale. They were added on 26 December 2022 ("Add interface IDs
  and use consistent formatting"). `refundFrom` was added to all three interfaces on 23 February
  2023 ("Improve Motivation and add refundFrom") and the identifiers were not recomputed. Each
  printed value is exactly the XOR of the other three functions. The two batch extensions in the same
  document print an empty identifier.
- **ERC-5496.** The declaration and the reference implementation disagree on one type. The interface
  declares `setPrivilege(uint256 tokenId, uint256 privilegeId, address user, uint256 expires)`; the
  reference implementation further down the same document, and the interface file in the assets
  folder, use `uint64 expires`. The printed identifier belongs to the `uint64` form. Line 74 makes it
  normative ("The `supportsInterface` method MUST return `true` when called with `0x076e1bbb`"), while
  the implementation printed in the text returns `type(IERC5496).interfaceId`, which for the interface
  as printed is `0xc906a5cb`.

### Group B: other statuses, cause identified

| ERC | status | line | what is printed | printed | recomputed | cause |
|---|---|---|---|---|---|---|
| 1538 | Withdrawn | 158 | comment `0x03A9BCCF == bytes4(keccak256("updateContract(address,string,string)"))`, and the value is used in `abi.encodeWithSelector` | `0x03a9bccf` | `0x61455567` | not found. The same document gives `0x61455567` as the identifier of the one-function interface |
| 7897 | Withdrawn | 191 | assembly `mstore(0x00, 0xd786d393) // DeployFailed()` | `0xd786d393` | `0xb4f54111` | not found |
| 725 | Draft | 289, 298 | `IERC725X` in the summary listing | `0x7545acac` | `0x28f19dd8` | the listing writes `bytes memory datas` in `executeBatch`; the method section writes `bytes[]`, which gives the printed value |
| 1185 | Review | 56 | "`dnsRecords()` ... has function signature `0x2461e851`" | `0x2461e851` | `0xa8fa5682` | the code in the document names the function `dnsRecord` and sets `DNS_RECORD_INTERFACE_ID = 0xa8fa5682` |
| 1417 | Stagnant | 86 | `IPoll` | `0x4fad898b` | `0xd1983698` | the interface without `getVoterBaseDenominator()` |
| 998 | Draft | 1140 | `ERC998ERC20BottomUp` | `0xffafa991` | `0x3617a1cb` | the interface without `transferFromParentERC223` |
| 4393 | Stagnant | 64 | `ITipToken`, comment inside the interface | `0x985a3267` | `0xe47a7022` | the paragraph above the interface requires `0xE47A7022`, the correct value |
| 8121 | Draft | 112 | comment `bytes4(keccak256(functionSignature)); // 0x1837de7f` for `"getContractMetadata(string)"` | `0x1837de7f` | `0x9e574b14` | not found. Line 166 of the same document uses `0x9e574b14` for this signature |
| 5700 | Draft | 144 | `IERC1155Bindable` | `0xd0d555c6` | `0xc6f44642` | the interface of the same name in the assets folder, whose parameter lists differ. The requirement sentence at line 139 prints the value with a digit missing, `0xd0d55c6` |

### Group C: other statuses, cause not determined

The printed value is not the XOR of any subset of the functions declared in the document.

| ERC | status | line | printed for | printed | recomputed |
|---|---|---|---|---|---|
| 1261 | Stagnant | 71 | `IERC1261` | `0x1d8362cf` | `0xf8779878` |
| 1844 | Stagnant | 31 | `interfaceImplementer(bytes32,bytes4)` | `0xb8f2bbb4` | `0x124a319c` |
| 4353 | Stagnant | 33 | `IERC721Staked` | `0x3a3d855f` | `0x5a459ed4` |
| 5635 | Stagnant | 40 | `IERC5635DNFT` | `0xd584841c` | `0xbda94636` |
| 5635 | Stagnant | 95 | `IERC5635Registry` | `0xb5065e9f` | `0x59213334` |
| 5700 | Draft | 44 | `IERC721Bindable` | `0x82a34a7d` | `0x11806543` |
| 5791 | Draft | 106 | `IERC5791` | `0x4901df9f` | `0x83e70509` |
| 6353 | Stagnant | 45 | `IERC20charity` | `0x557512b6` | `0xaceb828b` |
| 7204 | Draft | 50 | `IERC7204` | `0xf73edcda` | `0x4b090fea` |
| 7561 | Draft | 112 | comment above the reference contract `ERC7561` | `0xc1b31357` | `0x304ad1f2` for `IERC7561` |
| 7604 | Draft | 144 | `IERC1155Permit` | `0x7409106d` | `0x29011db4` |

ERC-5635 also states `bytes4(keccak256("IERC5635DNFT{}")) == 0xd584841c`; that hash begins
`0x37c007c8`.

### Group D: the text and the reference interface disagree, no identifier printed

Found by comparing each interface in a text with the interface of the same name in the document's
assets folder. 209 pairs were compared and 182 are identical. Of the 27 that differ, the three in
Final documents that are not already in group A are listed; the rest are in Draft, Review, Stagnant
or Last Call documents (ERC-5496 and ERC-725 appear above), or differ only through a type the parser
could not resolve.

| ERC | status | text | reference file | difference |
|---|---|---|---|---|
| 7066 | Final | line 111, `transferAndLock(uint256 tokenId, address from, address to, bool setApprove)`, selector `0xd0feac0a` | `assets/erc-7066/IERC7066.sol`, `transferAndLock(address from, address to, uint256 tokenId, bool setApprove)`, selector `0xa07b4087` | argument order; identifiers `0x18e33afa` and `0x6866d677` |
| 5169 | Final | line 69, `setScriptURI(string[])` | `assets/erc-5169/contract/ExampleContract.sol`, `updateScriptURI(string)` | the example contract carries an earlier interface; identifiers `0xa86517a1` and `0x2488f6c0` |
| 3643 | Final | line 304, `isTokenBound(address)` in `ICompliance` | `assets/erc-3643/interfaces/ICompliance.sol` | the function is missing from the reference interface |

In ERC-7066 the text links the assets file as its "Reference Interface", so a reader who copies the
linked file gets a function that a caller written from the text cannot reach. In the discussion
thread one of the authors wrote the signature in the order of the reference interface
(piyushchittara, 16 June 2023), so the order in the text may be the slip.

### Group E: the interface and the implementation printed in the same document disagree

Found by comparing each interface in a text with every contract in the same text that declares it
as a parent (129 pairs). Besides ERC-5496 above:

| ERC | status | interface | implementation in the same text |
|---|---|---|---|
| 7820 | Final | line 113, `getRoleInfo(address _contract) returns (bool isActive, address admin)`, selector `0x07483499` | line 309, `getRoleInfo(address targetContract, address account, bytes32 role) returns (bool)`, selector `0x6cf94b35` |
| 7656 | Final | line 142, `linkedData()`, selector `0x7e110a1d` (the printed identifier) | line 201, `linkedData(address service)`, selector `0x33c3411a` |
| 7085 | Draft | line 50, `setAttribute(uint256,string,uint256)` | `setAttribute(uint256,bytes32,bytes32)` |

In ERC-7820 the prose (line 137) describes the three-argument form, and the interface entry repeats
the comment and the return values of the neighbouring `getContractInfo`, so the interface entry is
the slip; a contract cannot implement the interface as printed and behave as the prose says. In
ERC-7656 the example contract calls `linkedData()` without arguments a few lines after declaring it
with one, so the stray parameter is in the example.

## Why it matters

A Final ERC is changed only to correct errata. A contract written from the ERC-5007 text returns `true`
for `0xf140be0d`, while a marketplace that asks for `type(IERC5007).interfaceId` asks for
`0x7a0cdf92` and gets `false`, and the other way round. The same holds for the ERC-5507 and ERC-5496
values, and for an ERC-7401 contract whose `addChild` is written from the text. This is an
interoperability problem. No way to lose funds through it was looked for or found.

## How to check

    python check.py

`check.py` reads `cases.json` (the signatures as declared in each document, the printed value, and
the changed signature list where a cause was found), recomputes every selector with a Keccak-256
written from the specification, and compares it with pycryptodome if that is installed. It first
reproduces twelve identifiers that the documents print correctly. Output is in `check.log`. To check a
row by hand, read the cited lines of the document and hash the signatures with any Keccak-256 tool.

## Limits

- The signatures in `cases.json` were extracted from the Markdown by a parser written for this
  check: comments stripped, `uint` read as `uint256`, structs expanded to tuples, enums read as
  `uint8`, contract types as `address`. Groups A and B and the three rows of group D were also read by
  eye, as were ERC-7820 and ERC-7656 in group E. Group C was read by eye only for the function
  names and parameter types.
- 199 further 4-byte values in the texts were not classified one by one. Most are bytecode offsets,
  example call data or constants; an identifier claim among them could have been missed. 10 printed
  identifiers could not be recomputed from the document alone (for example ERC-1450, whose formula
  ends in "...", and ERC-7498, whose struct is declared with a non-Solidity `extends`).
- Of the 291 values that reproduce, 22 are identifiers of other standards (for example `0x80ac58cd`
  for ERC-721) and were recomputed once from those standards' signatures, not from the citing
  document. 42 further values are `0xffffffff` or `0x00000000`.
- Nothing was compiled or run on an EVM. No deployed contract was examined.
- For group C the correct value could be either side; the page only states that the two disagree.
- This result comes from one agent and was not re-run by a second one.

## Novelty check (11 November 2026)

- Current default branch of `ethereum/ERCs` at the commit above: all values are present as listed.
- File history: none of the group A files changed in `ethereum/ERCs` since the move from
  `ethereum/EIPs` (25 October 2023), apart from ERC-7401 assets typos. History before the move was
  read in `ethereum/EIPs` for ERC-5007, 5507, 5496 and 7401; the dates above come from it.
- Pull requests and issues: title searches in `ethereum/ERCs` for 7401, 5007, 5507, 5496, 7066, 5169
  and 7820, and in `ethereum/EIPs` for 7401, 5007, 5507 and 7066. The two ERC-7401 pull requests
  (#980 merged, #1566 open) fix spelling only; the open ERC-7066 pull request #1540 fixes spelling
  only; the open ERC-725 pull request #1139 keeps `bytes memory datas`; the two open ERC-7656 pull
  requests (#1977, #1978) are, by their titles, about other things. All 338 open pull requests of
  `ethereum/ERCs` were listed by title and none announces a fix for these values. An issue search
  of `ethereum/ERCs` for `0xf140be0d`, `0x7a0cdf92`, `0x14a07a0c` and `0x4d1444d1` returns nothing.
- Web searches for `0xf140be0d` and `0x7a0cdf92`, for the three printed ERC-5507 values, for
  "ERC-7401 addChild bytes data interface id", and for surveys of wrong ERC-165 identifiers in ERC
  texts: nothing found about these documents.
- Ethereum Magicians threads, read through a summarising fetch, not post by post: ERC-6059 and
  ERC-7401 (one shared thread, 36 posts to 18 October 2023; `addChild` is never connected to a
  missing parameter), ERC-5507 (24 posts), ERC-5007 (10 posts), ERC-5496 (4 posts), ERC-7066
  (19 posts). None mentions the values or mismatches listed here, apart from the ERC-6059 report
  credited below.
- Not read: the threads of the group B and C documents.

## Credit

The ERC-6059 mismatch was reported by lukasz-glen in the Ethereum Magicians thread on 6 July 2023:
"The function `nestTransferFrom()` declared in EIP and in attached implementation mismatch. The
parameter `data` is missing." ThunderDeliverer (Jan Turk) confirmed on 18 July 2023 that "The
interface ID in the proposal takes the missing parameter into account", and the ERC-6059 authors
(Bruno Škvorc, Cicada, Steven Pineda, Stevan Bogosavljevic, Jan Turk) wrote ERC-7401 as the fix. The
remaining rows have no earlier record that this search could find.
