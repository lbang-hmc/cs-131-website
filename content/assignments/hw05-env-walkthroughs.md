# HW 5: Environment Walkthroughs

Step-by-step traces of the **variable environment** as the compiler works through a piq program: what the
environment is before each statement, and what it is after. These are the environments that `compileStmt` /
`compileStmts` / `compileLoop` (see [HW 5](hw05.md)) pass from one statement to the next.

One notation note before you start: these traces write the environment as `{ x ↦ 10 }`. HW 5's own `ghci` checks
show the exact same environment as `fromList [("x",10.0)]` — that's just how `Data.Map` prints an `Env`. Same
value, two notations.

## How to read a trace

```
    env  {}                       ← the environment at this point
x = 10                            ← a statement (concrete piq syntax)
    env  { x ↦ 10 }               ← the environment after it (= before the next statement)
y = x * 2                         -- a note: what gets evaluated, what gets drawn
  » save i: none                  ← a step the compiler takes that isn't a statement
```

- `{ x ↦ 10, y ↦ 20 }` is an environment where `x` is 10 and `y` is 20. `{}` is the empty environment. The order
  inside the braces doesn't matter (GHCI prints them in alphabetical order, as `fromList [("x",10.0),("y",20.0)]`).
- Every value is a `Double`; whole numbers are written without the `.0`.
- Only the **variable** environment is shown. The procedure environment (`box ↦ its definition`, …) is built once
  from the `define`s before anything runs, and never changes.
- Drawing statements leave the environment alone, so their env line is just repeated. Where nothing interesting
  happens, a few env lines are skipped.

---

## Part 4: assignment and sequences {: #part4 }

### Example 1: assignment, drawing, reassignment {: #ex1 }

```
    env  {}
x = 10                            -- 10
    env  { x ↦ 10 }
y = x * 2                         -- x * 2 = 10 * 2 = 20
    env  { x ↦ 10, y ↦ 20 }
square y                          -- y = 20: draws a 20 mm square
    env  { x ↦ 10, y ↦ 20 }
x = x + y                         -- x + y = 10 + 20 = 30
    env  { x ↦ 30, y ↦ 20 }
```

- An assignment evaluates its right-hand side in the environment **before** it, then binds the name.
- A drawing statement uses the environment but doesn't change it.
- Assigning to a name that already has a value replaces the value. The env after one statement is exactly the
  env before the next: that's what `compileStmts` threads along.

### Example 2: doubling (`part4Doubling`) {: #ex2 }

```
    env  {}
x = 10
    env  { x ↦ 10 }
square x                          -- 10 mm square
x = x * 2                         -- uses the OLD x: 10 * 2 = 20
    env  { x ↦ 20 }
square x                          -- 20 mm square
x = x * 2                         -- 20 * 2 = 40
    env  { x ↦ 40 }
square x                          -- 40 mm square
    env  { x ↦ 40 }
```

- `x = x * 2` is not an equation. The `x` on the right is looked up in the env before the statement.

### Example 3: using a variable before it has a value {: #ex3 }

```
    env  {}
x = 10
    env  { x ↦ 10 }
square y                          -- look up y in { x ↦ 10 }: not there
                                  -- STOPS: undefined variable: y
y = 20                            -- never reached
```

- Each statement only sees what the statements **before** it produced. It doesn't matter that `y` gets a value
  later.

---

## Part 5: loops {: #part5 }

### Example 4: an accumulator {: #ex4 }

