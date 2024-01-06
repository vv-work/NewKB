Sure, here are examples of each in Python:

### Deque:
Deque (double-ended queue) is a versatile data structure that supports adding and removing elements from both ends efficiently.

```python
from collections import deque

# Initializing a deque
d = deque([1, 2, 3, 4, 5])

# Adding elements
d.append(6)  # Adding at the right end
d.appendleft(0)  # Adding at the left end

# Removing elements
d.pop()  # Removing from the right end
d.popleft()  # Removing from the left end

print(d)  # Output: deque([1, 2, 3, 4, 5])
```

### Heapify and Heap:
Heap is a specialized tree-based data structure that satisfies the heap property. The `heapify` function in Python organizes the elements into a heap.

```python
import heapq

# Example of heapify
arr = [4, 1, 7, 3, 8, 5]
heapq.heapify(arr)
print(arr)  # Output: [1, 3, 5, 4, 8, 7]

# Example of heap (priority queue)
heap = []
heapq.heappush(heap, 2)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
print(heapq.heappop(heap))  # Output: 1 (pops the smallest element)
```

### Trie:
Trie is a tree-like data structure used for efficient retrieval of key-value pairs. It's commonly used for searching words in dictionaries or autocomplete systems.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

# Usage
trie = Trie()
trie.insert("apple")
trie.insert("app")
print(trie.search("apple"))  # Output: True
print(trie.search("apples"))  # Output: False
```

### Prefix Sum:
Prefix sum is an array where each element at index 'i' contains the sum of all elements up to index 'i' in the original array.

```python
def calculate_prefix_sum(arr):
    prefix_sum = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    return prefix_sum

# Example
arr = [1, 2, 3, 4, 5]
prefix_sum = calculate_prefix_sum(arr)
print(prefix_sum)  # Output: [0, 1, 3, 6, 10, 15]
```

Feel free to explore and experiment with these structures in Python!
