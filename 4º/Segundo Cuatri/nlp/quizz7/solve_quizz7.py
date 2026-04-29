from __future__ import annotations

from dataclasses import dataclass


GRAMMAR = {
    "S": [("NP", "VP")],
    "NP": [("D", "J", "N"), ("D", "N"), ("J", "N")],
    "VP": [("V", "VP"), ("V", "NP")],
    "D": [("the",)],
    "J": [("big",)],
    "N": [("can",), ("trap",)],
    "V": [("can",), ("trap",)],
}

TOKENS = ["the", "big", "can", "trap", "can", "the", "trap"]


@dataclass(frozen=True, order=True)
class Item:
    lhs: str
    rhs: tuple[str, ...]
    dot: int
    start: int

    def is_complete(self) -> bool:
        return self.dot == len(self.rhs)

    def next_symbol(self) -> str | None:
        if self.is_complete():
            return None
        return self.rhs[self.dot]

    def advance(self) -> "Item":
        return Item(self.lhs, self.rhs, self.dot + 1, self.start)

    def render(self) -> str:
        pieces = list(self.rhs)
        pieces.insert(self.dot, ".")
        return f"[{self.lhs} -> {' '.join(pieces)}, {self.start}]"


def run_earley(use_augmented_start: bool) -> list[set[Item]]:
    grammar = {lhs: list(rules) for lhs, rules in GRAMMAR.items()}
    nonterminals = set(grammar)
    start_symbol = "S"

    if use_augmented_start:
        grammar["GAMMA"] = [(start_symbol,)]
        nonterminals.add("GAMMA")
        seed = Item("GAMMA", (start_symbol,), 0, 0)
    else:
        seed = Item(start_symbol, grammar[start_symbol][0], 0, 0)

    chart = [set() for _ in range(len(TOKENS) + 1)]
    chart[0].add(seed)

    def close_set(i: int) -> None:
        changed = True
        while changed:
            changed = False
            for item in list(chart[i]):
                next_symbol = item.next_symbol()

                if next_symbol is None:
                    for parent in list(chart[item.start]):
                        if parent.next_symbol() == item.lhs:
                            advanced = parent.advance()
                            if advanced not in chart[i]:
                                chart[i].add(advanced)
                                changed = True
                elif next_symbol in nonterminals:
                    for production in grammar[next_symbol]:
                        predicted = Item(next_symbol, production, 0, i)
                        if predicted not in chart[i]:
                            chart[i].add(predicted)
                            changed = True

    for i in range(len(TOKENS) + 1):
        close_set(i)
        if i == len(TOKENS):
            break

        token = TOKENS[i]
        for item in list(chart[i]):
            if item.next_symbol() == token:
                chart[i + 1].add(item.advance())

    return chart


def print_chart(name: str, chart: list[set[Item]]) -> None:
    print(name)
    for i, states in enumerate(chart):
        print(f"S{i} ({len(states)} items)")
        for item in sorted(states):
            print("  " + item.render())
        print()


def main() -> None:
    plain_chart = run_earley(use_augmented_start=False)
    augmented_chart = run_earley(use_augmented_start=True)

    print_chart("Without augmented start symbol", plain_chart)
    print_chart("With augmented start symbol", augmented_chart)


if __name__ == "__main__":
    main()
