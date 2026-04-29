from nltk.tree import Tree


def tree_depth(node):
    """Return tree depth recursively without using Tree.height()."""
    if not isinstance(node, Tree):
        return 0

    if len(node) == 0:
        return 0

    return 1 + max(tree_depth(child) for child in node)


def main():
    tree = Tree.fromstring("(S (NP I) (VP (V saw) (NP him)))")
    print(tree_depth(tree))


if __name__ == "__main__":
    main()
