## Python `collections.Counter` Class

The `collections.Counter` class in Python is a part of the `collections` module. It is a dict subclass which helps count hashable objects. Inside of it, elements are stored as dictionary keys and the counts of the objects are stored as the value.

Let's take a look at a simple example:

```python
from collections import Counter
# Create a list of fruits
fruits = ['apple', 'banana', 'apple', 'banana', 'orange', 'banana']
# Use Counter to count the number of each fruit in the list
fruit_counter = Counter(fruits)
print(fruit_counter)
```

When you run this code, you'll get the following output:

```python
Counter({'banana': 3, 'apple': 2, 'orange': 1})
```

This shows that 'banana' appears 3 times, 'apple' 2 times, and 'orange' 1 time in the list.

The `Counter` holds the data in an unordered collection, just like hashtable objects. The elements here represent the keys and the count as values.

---

I hope this helps! Let me know if you have any other questions.


## Python Dictionary

A dictionary in Python is an unordered collection of items. Each item of a dictionary has a key/value pair. Dictionaries are optimized to retrieve values when the key is known.

Here is a simple example:

```python
# Create a dictionary
person = {'name': 'John', 'age': 30, 'city': 'New York'}
# Access elements
print(person['name'])
print(person['age'])
```

This will output:

```python
John
30
```

This shows that the 'name' key corresponds to the value 'John' and the 'age' key corresponds to the value 30 in the dictionary.

Dictionaries are very flexible in the data types they can hold. For example:

```python
# A dictionary can hold different data types
person = {'name': 'John', 'age': 30, 'cities_visited': ['New York', 'Los Angeles', 'Chicago']}
```

In this case, the 'cities_visited' key corresponds to a list of cities.


## Python `collections.defaultdict` Class

The `collections.defaultdict` class in Python is a dict subclass that calls a factory function to supply missing values. In other words, it does not raise a KeyError when you try to access a non-existent key. Instead, it will return a default value given by the factory function.

Here is an example with `int` as the factory function:

```python
from collections import defaultdict
# Create a defaultdict with int as the default factory
count = defaultdict(int)
# Access a non-existent key
print(count['non_existent_key'])
```

This will output:

```python
0
```

This shows that accessing a non-existent key in the defaultdict returns 0, the default value for int.

And here is an example with `str` as the factory function:

```python
from collections import defaultdict
# Create a defaultdict with str as the default factory
s = defaultdict(str)
# Access a non-existent key
print(s['non_existent_key'])
```

This will output:

```python
'''
```

This shows that accessing a non-existent key in the defaultdict returns an empty string, the default value for str.
