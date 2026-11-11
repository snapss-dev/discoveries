# Eight statements in Wikipedia chess articles that endgame tablebases refute

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the
repository README. Nothing was edited or reported on Wikipedia.

**Why this avenue.** Chess positions with at most seven men are solved: a tablebase gives the exact
result of every one of them, so a printed claim about such a position can be checked in seconds by
anyone, and a Wikipedia article carries its own complete history, so one can test whether an error
was noticed before. The Lichess puzzle database, the obvious first target, is already checked against
tablebases by Lichess developers (the tools `lichess-puzzle-tb-check` and `checkpuzzlestb`), so the
diagrams of eleven Wikipedias were audited instead, five of them in depth.

## The source

All 3,505 articles of the English, German, French, Spanish and Russian Wikipedias that use the
chess-diagram template, as served on 2026-11-11: 9,689 diagrams, of which 1,783 (1,404 distinct
positions) have both kings and at most seven men. Each of those was looked up in the Syzygy
tablebases with White to move and with Black to move, and compared with what the caption and the
text printed next to it say.

## Result

Eight statements are wrong. Each row quotes the live revision; "wins", "draws" and "loses" below are
tablebase facts for the exact position.

| | article (revision) | the article says | the tablebase says |
|---|---|---|---|
| G | de: *Ignace Vandecasteele* (259898544) | Study, "1233 Schakend Nederland 11/1970", White Ka4 Bb6 Ng6, Black Kh6 Nc1, pawns d5 h7: "Weiß zieht und gewinnt", solution 1. Sf4 Kg5 2. Le3 Sa2 3. Kb3 d4 4. Se6+ Kf5 5. Sxd4+ ... | The position is a **draw**. The printed line keeps the draw up to 4.Ne6+; then **4...Kg4** (not 4...Kf5) is the only move that holds it: the knight no longer takes on d4 with check, and both the bishop on e3 and the knight on a2 are attacked. |
| A | en: *Women's event at the 43rd Chess Olympiad* (1377227822) | "In this position, Mammadzada made a blunder by playing 106. Kh4? (106. Kh2 would have saved the game) and resigned immediately after 106... Kf3." | The diagram is the game position and it is **already lost**: 106.Kh2 loses too (Black then mates in 39 moves; after 106.Kh4, in 25). The losing move was **105.Kg3**; 105.Kh2 was the only drawing move, and 105...Rg1+ the only winning reply. From move 93, when five men were left, until then every position of the rook and knight against rook ending had been a draw. |
| B | en: *Open event at the 44th Chess Olympiad* (1381137688) | Diagram of Carlsen vs. Meier with White Kg5 Qf5, pawns g4 **h5**, Black Kh8 Qc5: "Meier lost defensive coordination by playing 78... Qe3+?. Instead, 78... Qc7!! would have held despite being two pawns down." | In the game the pawn stood on **h6**. With the pawn on h6, 78...Qc7 is indeed the only drawing move. In the position as diagrammed (pawn h5) every Black move loses, 78...Qc7 included. The diagram is wrong by one square. |
| D | de: *Abdrängung* (225061776) | Position "Richard Réti, 1928, Schluss einer Studie" (White Ke2 Re1, Black Ke5, pawns c2 g2): "Spielt Weiß hier 1. Ke2–d2+? (analog 1. Ke2–f2+?), so hält Schwarz mit 1. … Ke5–f4 (bzw. Ke5–d4) remis. Richtig ist 1. Ke2–e3!" | Black does **not** hold a draw. After 1.Kd2+ Kf4, and after 1.Kf2+ Kd4, White still wins, each time only by returning with 2.Ke2. The checks lose time, not the win. Eight first moves keep the win; 1.Ke3 is the fastest (mate in 39). |
| C | en: *Wrong bishop* (1356540113) | White Ke5 Rb7, pawn f6, Black Kf8 Bc4, Black to move draws: "1... Be2 2. Kf4 Bc4 3. Kg5 Bd5! 4. Rc7 Ba2! ..." (de la Villa 2008, pp. 219-21) | **1...Be2 loses** (2.Rc7, mate in 31); only 1...Ba2 and 1...Kg8 draw, and 2.Kf4 gives the draw back. The article *Fortress (chess)* prints the same line from the same pages with 1...Ba2, so "Be2" is a misprint, present since 2008. |
| E | de: *Endspiel Springer gegen Bauer* (256958683) | Chéron 1952, White Kh1 Ne6, pawn h5, Black Ke8 Nf5: "Weiß am Zug gewinnt mit 1. Sh6–g7+! Sf5xg7 2. h5–h6!" | There is no knight on h6. The only winning move is 1.Ne6-g7+; "Sh6" is a misprint for "Se6". |
| H | it: *Aggiramento (scacchi)* (152526685) | Third diagram, White Kd7 Rh1, Black Kd4, pawn b4, caption: "Il bianco muove e patta". The text under it: "Il bianco vince aggirando il pedone ... 1. Rc6! ... e il bianco vince." | White to move **wins**, by 1.Kc6 only (mate in 43). The caption repeats that of the two diagrams before it, which are draws, and contradicts the article's own text. |
| F | de: *Endspiel König und Bauer gegen König und Bauer* (267044445) | White Ke4, pawn g5, Black Ke7, pawn g6: "1. Ke5! Der einzige Gewinnzug. ... 1. … Kf7 2. Kd6! ebenfalls der einzige Gewinnzug" | 1.Ke5 is the only winning move, but after 1...Kf7 both 2.Kd6 (mate in 39) and 2.Kd5 (mate in 43) win. |

