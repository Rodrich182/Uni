# Quiz 6

```python
from nltk.tree import Tree


def tree_depth(node):
    if not isinstance(node, Tree):
        return 0

    if len(node) == 0:
        return 0

    return 1 + max(tree_depth(child) for child in node)


tree = Tree.fromstring("(S (NP I) (VP (V saw) (NP him)))")
print(tree_depth(tree))
```

Answer:

```text
3
```
