# Sorting 

## Problems to repeat

- [ 2418 Sort the People](https://leetcode.com/problems/sort-the-people/)
- [ 1636 Sort by increasing Freq](https://leetcode.com/problems/sort-array-by-increasing-frequency/)

## Resources
- [Counting Sort](https://leetcode.com/explore/learn/card/sorting/695/non-comparison-based-sorts/4437/)


## Lambda 

- ❗`lambda x: (freq[x], -x)` - Sort by frequency and then by value

```python
add = lambda x,y: x+y

# The same add(x,y) -> return x+y
sorted(height_name, key=lambda x: x[1], reverse = True)

freq = Counter(nums)
sorted(nums, key = lambda x: (freq[x], -x))
```

## Data Types

```python
dict(zip(names,heights)) # Creates diectionary
list(zip(names,heights)) # Creates 2D array
set() #creates HashSet

```

### Sorting custom


```python

counter = Counter(data)
# Sort the Counter by the amount of elements
sorted_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)

```
### Ordered dictionary

```python
height_to_name_map = OrderedDict()
# Sort the OrderedDict by height in descending order
height_to_name_map = OrderedDict( sorted(height_to_name_map.items(), reverse=True))
```