G, A, B and D are errors of substance; C, E and H are slips that a tablebase happens to certify;
F is a matter of convention (a move that only loses time is not usually counted as a second
solution), and so, in part, is D, although its sentence says in so many words that Black draws.

## How it was found

1. For every diagram with at most seven men the result for both sides to move was computed (five men
   and fewer: Syzygy tables probed locally; six and seven men: the public Lichess tablebase service).
   Captions containing a word for "wins" or "draws" were compared with it: 46 of 1,783 were flagged
   and read. One was item G. Two were studies that the articles themselves describe as refuted
   (the original 1895 stipulation of the Saavedra position, and the study in de: *Widerlegung
   (Schach)*). The rest were not contradictions: fairy pieces, variants, joke problems, positions
   drawn under the fifty-move rule, a study whose key move is castling, or a keyword used in another
   sense.
2. The numbered move sequences printed in the caption and after each diagram were replayed from the
   diagram and every move was compared with the tablebase: 1,700 moves from 991 diagrams with at most
   five men, and 517 moves from 264 six-man diagrams (26 material classes). A move was flagged when it
   carried "!" or no mark and worsened the result, when it carried "?" and did not change it, or when
   the text called it the only move and it was not. 155 flags were read; six were real (A to F); the
   others were variations the parser attached to the wrong position, or moves the text itself
   describes as mistakes. Russian lines were replayed separately with a notation adapter: 548 moves
   from 247 diagrams with at most six men, 35 flags read, none real.
3. A second, lighter pass (caption test only) covered the Italian, Polish, Portuguese, Ukrainian,
   Czech and Swedish Wikipedias: 1,772 articles, 3,558 diagrams, 408 with at most seven men, 89
   captions stating a win or a draw, 11 flagged and read, one real (item H). The Dutch and Hungarian
   templates use another format and were not read.
4. For the two game positions the full scores were taken from The Week in Chess (issues 1247 and
   1447) and replayed: the diagram of A occurs in the game before White's 106th move; the diagram of
   B does not occur in the game, and the position that does differs from it by the pawn on h6.

**Calibration.** The pipeline flags the two studies that Wikipedia already documents as refuted, and
confirms move for move analyses printed in the articles, for example the
drawing line 74.Kd3 Kg4 75.Ke2 Kh3 76.Kf2 of Ligterink - Schmidt 1975 in de: *Läuferendspiel*, where
76.Kf1 loses to exactly the two moves the article names, and the statement in ru: *Мат ферзём*
that from White Ka1 Qb2 against Ke6 every move except the two queen losses mates in exactly ten. The press reading of Carlsen - Meier
(78...Qc7 draws) is confirmed for the position actually played.

