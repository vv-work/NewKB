# Code Snippets & tricks


## Operations with Chars 

```python
ord('a') # 97
latters = [0] * 26 # array of all characters in the alphabet
for c in text:
    latters[ord(c) - ord('a')] += 1 # count the number of each character in the text
```
