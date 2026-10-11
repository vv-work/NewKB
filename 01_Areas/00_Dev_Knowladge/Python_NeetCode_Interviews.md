# NeetCode course Python for coding interviews 

## Sorting 

### Flashcards 

1. Timsort
2. ascending, descending 
3. lexographical 


### Sorting 

```python 
words = ["apple", "app", "apricot", "banana", "berry", "blueberry"]
res = sorted(key=x:lambda x:len(x),reverse=True)
print(res)
```
> ['blueberry', 'banana', 'apricot', 'apple', 'berry', 'app']

## Pythonic Code  

### Flashcards

1. Pythonic code 
2.`enumerate(nums)` 

### Unpacking

```python 
point1 = [0, 0]
x1, y1 = point1 # x1 = 0, y1 = 0

demensions:Tuple[int, int] = (1920,1080)
x,y = demensions # x = 1920, y = 1080
```

### Loop Unpacking 

```python 
points = [[0,1],[2,4],[3,6],[5,7]]

for x,y in points:
    print(x={x},y={y})
```
> x=0, y=1 \n x=2, y=4 \n x=3, y=6 \n x=5, y=7


### Enumerator 

```python 
nums = [5,3,6,2,1,4]

for i,num in enumerate(nums):
    print(f'{i} : {num})

dic = {num:i for i,num in enumerate(nums)}

```
> 0 : 5 \n 1 : 3 \n 2 : 6 \n 3 : 2 \n 4 : 1 \n 5 : 4

### Zip 

❗`TC: O(1)`
❗`SC: O(1)`

```python
names = ["John", "Jane", "Doe"]
ages  - [25, 30, 22]

for name,age in zip(names,ages):
    print(f'{name} is {age} years old')
```
> John is 25 years old \n Jane is 30 years old \n Doe is 22 years old

### Inequality 

```python
inRange = 1 <= x < 10
```

### Max/Min

```python
nums = [5,3,6,2,1,4]
max(nums[i]-nums[i-1] for i in range(1,len(nums)))
```

## Lists

### Flash cards 

1. `insert()`, `rindex()`, `copy.deepcopy()`
2. Comprehension: 
```python 
    [i+j for i,j in zip(arr1,arr2)]
```

### Basics

```python
my_list = [1,2,3] 

my_list.append(4)   # [1,2,3,4]
my_list.pop()       # [1,2,3]

my_list.insert(1,3) # [1,3,2,3]
```

### Basics II

```python 
arr = [1,3,2,3]

arr.index(3)     # 1
arr.remove(3)    # [1,2,3] 
arr.extend([4,5])# [1,2,3,4,5]
arr + [6,7]      # [1,2,3,4,5,6,7]
```

### Copy

```python 
clone1 = arr.copy()
clone2 = arr[:]
clone3 = list(arr)

import copy 

deep_clone = copy.deepcopy(arr)
```
### List comprehension

```python
arr1,arr2 = [1,2,3],[4,5,6]
arr3 = [i+j for i,j in zip(arr1,arr2)]

even = [i for i in range(10) if i%2 == 0]
```


