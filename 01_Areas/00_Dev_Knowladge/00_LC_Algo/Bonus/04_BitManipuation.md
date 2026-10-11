# Binary Operation

## Operation

- OR    `|`
- AND   `&`
- XOR   `^`
- Shift `>>`,`<<`

### Example

`x=14`# 1110  
`y=13`# 1101

| Name   | Oper  |  =   | Bits |
|--------|-------|------|------| 
|**OR**  | `x\|y`| `15` | 1111 | 
|**AND** | `x&y` | `12` | 1100 | 
|**XOR** | `x^y` | `2`  | 0010 | 
|L Shift | `x>>y`| `7`  | 0111 | 
|R Shift | `x<<y`| `30` | 11110| 


```python
x = 5#101
bin(x) # get Binary represenatio of number
# out: 0b101
x>>1 # Binary shift right
# out: 2 (010)
x<<1 # Binary shift left
# out: 10(1010)
x^1 # XOR operation
# out 4(100) 
```

## Notes

<details>

<summary>
<code>O(logN)</code> complexity of shifting
</summary>


 **Not** `O(N)` **If we are shifting** `>>` or `<<` to the left our complexity would be
 Because we basically multiplying or deviding by **2**

</details>


## Bitmask(mask)

- [ 136 Single Number](https://leetcode.com/problems/single-number/)



