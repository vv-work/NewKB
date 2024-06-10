# Trie

- Pronunce like **try**
- 

- [LC Crash Course explentation](https://leetcode.com/explore/interview/card/leetcodes-interview-crash-course-data-structures-and-algorithms/714/bonus/4549/)
- [208. Implment Trie(Prefix Tree) on **LC**](https://leetcode.com/problems/implement-trie-prefix-tree/description/ )

### Exmple 
 
Words: `apple`, `app`, `april`, `ban`, `bat`, `ball`

```mermaid

graph TD
    root((root)) -->|start| a0((A))
    root         -->|start| b0((B))
    a0 --> p1((P))
    p1 --> |end| p2[P]
    p2 --> l3((L))
    l3 --> |end| e4[E]

    p1 --> r2((R))
    r2 --> i3((I))
    i3 --> |end| l4[L]
    b0 --> a1((A))
    a1 --> |end|  n2[N]

```


## Implementation 

### Insertion example

```python
def insert(self, word: str) -> None:
    cur = self.root

    for c  in word:
        if c not in cur.children:
            cur.children[c] = TrieNode()
        cur = cur.children[c]
    cur.isEnd = True
```

Below is simple example of Trie data structure.


```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.isEnd = False

```

