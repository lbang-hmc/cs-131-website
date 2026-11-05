# Lab 8: Lambda Calculus Encodings

[Module 08.1](../modules/08.1-lambda-calculus-foundations.md) introduced the lambda calculus and the `lc` interpreter. [Module 08.2](../modules/08.2-encoding-data-with-functions.md) showed how Booleans, pairs, lists, and numbers can all be encoded as functions. In this lab, you write the missing pieces yourself. Part 1 finishes the list operations, and Part 2 builds arithmetic on Church numerals. [HW 08](../assignments/hw08.md) uses these same encodings, so the time you spend here pays off there.

## Objectives

- Load a file of definitions into `lc` and read its reduction output.
- Write `IsNil`, `Head`, and `Tail` for the tagged list representation.
- Use a Church numeral as a loop to define `Plus` and `Times`.
- Finish Kleene's predecessor trick by writing `NextPair`.
- Explain why some encoded operations take many more β-reductions than others.

!!! note "How you'll get the starter code"
    The starter code is a small public repository, [`hmc-cs-131-fa-2026/lambda-calc-lab`](https://github.com/hmc-cs-131-fa-2026/lambda-calc-lab). On the course server, clone it directly. You don't need to make your own copy first:

    ```bash
    cd cs131
    git clone https://github.com/hmc-cs-131-fa-2026/lambda-calc-lab.git
    cd lambda-calc-lab
    ```

    **Run `lc` from this `lambda-calc-lab` folder** so that `:load encoding.lc` can find the file.

    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a terminal on the server yet.

!!! note "Gradescope"
    At the end of the lab, upload your `encoding.lc` to the **Lab 08** assignment on Gradescope. Lab credit is for completion, not correctness, but give every definition a real try. HW 08 assumes you can do this.

    Work on your own copy and submit individually. Talking problems over with the people around you is encouraged.

!!! note "Solutions"
    The repo includes a `solution/` folder with a finished `encoding.lc`. Give the lab your best shot on your own first. Look at the solution after the lab, or once you've really run out of ideas.

!!! tip "You've done this before"
    Remember [Higher-Order Arithmetic in HW 2](../assignments/hw02.md#higher-order-arithmetic)? `applyN f n x` applied `f` to `x`, `n` times, and you built `addition` and `multiplication` from it and `increment`. That's exactly what a Church numeral does, so you were already doing lambda calculus without knowing it. If you get stuck on `Plus` or `Times` in Part 2, go back and look at how you wrote `addition` and `multiplication`.

---

## Warmup: `lc` and `encoding.lc`

Start the interpreter and load the starter file:

```
lc
:load encoding.lc
```

`lc` lists the macros it just loaded. Six of them are placeholders you'll replace: `IsNil`, `Head`, and `Tail` in Part 1, and `Plus`, `Times`, and `NextPair` in Part 2. `Pred` and `Monus` are written for you, but they're built on `NextPair`, so they won't give correct answers until you've fixed it. Everything else (`True`, `False`, `Not`, `And`, `Or`, `Pair`, `Fst`, `Snd`, `Nil`, `Cons`, `Succ`, and `IsZero`) already works.

!!! example "Try it in lc - nothing to submit"
    Evaluate

    ```
    ((And ((Or True) False)) ((And True) True))
    ```

    Scroll back up to where you typed it and read the trace. Notice that `lc` doesn't expand a macro like `Or` until it has to. The result should be `(λx.(λy.x))`, which is `True`.

    Then try `((True False) True)` and `(Fst ((Pair True) False))`. Predict each answer before you press Enter.

A few commands you'll use all lab:

| Command | What it does |
|---|---|
| `:reload` (or `:r`) | Reload `encoding.lc` after you edit it |
| `:set trace compact` | Show a shorter trace |
| `:set trace off` | Show only the result and the step count |
| `:set trace full` | Show every step again |
| `:help` | List all commands |

Type `\` for λ. Up-arrow brings back earlier inputs.

---

## Part 1: Lists

A list is either empty or has a head and a tail. `encoding.lc` uses the **tagged representation** from Module 08.2. Every list is a pair whose first component answers "is this list empty?":

| List | Built with | Encoded as |
|---|---|---|
| `[]` | `Nil` | `(True, True)` |
| `[2]` | `((Cons 2) Nil)` | `(False, (2, (True, True)))` |
| `[1,2]` | `((Cons 1) ((Cons 2) Nil))` | `(False, (1, (False, (2, (True, True)))))` |

The second component of `Nil` is never used. For a `Cons`, it's another pair holding the head and the tail.

In `encoding.lc`, `IsNil`, `Head`, and `Tail` are placeholders that always return `True`. Replace them so that, for any `h` and `t`:

| Expression | Should reduce to |
|---|---|
| `(IsNil Nil)` | `True` |
| `(IsNil ((Cons h) t))` | `False` |
| `(Head ((Cons h) t))` | `h` |
| `(Tail ((Cons h) t))` | `t` |

You may assume `Head` and `Tail` are only ever applied to a list built by `Cons`. For each one, ask where the information lives in the representation, and which of `Fst` and `Snd` gets you there.

!!! example "Try it in lc"
    After `:reload`, check all four rows of the table. Plain variables like `a` and `b` work fine for `h` and `t`, so `(Head ((Cons a) b))` should give `a`. Then try a longer list, such as `(Head (Tail ((Cons a) ((Cons b) Nil))))`.

---

## Part 2: Arithmetic with Church Numerals

`lc` has the Church numerals built in. The numeral `n` takes a function and a starting value and applies the function `n` times:

| Numeral | Definition | `((n f) x)` reduces to |
|---|---|---|
| `0` | `(λf.(λx.x))` | `x` |
| `1` | `(λf.(λx.(f x)))` | `(f x)` |
| `2` | `(λf.(λx.(f (f x))))` | `(f (f x))` |
| `3` | `(λf.(λx.(f (f (f x)))))` | `(f (f (f x)))` |

So a numeral is a loop. `((7 g) v)` runs `g` seven times, starting from `v`. Every definition in this part comes from choosing the right `g` and the right `v`.

When a result is exactly one of the built-in numerals, `lc` sometimes prints it by name, for example `0` or `3`, instead of writing out the λ-expression. Both forms mean the same thing.

### Successor

`Succ` is given:

```
Succ = (\n.(\f.(\x. (f ((n f) x)))));
```

`((n f) x)` applies `f` `n` times, and the outer `f` applies it once more.

!!! example "Try it in lc"
    Check `(Succ 0)`, `(Succ 1)`, and `(Succ 6)`. Count the `f`s in each answer.

### Addition

Fix `Plus` so that `((Plus n) m)` reduces to the numeral for `n + m`.

- `Plus` takes two arguments, so it's a curried function: `(\n.(\m. ...))`.
- Adding `m` to `n` is the same as taking the successor `m` times, starting at `n`.

!!! example "Try it in lc"
    `((Plus 2) 2)` should reduce to `(λf.(λx.(f (f (f (f x))))))`. Also try `((Plus 0) 3)` and `((Plus 3) 0)`.

### Multiplication

Fix `Times` so that `((Times n) m)` reduces to the numeral for `n × m`.

- Multiplying `n` by `m` is the same as adding `m`, `n` times, starting at `0`.
- That means the function you repeat is "add `m`". What does `(Plus m)` give you?

!!! example "Try it in lc"
    `((Times 3) 2)` should reduce to the numeral `6`. Then check that `((Times 0) 5)` gives `0`.

### IsZero

`IsZero` is already defined:

```
IsZero = (\n. ((n (\x.False)) True));
```

It starts at `True` and applies "ignore your argument and return `False`" `n` times. If `n` is `0`, nothing is applied and the answer stays `True`. Applying the function even once gives `False`.

!!! example "Try it in lc"
    Check `(IsZero 0)`, `(IsZero 1)`, and `(IsZero 7)`.

### Predecessor

Subtracting one is the hard direction. You can't un-apply a function, so there's no direct way to turn "apply something 10 times" into "apply something 9 times." The logician Stephen Kleene found a way around this using a sequence of pairs:

| Step | Pair |
|---|---|
| 0 | `(0, 0)` |
| 1 | `(0, 1)` |
| 2 | `(1, 2)` |
| 3 | `(2, 3)` |
| 4 | `(3, 4)` |

Each pair comes from the one before it by the same rule: `(a, b)` becomes `(b, b+1)`. Start at `(0, 0)`, apply the rule `n` times, and the first component is `n − 1`. (There are no negative numerals, so `0` is its own predecessor.)

`Pred` is given and follows that recipe exactly:

```
Pred = (\n. (Fst ((n NextPair) ((Pair 0) 0))));
```

But `NextPair` is a placeholder. Fix it so that it takes one pair `p` from the sequence and returns the next one. You already have `Pair`, `Snd`, and `Succ`.

!!! example "Try it in lc"
    `(Pred 3)` should reduce to the numeral `2`, and `(Pred 0)` should reduce to `0`. If `Pred` is off, test `NextPair` alone first, for example `(Fst (NextPair ((Pair 1) 2)))` and `(Snd (NextPair ((Pair 1) 2)))`.

### Subtraction

Addition is repeated `Succ`, so subtraction can be repeated `Pred`. `encoding.lc` defines this for you:

```
Monus = (\n.(\m. ((m Pred) n)));
```

Because nothing goes below `0`, subtracting a bigger number from a smaller one gives `0`. That's not quite subtraction, so the operation gets its own name: *monus*.

!!! example "Try it in lc"
    Run `:set trace off`, then try `((Monus 4) 2)` and `((Monus 2) 4)`. You should get `2` and `0`. Compare the step counts with `((Plus 4) 2)`.

!!! question "Think about it"
    `((Monus 4) 2)` takes many more β-reductions than `((Plus 4) 2)`. Look at how `Pred` is defined, and explain where the extra steps come from. How would you expect the cost to grow as the numbers get bigger?

---

## Submitting

Make sure `encoding.lc` loads without errors (`:reload` should list all the macros), then upload `encoding.lc` to **Lab 08** on Gradescope.

!!! tip "Checking your work"
    Compare your definitions with [`solution/encoding-lab-solution.lc`](https://github.com/hmc-cs-131-fa-2026/lambda-calc-lab/blob/main/solution/encoding-lab-solution.lc). There's more than one correct answer. If yours is different and passes every check above, it's fine.
