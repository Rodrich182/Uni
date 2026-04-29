from collections import defaultdict


def main() -> None:
    left_cell = {
        "NNS": 0.0023,
        "VB": 0.001,
    }

    right_cell = {
        "PP": 0.2,
        "IN": 0.0014,
        "NNS": 0.0001,
    }

    binary_rules = [
        ("NP", "NNS", "NNS", 0.01),
        ("NP", "NNS", "PP", 0.01),
        ("VP", "VB", "PP", 0.045),
        ("VP", "VB", "NP", 0.015),
    ]

    candidates = []
    best = defaultdict(float)

    for parent, left_symbol, right_symbol, rule_prob in binary_rules:
        if left_symbol in left_cell and right_symbol in right_cell:
            prob = rule_prob * left_cell[left_symbol] * right_cell[right_symbol]
            candidates.append((parent, left_symbol, right_symbol, rule_prob, prob))
            best[parent] = max(best[parent], prob)

    print("Candidates for the next CKY cell:")
    for parent, left_symbol, right_symbol, rule_prob, prob in candidates:
        print(
            f"{parent} -> {left_symbol} {right_symbol} | "
            f"{rule_prob} * {left_cell[left_symbol]} * {right_cell[right_symbol]} = {prob}"
        )

    print("\nBest probability per constituent:")
    for symbol in sorted(best):
        print(f"{symbol} = {best[symbol]}")

    unary_pp_from_in = 0.002 * right_cell["IN"]
    print(f"\nUnary trap from PP -> IN on the right cell only: {unary_pp_from_in}")


if __name__ == "__main__":
    main()
