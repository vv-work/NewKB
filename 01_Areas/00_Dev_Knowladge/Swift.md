
```swift
//wtf is that syntaxis 
var count  = [Int](repeating: 0, count: 26) 

// getting character `idx` why do we put ! in the `asciiValue`
let idk = Int(c.asciiValue!)  - 97 

// creating empty array by default
res[count, default: [ ]].append(s)  // why do we need to  initlize it in different way ? 
Array(res.values) 

//why do we use sometimes, `Array()` and other time `Array<Int>` 

```
Great questions! Let me break down these Swift syntax pieces:

## `[Int](repeating: 0, count: 26)`

This creates an **array of 26 integers, all initialized to 0**.

Breaking it down:
- `[Int]` = array type containing integers
- `(repeating: 0, count: 26)` = initializer that repeats the value `0` exactly `26` times

So you get: `[0, 0, 0, ..., 0]` (26 zeros total)

**Why 26?** One slot for each letter a-z.

---

## `Int(c.asciiValue!) - 97`

This converts a character to its position (0-25).

Breaking it down:
- `c.asciiValue` returns an optional `Int?` (might be nil if character has no ASCII value)

- The `!` **force-unwraps** the optional, asserting "I know this is safe, give me the value"

- ASCII value of 'a' is 97, so subtracting 97 gives: 'a'→0, 'b'→1, ..., 'z'→25

**Why the `!`?** In this case it's safe because we know `strs[i]` contains only lowercase English letters (per constraints). But it's risky in general—if the character doesn't have an ASCII value, your code crashes.

---

## `res[count, default: []].append(s)`

This is Swift's dictionary subscript with a **default value**.

Breaking it down:
- `res[count]` = look up the array associated with key `count`
- `, default: []` = if key doesn't exist, use an empty array `[]` instead
- `.append(s)` = add string `s` to that array

**Why different syntax?** This is a convenient shorthand. Instead of:
```swift
if res[count] == nil {
    res[count] = []
}
res[count]!.append(s)
```

You get a cleaner one-liner that automatically creates the array if needed.

---

## `Array(res.values)` vs `Array<Int>`

These do **different things**:

**`Array(res.values)` ** = converts dictionary values to an array
- `res.values` gives you a collection of all arrays in your dictionary
- `Array()` wraps it into a concrete array type
- Result: `[[String]]` (array of arrays of strings)

**`Array<Int>`** = declares a type, not a conversion
- This is a **type annotation**, like writing `: Array<Int>` or `: [Int]`
- Used when you need to specify what type something is

**Different contexts:**
```swift
// Type annotation (what type is this?)
var count: Array<Int> = [0, 0, 0]
// or more commonly:
var count: [Int] = [0, 0, 0]

// Conversion (turn something into an array)
let arr = Array(someDictionary.values)
```

## Takeaways:
- if `res` hashSet and we need. to unwrap those values. 
- res[count, default: []].append(s) // Way to initialize default value. like defaultdict in python
- Array(dict.values) // turning dictionary values into Array, 


        var count = [Int:Int]()

        for num in nums{
            count[num, default: 0] += 1
        }

        var arr = [(Int, Int)]()

        for (num, cnt) in count {
            arr.append((cnt,num))
        }

        arr.sort { $0.0 < $1.0 } // sorting with { }

        var res = [Int]()

        while res.count < k {
            res.append(arr.removeLast().1)
        }

        return res
