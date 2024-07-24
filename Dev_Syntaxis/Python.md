# Python

Python is a high-level, interpreted, interactive and object-oriented scripting language. Python is designed to be highly readable. It uses English keywords frequently where as other languages use punctuation, and it has fewer syntactical constructions than other languages.

## Lambda and Sorting 


```python
add = lambda x,y: x+y

def add(x,y):
    return x+y
# Both above are the same

sorted(height_name, key=lambda x: x[1], reverse = True)

```

## Data Types

```python
dict(zip(names,heights)) # Creates diectionary
list(zip(names,heights)) # Creates 2D array
set() #creates HashSet

```
### Ordered diectionary

```python
height_to_name_map = OrderedDict()
# Sort the OrderedDict by height in descending order
height_to_name_map = OrderedDict( sorted(height_to_name_map.items(), reverse=True))
```