```
    env  {}
total = 0
    env  { total ↦ 0 }
for i from 1 to 4 {
  » bounds, evaluated once in { total ↦ 0 }: 1 and 4, so i takes 1, 2, 3, 4
  » save i: none (i has no value yet)

  ── i = 1 ──                     -- start from the env before the loop, set i ↦ 1
      env  { total ↦ 0, i ↦ 1 }
  total = total + i               -- 0 + 1 = 1
      env  { total ↦ 1, i ↦ 1 }

  ── i = 2 ──                     -- start from the env iteration 1 left, set i ↦ 2
      env  { total ↦ 1, i ↦ 2 }
  total = total + i               -- 1 + 2 = 3
      env  { total ↦ 3, i ↦ 2 }

  ── i = 3 ──
      env  { total ↦ 3, i ↦ 3 }
  total = total + i               -- 3 + 3 = 6
      env  { total ↦ 6, i ↦ 3 }

  ── i = 4 ──
      env  { total ↦ 6, i ↦ 4 }
  total = total + i               -- 6 + 4 = 10
      env  { total ↦ 10, i ↦ 4 }

  » restore i: it had no value before, so remove it
}
    env  { total ↦ 10 }
```

- Each iteration starts from the environment the **previous iteration** left, with the loop variable set to the
  next value. That's how `total` accumulates (`compileLoop` threads the env just like `compileStmts`).
- Assignments to other variables (`total`) survive the loop.
- The loop variable doesn't: it was saved as "none", so afterwards it's removed.

### Example 5: a loop variable that already had a value {: #ex5 }

```
    env  {}
i = 100
    env  { i ↦ 100 }
for i from 1 to 3 {
  » bounds: 1 and 3
  » save i: 100

  ── i = 1 ──
      env  { i ↦ 1 }
  dot
      env  { i ↦ 1 }

  ── i = 2 ──
      env  { i ↦ 2 }
  dot
      env  { i ↦ 2 }

  ── i = 3 ──
      env  { i ↦ 3 }
  dot
      env  { i ↦ 3 }

  » restore i: put back 100
}
    env  { i ↦ 100 }
square i                          -- still a 100 mm square
```

- Inside the loop, `i` is the loop's `i`. Afterwards, the old `i` is back, as if the loop had never touched it.

### Example 6: the bounds are evaluated once {: #ex6 }

```
    env  {}
n = 3
    env  { n ↦ 3 }
for i from 1 to n {
  » bounds, evaluated once in { n ↦ 3 }: 1 and 3, so i takes 1, 2, 3 (fixed from now on)
  » save i: none

  ── i = 1 ──
      env  { n ↦ 3, i ↦ 1 }
  n = n + 1                       -- 3 + 1 = 4
      env  { n ↦ 4, i ↦ 1 }

  ── i = 2 ──
      env  { n ↦ 4, i ↦ 2 }
  n = n + 1                       -- 5. n is now bigger than 3, but the loop still stops after i = 3
      env  { n ↦ 5, i ↦ 2 }

  ── i = 3 ──
      env  { n ↦ 5, i ↦ 3 }
  n = n + 1                       -- 6
      env  { n ↦ 6, i ↦ 3 }

  » restore i: remove it
}
    env  { n ↦ 6 }
```

- Changing `n` inside the loop doesn't change how many times it runs: the list of values `[1 .. 3]` was made
  before the first iteration.

### Example 7: zero iterations, and a bad bound {: #ex7 }

```
    env  {}
x = 1
    env  { x ↦ 1 }
for i from 5 to 1 {
  » bounds: 5 and 1, so i takes no values at all ([5 .. 1] is [])
  » save i: none
  x = x * 10                      -- never runs
  » restore i: remove it (it isn't there anyway)
}
    env  { x ↦ 1 }                -- unchanged, and no code was produced
for i from 1 to x / 2 {
  » bounds, in { x ↦ 1 }: 1 and 0.5
                                  -- STOPS: non-integral loop bound: 0.5
  dot
}
```

### Example 8: nested loops {: #ex8 }

```
for row from 1 to 2 {
  for col from 1 to 2 {
    dot
    move right 10
  }
  move left 20
  move down 10
}
```

