# Quizz 7

## Answer ready to paste

Assumption used: the Earley chart is written with the variables of the grammar only, without an augmented start symbol. Under that convention:

List of items in `S7`:

- `[S $$\\rightarrow$$ NP VP $$\\bullet$$, 0]`
- `[VP $$\\rightarrow$$ V VP $$\\bullet$$, 3]`
- `[VP $$\\rightarrow$$ V NP $$\\bullet$$, 4]`
- `[NP $$\\rightarrow$$ D N $$\\bullet$$, 5]`
- `[N $$\\rightarrow$$ trap $$\\bullet$$, 6]`

Fill in the table:

| S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 |
|----|----|----|----|----|----|----|----|
| 6 | 6 | 4 | 7 | 12 | 12 | 6 | 5 |

The sentence is accepted because `S7` contains the completed start item:

- `[S $$\\rightarrow$$ NP VP $$\\bullet$$, 0]`

## Short derivation intuition

The sentence is:

```text
the big can trap can the trap
```

The successful path is:

```text
S => NP VP
NP => D J N         => the big can
VP => V VP          => trap VP
VP => V NP          => can NP
NP => D N           => the trap
```

## Important note about conventions

Some presentations of Earley add an augmented initial item:

```text
[GAMMA -> . S, 0]
```

If your professor uses that convention, then there is one extra item in `S0` and one extra item in `S7`:

- extra in `S0`: `[GAMMA $$\\rightarrow$$ $$\\bullet$$ S, 0]`
- extra in `S7`: `[GAMMA $$\\rightarrow$$ S $$\\bullet$$, 0]`

and the counts become:

| S0 | S1 | S2 | S3 | S4 | S5 | S6 | S7 |
|----|----|----|----|----|----|----|----|
| 7 | 6 | 4 | 7 | 12 | 12 | 6 | 6 |
