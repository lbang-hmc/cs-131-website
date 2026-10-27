# Lab 7: From Higher-Order Functions to Monads

[Module 7.1](../modules/07.1-functors-generalizing-map.md) and [Module 7.2](../modules/07.2-monads-composing-computations.md) introduced functors and monads. In this lab you use them. Part 1 is a quick run from `map` to `>>=` on `Maybe`. Part 2 writes one stack-calculator program three ways, and the third version uses a monad. Part 2 is where the lab really happens, so try to get there within the first half hour.

## Objectives

- Write small functions in pointfree style and combine them with `.`.
- Use `fmap` to apply a plain function to a value inside a `Maybe` or a list.
- See for yourself where `.` and `fmap` fail, and use `>>=` instead.
- Follow one calculator program from hand-threaded state, to a homemade combinator, to `do` notation.

!!! note "How you'll get the starter code"
    The starter code is a small public repository, [`hmc-cs-131-fa-2026/monad-lab`](https://github.com/hmc-cs-131-fa-2026/monad-lab). On the course server, clone it directly. You don't need to make your own copy first:

    ```bash
    cd cs131
    git clone https://github.com/hmc-cs-131-fa-2026/monad-lab.git
    cd monad-lab
    ```

    **Run every command below from this `monad-lab` folder.**

    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a terminal on the server yet.

!!! note "Gradescope"
    As you work, complete the **Lab 07** assignment on Gradescope. You don't submit the repo. You edit the files, try things in `ghci`, and type your answers (code and short explanations) into Gradescope. Each **Gradescope question** box below matches a question there.

!!! note "Solutions"
    The repo includes a `solutions/` folder with answers to every question. Give the lab your best shot on your own first. Look at the solutions after the lab, or once you've really run out of ideas. Getting stuck and working your way out is where most of the learning happens.

!!! question "Gradescope check: starter code"
    Confirm on Gradescope that you cloned the repo and that `ghci HigherOrderExercises.hs` says `Ok, one module loaded.`

---

## Part 1: From `map` to `>>=`

Load the first file:

```
ghci HigherOrderExercises.hs
```

After you edit the file, use `:reload` in `ghci`.

### Warmup: `map show`

!!! question "Gradescope question: `map show`"
    Before you run anything, write down what you think `map show [1, 2, 3]` evaluates to. Then check in `ghci`. Did anything about the output surprise you?

    Next, ask `ghci` for the type of `map show` alone (`:t map show`). `map` got only one of its two arguments. What kind of thing is `map show`, and what would you have to give it to get a result?

### Pointfree Style

The answer to that last question is the idea behind pointfree style. A function given only some of its arguments is still a function, so you can define a new function without ever naming its argument:

```haskell
increment :: Int -> Int
increment x = 1 + x

increment' :: Int -> Int
increment' = (1 +)      -- same function, no x
```

`(1 +)` is `+` with only its left argument filled in.

!!! question "Gradescope question: `double`"
    In `HigherOrderExercises.hs`, define `double` (multiply by 2) in pointfree style, reload, and try it.

    ```haskell
    double :: Int -> Int
    double = undefined -- <REPLACE WITH YOUR SOLUTION>
    ```

### Function Composition

Here's `plus2`, written three ways:

```haskell
plus2   x = increment (increment x)
plus2'  x = (increment . increment) x
plus2''   = increment . increment
```

The composition operator is defined as

```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
(.) g f x = g (f x)
```

Note the order: `g . f` runs `f` first.

!!! question "Gradescope question: `incrementDouble`"
    Using `(.)`, pointfree style, and functions already in the file, define a function that first adds one and then doubles. `incrementDouble 1` should give `4`.

    ```haskell
    incrementDouble :: Int -> Int
    incrementDouble = undefined -- <REPLACE WITH YOUR SOLUTION>
    ```

!!! question "Gradescope question: composing inside `map`"
    Using `(.)`, `map`, `show`, `(3 *)`, and the list `[1, 2, 3]`, write a `ghci` expression that produces `["3", "6", "9"]`.

### Functors

`map` applies a function to every element of a list. `fmap` does the same for any type that's a `Functor`, including `Maybe`:

```haskell
fmap double (Just 2)    -- Just 4
fmap double Nothing     -- Nothing
```

!!! question "Gradescope question: `f` with `fmap`"
    Given

    ```haskell
    onlyOdds :: Int -> Maybe Int
    onlyOdds i = if even i then Nothing else Just i
    ```

    use `fmap` and `double` to define `f`, which gives `Just (2 * n)` when `n` is odd and `Nothing` when `n` is even. Pointfree style is optional.

    ```haskell
    ghci> f 1
    Just 2
    ghci> f 2
    Nothing
    ghci> f 3
    Just 6
    ```

!!! question "Gradescope question: `Maybe`s inside a list"
    Write an expression that turns `[Just 1, Just 2, Just 3]` into `[Just "2", Just "4", Just "6"]`.

    *Hint:* there are two layers here, a list and a `Maybe` inside it. How many `map`s or `fmap`s does that suggest?

### Where Composition Breaks

The file defines two functions that each return a `Maybe`:

```haskell
-- minNum n is Just n if n is non-negative; otherwise it's Nothing
minNum :: Int -> Maybe Int
minNum i = if i < 0 then Nothing else Just i

-- maxNum n is Just n if n is less than 100; otherwise it's Just 100
maxNum :: Int -> Maybe Int
maxNum i = if i < 100 then Just i else Just 100
```

We want one function, `numLimits`, that caps a number at 100 and turns negative numbers into `Nothing`. The obvious idea is to run `maxNum` and then `minNum`.

!!! question "Gradescope question: two attempts that don't work"
    1. In `ghci`, try `numLimits = minNum . maxNum`. In a sentence, what is the type error complaining about?
    2. `fmap` let us apply a function to a value inside a `Maybe`, so try `fmap minNum . maxNum` instead. It compiles! What is its type (`:t`), and what does it give for `5`? Why is that still not what we want?

What we need is an operator that takes a `Maybe Int`, runs the next `Int -> Maybe Int` function on the value inside it (if there is one), and does *not* wrap the result a second time. That's bind:

```haskell
(>>=) :: Monad m => m a -> (a -> m b) -> m b
```

!!! question "Gradescope question: `numLimits`"
    Using `minNum`, `maxNum`, and `>>=`, define `numLimits`:

    ```haskell
    --    numLimits n =  Just n     if 0 <= n <= 100
    --                   Just 100   if n > 100
    --                   Nothing    otherwise
    numLimits :: Int -> Maybe Int
    numLimits n = undefined -- <REPLACE WITH YOUR SOLUTION>
    ```

    Test the boundaries with:

    ```haskell
    map numLimits [-1..1]
    map numLimits [99..101]
    ```

---

## Part 2: Motivating Monads

Using `>>=` on `Maybe` is handy, but it doesn't explain why Haskell builds a whole typeclass and special syntax around it. Part 2 shows why, using one program written three ways:

| File | How the program is written |
|---|---|
| `Program1.hs` | You pass the stack from each step to the next by hand. |
| `Program2.hs` | A homemade combinator, `followedBy`, passes the stack for you. |
| `Program3.hs` | Haskell's `Monad` instance and `do` notation do the same job. |

### The Stack-Based Calculator

The calculator keeps its arguments and results on a stack. Each operation takes a stack and returns a pair: `(result, newStack)`.

Open `Calculator.hs` and read it. Pay attention to:

- how the stack works (it should look familiar from [HW 3](../assignments/hw03.md)),
- the fact that every calculator operation returns a pair, and
- how `binaryOperation` works.

Then open `Program1.hs`. `program` runs six steps and names five intermediate stacks, `stack1` through `stack5`. `run program` should give `(70.0, [70.0])`.

!!! question "Gradescope question: break `Program1.hs`"
    In `program`, change the line `(_, stack4) = push 7 stack3` so it uses `stack2` instead of `stack3`. Before reloading, predict whether it will still compile. Then reload and `run program`.

    1. Did it compile? What did `run program` return?
    2. Why can't the type checker catch this mistake?

    Change it back when you're done.

### Is There a Better Way?

That bug happened because every step has to be handed the right stack by hand. Look at `binaryOperation`:

```haskell
binaryOperation f stack =
    let (right, stack1)  = pop stack
        (left,  stack2)  = pop stack1
        result           = f left right
        (_, stack3)      = push result stack2
    in (result, stack3)
```

What we *mean* is closer to:

```
right  <- pop
left   <- pop
push (f left right)
```

The idea is to write the stack-passing once, in a single **combinator**, and then never write it again. Open `Combinators.hs`. The important definition is `followedBy`:

```haskell
followedBy :: CalcStep -> (Value -> CalcStep) -> CalcStep
followedBy step function stack =
  let (firstValue, firstStack) = step stack
  in function firstValue firstStack
```

!!! question "Gradescope question: `followedBy`"
    1. Work out by hand what `` (pop `followedBy` push) [3, 4] `` returns. Show the intermediate `firstValue` and `firstStack`. Then check your answer in `ghci` (`ghci Combinators.hs`).
    2. Open `Program2.hs` and compare its `program` to the one in `Program1.hs`. Where did `stack1` through `stack5` go? Could you make the Part 1 bug in `Program2.hs`?

!!! question "Gradescope question: `tnpo`"
    In `Program2.hs`, implement a new operation `tnpo` that triples the value on top of the stack, adds 1, and pushes the result back on the stack. If `n` is on top before `tnpo`, then `3n+1` is on top after. Make `tnpo` the last operation `program` performs. Running the program should give `(211.0, [211.0])`.

    Challenge yourself to build `tnpo` using only existing calculator operations, not Haskell arithmetic.

### Monadic Calculators

Open `MonadicCalculator.hs` and compare it to `Calculator.hs`. A few things to know before you read:

- `CalcStep` is now a `newtype` that takes one type parameter, `CalcStep a`. A `Monad` instance has to be for a type with exactly one parameter. That parameter also means a calculator step could produce a `String`, a `Bool`, or anything else, not just a `Value`.
- There are `Functor` and `Applicative` instances, because every `Monad` must have them. You can skip those for now.
- Look at the `Monad CalcStep` instance and at the new `binaryOperation`.

!!! question "Gradescope question: `followedBy` and `>>=`"
    1. Here are the two types side by side:

        ```haskell
        followedBy :: CalcStep -> (Value -> CalcStep) -> CalcStep
        (>>=)      :: Monad m => m a -> (a -> m b) -> m b
        ```

        For the calculator, what plays the role of `m`, `a`, and `b`? Compare the body of `>>=` in the `Monad CalcStep` instance to `followedBy` in `Combinators.hs`. What's the same, and what's different?
    2. Open `Program3.hs` and compare `program` there to the one in `Program1.hs`. Then compare the `do`-notation `binaryOperation` in `MonadicCalculator.hs` to the original. Which version would you rather read and maintain, and why?

!!! example "Optional, if you have time"
    Port your `tnpo` from `Program2.hs` to `Program3.hs`. There's an optional Gradescope box for it.

---

## Where This Leaves Us

- `.` composes functions whose types line up.
- `fmap` applies a plain function to a value inside a box.
- `>>=` chains functions that each *return* a box. In the calculator, the box is a computation that carries a stack, which is why `do` notation can hide the stack completely.

That last pattern comes up whenever a computation carries some extra context: a value that might be missing, state that has to be passed from step to step, or a parse that might fail. In HW 7 you'll build it up yourself, starting from four versions of one small evaluator.

!!! tip "Checking your work"
    Now that you've finished, you can compare your answers with the [`solutions/` folder](https://github.com/hmc-cs-131-fa-2026/monad-lab/tree/main/solutions) in the repo. Its `README.md` has answers to the written questions, and the `.hs` files are complete, working versions you can load in `ghci` from inside that folder.

!!! question "Gradescope: wrap-up"
    Share any thoughts on this lab's format, plus any other comments or questions, directly on Gradescope.
