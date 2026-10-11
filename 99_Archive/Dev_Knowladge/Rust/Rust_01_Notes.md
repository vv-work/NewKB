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


## Options and NULL 

Rust has enum types reprsenting null(absent) data type `Some(T)` `None`


The `Option` enum in Rust is a powerful way to handle situations where a value might be present or absent. It is defined as follows:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

- `Some(T)`: This variant contains a value of type `T`.
- `None`: This variant represents the absence of a value.

Using `Option` helps avoid issues related to null references (like null pointer exceptions in other languages). Instead of returning a null value, a function can return an `Option` to explicitly indicate that a value might or might not be present.

Here's a simple example:

```rust
fn divide(numerator: f64, denominator: f64) -> Option<f64> {
    if denominator == 0.0 {
        None
    } else {
        Some(numerator / denominator)
    }
}

fn main() {
    let result = divide(4.0, 2.0);
    match result {
        Some(value) => println!("Result: {}", value),
        None => println!("Cannot divide by zero"),
    }
}
```

In this example:

- The `divide` function returns an `Option<f64>`, indicating that the result might be a floating-point number (`Some(value)`) or might not be available (`None`).
- The `match` statement in the `main` function handles both cases, ensuring that the program can safely deal with the possibility of division by zero.


## Exeustive Pattern Matching

In Rust, exhaustively matching an enum means that when you use a `match` expression to handle an enum, you provide patterns for all possible variants of that enum. This ensures that every possible value the enum can take is accounted for, preventing runtime errors from unhandled cases.

Here's a basic example to illustrate this concept:

Suppose you have an enum representing a traffic light:

```rust
enum TrafficLight {
    Red,
    Yellow,
    Green,
}
```

To exhaustively match this enum, you need to handle all possible variants (`Red`, `Yellow`, and `Green`) in your `match` expression:

```rust
fn describe_light(light: TrafficLight) {
    match light {
        TrafficLight::Red => println!("Stop"),
        TrafficLight::Yellow => println!("Caution"),
        TrafficLight::Green => println!("Go"),
    }
}

fn main() {
    let light = TrafficLight::Red;
    describe_light(light);
}
```

In this example:

- The `match` expression in the `describe_light` function has a pattern for each of the three possible `TrafficLight` variants.
- If you forget to include one of the variants, the Rust compiler will produce an error, indicating that the match is not exhaustive. This helps catch potential bugs at compile time.

Exhaustively matching enums is a key feature of Rust's type system, promoting safety and correctness by ensuring that all possible cases are handled explicitly.
