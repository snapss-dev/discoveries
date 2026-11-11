# A243013: the seventh term should be 37, as another entry already shows

Status: **rediscovery**. The correct values are in A308544. Produced with AI assistance; see the
repository README.

## What was found here

[A243013](https://oeis.org/A243013) counts the graphs with n vertices and n - 1 edges that can be
gracefully labeled, and lists 1, 1, 1, 3, 5, 12, 36. The entry says the first six terms were calculated by
hand by a class of third-grade students, and its author wrote in the discussion that he might have made
an error.

On 2026-11-11 an agent computed the seventh term as 37, by three methods that agree: an enumeration of
all labelings in canonical form, a second implementation with a different search order, and a backtracking
test of every graph in the graph atlas. Of the 41 graphs with 7 vertices and 6 edges, exactly 4 cannot be
gracefully labeled: the bowtie with two isolated vertices, the 6-cycle with one, two triangles with one,
and a triangle together with the star K(1,3).

## Who had it first

[A308544](https://oeis.org/A308544) (graceful graphs on n edges with no isolated points) lists
1, 1, 3, 5, 12, 37, 112, 340, 1078, 3620, 12737, 46376. A graceful graph with n - 1 edges uses at most n
vertices, so padding with isolated vertices gives A243013(n) = A308544(n - 1). The value 37 and the later
terms are therefore already published there.

## What is not recorded

A243013 still shows 36, stops there, and has no cross-reference to A308544.

This result was not recomputed in a second pass; it rests on the agent's three methods and on the
agreement with A308544.