## How to check

`python check.py` replays the two game scores and the study line, and compares every statement of
the table with the saved answers of the Lichess tablebase service (`tablebase_2026-11-11.json`).
`python check.py --online` asks the service again. `python check.py --syzygy DIR` probes Syzygy WDL
files directly with python-chess; the 3-4-5-man set (378 MB) covers A, C, D, E, F and H, and
`KQPPvKQ.rtbw` covers B. `check.log` is the output of a run with both options: all 17 positions
agree in every source available for them. By hand: paste any position of `claims.json` into
https://lichess.org/analysis and open the tablebase tab.

The five-man results were obtained twice, with tables of different kinds and different probing code:
Syzygy tables read by python-chess, and the Lichess service, whose mate distances for five men come
from the separate Gaviota tables. `audit/` holds the scripts of the survey itself.

## Limits

- Item G is a seven-man position. Its table (26.5 GB) was not downloaded, so G rests on two public
  services, Lichess and chessdb.cn (`chessdb_2026-11-11.txt`), which agree move for move on the three
  key positions but may both read the same Syzygy files, plus the plain chess reason given in the
  table.
- The printed sources were not seen: the 1970 issue of Schakend Nederland, de la Villa's book,
  Dvoretsky's manual (cited by *Abdrängung*). So it is not known whether G and D are faults of the
  original publications or of the transcription into Wikipedia. The statement here is only that the
  live articles are wrong. Harold van der Heijden's study database, which records known busts, is
  not open and was not consulted; the bust of G may be recorded there.
- The game scores come from one source (The Week in Chess).
- Results ignore the fifty-move rule; all positions in the table are unconditional wins, losses or
  draws.
- The survey is far from exhaustive. The caption test only recognises a few words for win and draw
  in each language. The replay only follows numbered lines it can parse, not for
  seven men, and for six men only where the table had been downloaded. 411 of the 9,689 templates did
  not parse (and 543 of the 3,558 of the second pass, most of them Ukrainian). Diagrams with more
  than seven men were not examined at all.

## Novelty check (2026-11-11)

- Each statement is in the live revision named above. First revisions that contain the wording:
  A 862674116 (2018-10-05), B 1101682154 (2022-08-01, already with the pawn on h5), C 252403961 (2008-11-17), D 167653737
  (2017-07-27, a typography edit; the sentence may be older), E 256107191 (2025-05-18), F 206214481
  (2020-12-04), G 177799351 (2018-05-27, creation of the article), H 131340249 (2023-01-04).
- Talk pages: none exists for E, F, G and H; those of A and B hold project banners only; that of C
  holds one 2008 note on the article's class; the talk page of D (6,180 characters) was searched for
  the moves, "Réti", "remis" and "Tablebase" and does not mention this position. Edit
  summaries of all eight histories were searched for the moves and for "tablebase"; nothing.
- In-depth web searches for the Mammadzada - Zatonskih ending with 105.Kg3, 105.Kh2 and "tablebase",
  and for the Vandecasteele study with its pieces, source and "unsound", "cooked", "incorrect":
  no source names 105.Kg3 as the losing move (Chess.com's report speaks of "a critical decision that
  gave a 50-50 chance of walking into a mate" without naming the move), and no
  source discusses the study. The composer's own later collection (schaakstudiespinsels2.be, about
  300 studies indexed by material and king squares) has no study with this material and kings on
  a4 and h6.
- Existing tablebase audits found: the Lichess puzzle checkers named above. No audit of Wikipedia
  diagrams was found.

## Credit

Tablebases: Ronald de Man (Syzygy), Miguel Ballicora (Gaviota); seven-man Syzygy tables computed by
Bojun Guo; public probing service and python-chess by Niklas Fiekas and Lichess. Game scores: Mark
Crowther, The Week in Chess. The articles and their sources are credited in the table.
