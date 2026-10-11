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

## Imports 

```python 
from collections import defaultdit
from collections import deque 
import heapq 
```
## Adjacency list 

```python 

class GraphNode:
	def __init__(self,val):
		self.val = val
		self.neighbours = val
		
adjList = [ ["A", "B"] ,["B","C"], ["B","E"], ["C","E"] ,["E", "D"]]

adjList = {}

for src,dst in edges:
	if not src in adjList:
		adjList[src] = []
	if not dst in adjList:
		adjList[dst] = []
	adjList[src].append(dst)
```