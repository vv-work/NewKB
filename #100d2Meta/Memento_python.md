```python
from collections import Counter
import heapq

  
class Solution:
	def topKFrequent(self, nums: List[int], k: int) -> List[int]:
	
		count = Counter(nums)
		return heapq.nlargest(k,count.keys(),key=count.get)
```
```csharp
int [] arr = {1,2,3,4,5};
arr.Sum(); // 15
arr.Max(); // 5
arr.Min(); // 1


// Convert char to int
char c = '5';
int number = c - '0';  // 5

// StringBuilder
StringBuilder sb = new StringBuilder();
sb.Append('a');

PriorityQueue<int> pq = new PriorityQueue<int>();
pq.Enqueue(5);


```

## Memoization through cache

```python
# memoization in Python 
@lru_cache(maxsize=None)
def min_path(row, col):
```

## input -> int 

```python
N = int(input().strip())
```