```
    env  {}
for row from 1 to 2 {
  » bounds: 1 and 2;  save row: none

  ── row = 1 ──
      env  { row ↦ 1 }
  for col from 1 to 2 {
    » bounds: 1 and 2;  save col: none

    ── col = 1 ──
        env  { row ↦ 1, col ↦ 1 }
    dot
    move right 10
        env  { row ↦ 1, col ↦ 1 }

    ── col = 2 ──
        env  { row ↦ 1, col ↦ 2 }
    dot
    move right 10
        env  { row ↦ 1, col ↦ 2 }

    » restore col: remove it
  }
      env  { row ↦ 1 }
  move left 20
  move down 10
      env  { row ↦ 1 }

  ── row = 2 ──                   -- start from the env row 1 left: { row ↦ 1 }, set row ↦ 2
      env  { row ↦ 2 }
  for col from 1 to 2 {
    » bounds: 1 and 2;  save col: none (removed at the end of row 1)

    ── col = 1 ──
        env  { row ↦ 2, col ↦ 1 }
    dot
    move right 10

    ── col = 2 ──
        env  { row ↦ 2, col ↦ 2 }
    dot
    move right 10
        env  { row ↦ 2, col ↦ 2 }

    » restore col: remove it
  }
      env  { row ↦ 2 }
  move left 20
  move down 10
      env  { row ↦ 2 }

  » restore row: remove it
}
    env  {}
```

- The inner loop is just a statement in the outer loop's body, so it runs (save, iterate, restore) once per outer
  iteration. `col` appears and disappears each time; `row` stays put for a whole row.

---

## Part 6: procedures {: #part6 }

### Example 9: a simple call {: #ex9 }

```
define box(size, gap) {
  half = size / 2
  move right half
  square size
  move right half + gap
}
```

(A variant of `box` from `part6Boxes`, with a local variable `half`.)

```
    env  {}
w = 5
    env  { w ↦ 5 }
box(w * 2, 3)
  » look up box: parameters size, gap
  » 2 arguments for 2 parameters: OK
  » evaluate the arguments in the CALLER's env { w ↦ 5 }: w * 2 = 10, and 3
  » local env = caller's env + size ↦ 10, gap ↦ 3
      env  { w ↦ 5, size ↦ 10, gap ↦ 3 }
  half = size / 2                 -- 10 / 2 = 5
      env  { w ↦ 5, size ↦ 10, gap ↦ 3, half ↦ 5 }
  move right half                 -- 5
  square size                     -- 10 mm square
  move right half + gap           -- 5 + 3 = 8
      env  { w ↦ 5, size ↦ 10, gap ↦ 3, half ↦ 5 }
  » keep the body's code; throw its env away
    env  { w ↦ 5 }                -- the caller's env, exactly as it was before the call
```

- The arguments are evaluated where the call **is**, before the body starts.
- The body runs in a new local environment: the caller's, plus the parameters. (So the body could also read `w`.)
- Nothing the body does to the environment (`half`, `size`, `gap`) escapes. The call returns the caller's env
  unchanged, plus the body's code.

### Example 10: a parameter with the same name as a caller variable (`part6Shadowing`) {: #ex10 }

```
define foo(x) {
  x = x + 100
  square x
}
```

```
    env  {}
x = 10
    env  { x ↦ 10 }
foo(20)
  » evaluate the argument in { x ↦ 10 }: 20
  » local env = { x ↦ 10 } + x ↦ 20   (the parameter hides the caller's x)
      env  { x ↦ 20 }
  x = x + 100                     -- 20 + 100 = 120
      env  { x ↦ 120 }
  square x                        -- 120 mm square
      env  { x ↦ 120 }
  » throw the local env away
    env  { x ↦ 10 }
square x                          -- 10 mm square
```

- The body's `x` is the parameter. Changing it changes only the local environment, which disappears after the
  call.

### Example 11: a call inside a loop (`part6Boxes`) {: #ex11 }

```
define box(size, gap) {
  move right size / 2
  square size
  move right size / 2 + gap
}

move left 80
for i from 1 to 5 {
  box(i * 8, 10)
}
```

