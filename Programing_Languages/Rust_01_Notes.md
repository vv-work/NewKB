# Rust Notes

## Borowing


### Overview
Borrowing in Rust allows functions to access data without taking ownership. There are two types of borrowing:
1. **Immutable Borrowing** (`&T`)
2. **Mutable Borrowing** (`&mut T`)

### Immutable Borrowing (`&T`)
Immutable borrowing lets you read data without modifying it. Multiple immutable borrows are allowed simultaneously, ensuring data is read-only.

#### Example
```rust
fn main() {
    let x = 10;
    let y = &x; // Immutable borrow
    
    println!("Value of x: {}", x);
    println!("Value of y: {}", y);
}
```
In this example, `y` is an immutable reference to `x`. Both `x` and `y` can be read, but neither can be modified.

#### Context
Use immutable borrowing when you need to read data without changing it, and when multiple parts of your program need to access the data concurrently.

### Mutable Borrowing (`&mut T`)
Mutable borrowing allows you to modify the borrowed data. Only one mutable borrow is allowed at a time to ensure safe, concurrent access to data.

#### Example
```rust
fn main() {
    let mut x = 10;
    {
        let y = &mut x; // Mutable borrow
        *y += 5; // Modify the borrowed data
    } // y goes out of scope here
    
    println!("Value of x: {}", x);
}
```
In this example, `y` is a mutable reference to `x`. Within the inner scope, `y` modifies `x` by adding 5. After `y` goes out of scope, `x` is printed with the modified value.

#### Context
Use mutable borrowing when you need to modify data. Ensure no other references (immutable or mutable) exist to the data while it's mutably borrowed. This prevents data races and ensures memory safety.

## Rules of Borrowing
1. **One Mutable Reference or Many Immutable References:**
   - You can have either one mutable reference or any number of immutable references, but not both simultaneously.
2. **References Must Be Valid:**
   - References must always be valid. Rust's borrow checker enforces these rules at compile time, preventing dangling references and data races.

#### Example Demonstrating Borrowing Rules
```rust
fn main() {
    let mut x = 10;
    
    let r1 = &x; // Immutable borrow
    let r2 = &x; // Another immutable borrow
    println!("r1: {}, r2: {}", r1, r2);
    
    // let r3 = &mut x; // Error: cannot borrow `x` as mutable because it is also borrowed as immutable
    // println!("r3: {}", r3);
    
    let r4 = &mut x; // Mutable borrow after immutable borrows go out of scope
    *r4 += 5;
    println!("r4: {}", r4);
}
```
In this example, `r1` and `r2` are immutable borrows, which are allowed simultaneously. Trying to create `r3`, a mutable borrow, while `r1` and `r2` are in scope would result in a compile-time error. After the immutable borrows go out of scope, `r4` can be created as a mutable borrow.

