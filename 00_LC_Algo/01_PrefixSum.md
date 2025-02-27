
## Prefix Sum

For prefix sum you just create array with first element in the begining. 
And then sum them all up


```python

def prefixSum(self,arr:[int])->[int]:
    prefix = [arr[0]]
    for i in range(1,len(arr)):
        prefix[i] = prefix[-1] +prefix[i]
```