```
    env  {}
move left 80
    env  {}
for i from 1 to 5 {
  » bounds: 1 and 5;  save i: none

  ── i = 1 ──
      env  { i ↦ 1 }
  box(i * 8, 10)
    » arguments, in { i ↦ 1 }: 1 * 8 = 8, and 10
    » local env:
        env  { i ↦ 1, size ↦ 8, gap ↦ 10 }
    move right size / 2           -- 4
    square size                   -- 8 mm square
    move right size / 2 + gap     -- 4 + 10 = 14
    » throw the local env away
      env  { i ↦ 1 }

  ── i = 2 ──
      env  { i ↦ 2 }
  box(i * 8, 10)
    » arguments, in { i ↦ 2 }: 16, and 10
    » local env:
        env  { i ↦ 2, size ↦ 16, gap ↦ 10 }
    move right size / 2           -- 8
    square size                   -- 16 mm square
    move right size / 2 + gap     -- 18
    » throw the local env away
      env  { i ↦ 2 }

  ── i = 3, 4, 5: the same, with size 24, 32, 40 ──
      env  { i ↦ 5 }

  » restore i: remove it
}
    env  {}
```

- Each call gets a fresh local environment built from the env **at that moment** (here, with the current `i`).
- `size` and `gap` never show up in the loop's own environment.

### Example 12: a procedure that calls a procedure that has a loop {: #ex12 }

```
define target(r) {
  for k from 1 to 3 {
    circle k * r / 3
  }
  dot
}

define flower(r) {
  d = 2 * r
  target(r)
  move up d
  target(r / 2)
  move down d
}

move left 80
flower(15)
```

(A cut-down version of `part6Flowers`.)

```
    env  {}
move left 80
    env  {}
flower(15)
  » argument, in {}: 15
  » flower's local env = {} + r ↦ 15
      env  { r ↦ 15 }
  d = 2 * r                       -- 30
      env  { r ↦ 15, d ↦ 30 }
  target(r)
    » argument, in flower's env { r ↦ 15, d ↦ 30 }: 15
    » target's local env = flower's env + r ↦ 15
        env  { r ↦ 15, d ↦ 30 }
    for k from 1 to 3 {
      » bounds: 1 and 3;  save k: none
      ── k = 1 ──
          env  { r ↦ 15, d ↦ 30, k ↦ 1 }
      circle k * r / 3            -- radius 5
      ── k = 2 ──
          env  { r ↦ 15, d ↦ 30, k ↦ 2 }
      circle k * r / 3            -- radius 10
      ── k = 3 ──
          env  { r ↦ 15, d ↦ 30, k ↦ 3 }
      circle k * r / 3            -- radius 15
      » restore k: remove it
    }
        env  { r ↦ 15, d ↦ 30 }
    dot
    » throw target's local env away
      env  { r ↦ 15, d ↦ 30 }     -- back in flower, with flower's env
  move up d                       -- 30
  target(r / 2)
    » argument, in flower's env: 15 / 2 = 7.5
    » target's local env = flower's env + r ↦ 7.5   (target's r hides flower's r)
        env  { r ↦ 7.5, d ↦ 30 }
    for k from 1 to 3 {
      » bounds: 1 and 3;  save k: none
      ── k = 1, 2, 3 ──           -- radius 2.5, 5, 7.5
          env  { r ↦ 7.5, d ↦ 30, k ↦ 3 }   (after the last iteration)
      » restore k: remove it
    }
        env  { r ↦ 7.5, d ↦ 30 }
    dot
    » throw target's local env away
      env  { r ↦ 15, d ↦ 30 }     -- flower's r is 15 again
  move down d                     -- 30
  » throw flower's local env away
    env  {}
```

- Calls nest: each call builds its local env from the env of whoever called it, and each one's env is thrown away
  when it finishes, returning to its caller's env.
- Inside `target`, `d` is visible (it came from flower's env), even though `target` doesn't use it.
