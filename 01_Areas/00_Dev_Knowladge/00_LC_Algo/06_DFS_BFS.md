## DFS & BFS 

```python

class TreeNode:
	def __init__(self,val = 0,left=None,right=None):
		self.val = val
		self.left = left
		self.right = right

# preorder iteration 
def dfs(node:TreeNode):
	if not node: 
		return 
	print(node.val)
	
	dfs(node.left)
	dfs(node.right)
		
```

## Depth First Search 
