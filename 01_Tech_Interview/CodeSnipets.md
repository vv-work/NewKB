# Code Snippets & tricks


## Operations with Chars 

```python
ord('a') # 97
latters = [0] * 26 # array of all characters in the alphabet
for c in text:
    latters[ord(c) - ord('a')] += 1 # count the number of each character in the text
```

## DFS through array 

```python
def leafSimilar(root1,root2):
    def dfs(self, node):
        if node:
            if not node.left and not node.right:
                yield node.val
            yield from dfs(node.left)
            yield from dfs(node.right)
```
