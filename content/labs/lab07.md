# Lab 7: From Higher-Order Functions to Monads

This lab is a staircase. You start somewhere very familiar: passing functions to other functions. About an hour later you'll be at monads. Each step exists because the step before it **hits a wall**: something plain function composition can't express. So as you go, watch for the moment each tool stops working. That moment is the reason the next tool exists.

[Module 7.1](../modules/07.1-functors-generalizing-map.md) and [Module 7.2](../modules/07.2-monads-composing-computations.md) gave you the ideas. In this lab you get to feel why they're needed.

## Objectives

- Write small functions in pointfree style and build bigger ones with composition `.`.
- Use `fmap` to apply a plain function to a value inside a box (a list, a `Maybe`).
- See exactly where `.` and `fmap` stop working, and use `>>=` to get past that point.
- Follow one stack-calculator program through three versions (manual plumbing, a homemade combinator, and Haskell's `Monad` with `do` notation) and recognize that the homemade combinator *is* `>>=`.

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
    As you work, complete the **Lab 07** assignment on Gradescope. You don't submit the repo. You edit the files, try things in `ghci`, and type your answers (code and short explanations) into Gradescope.

    Boxes labeled **Gradescope question** need a submitted answer. Boxes labeled **Try it** don't. They're there so you actually run the command, not just read it.

- [ ] I was able to clone the repo and load `HigherOrderExercises.hs` in `ghci` (`Ok, one module loaded.`).

!!! question "Gradescope check: starter code"
    Confirm this on Gradescope.

---

## Part 1: Higher-Order Operations

Load the first file:

```
ghci HigherOrderExercises.hs
```

Every exercise in Part 1 is **the same move**: gluing small functions together into bigger ones. What changes is how hard the gluing gets:

| Step | Tool | What it glues |
|---|---|---|
| 1 | HOFs and pointfree style | Functions are values you can pass around and name without mentioning their arguments. |
| 2 | Composition `.` | `a -> b` to `b -> c`. Easy, as long as the types line up. |
| 3 | Functors `fmap` | A plain function onto a value that's *inside a box* (a list, a `Maybe`). |
| 4 | Monads `>>=` | Functions that *produce* boxes, which is where `.` breaks. |

Keep that table in mind. By the end of Part 1 you'll have gone from `map show [1, 2, 3]` to the operator at the heart of every monad. After you edit the file, use `:reload` in `ghci`.

!!! tip "Move quickly through the warmups"
    The first few sections (HOF Warmup through Functors) are just quick reminders to set up the real work of the lab, which starts at **Monads** and continues through Part 2. Don't get hung up on them or spend too long. Go through them quickly, give short answers, and save your time for the monad sections.

### HOF Warmup

The jargon ("pointfree", "functors", "monads") sounds a bit scary, but all of it grows out of something you already know well: **higher-order functions (HOFs)**.

!!! question "Gradescope question: what is a HOF?"
    Give a short, intuitive definition of a higher-order function, based on your own current understanding.

### Higher-Order Functions

A higher-order function is a function that accepts another function as input, or returns another function as output. `map` is the classic example: its first argument is a function, which gets applied to each element of its second argument, a list.

!!! question "Gradescope question: `map show`"
    In `ghci`, run `map show [1, 2, 3]` and explain what you got.

### Pointfree Style

This function should look familiar:

```haskell
increment :: Int -> Int
increment x = 1 + x
```

In Haskell, we could also define it like this:

```haskell
increment = (1 +)
```

Instead of declaring and using the variable `x`, we leave it out. The parentheses around `1 +` tell Haskell that this expression is a function that takes a number and returns a number (by adding 1 to the input).

!!! question "Gradescope question: `double`"
    In `HigherOrderExercises.hs`, define `double` (which multiplies a number by 2) using pointfree style, reload, and try calling it.

    ```haskell
    double :: Int -> Int
    double = undefined -- <REPLACE WITH YOUR SOLUTION>
    ```

    Submit your definition.

### Function Composition

Pointfree style lets you name a function without naming its argument. Composition is what makes that useful, because now you can build new functions entirely out of old ones.

Here's one (non-pointfree) way to define a "plus 2" function:

```haskell
plus2 x = increment (increment x)
```

That definition composes two calls to `increment`. Composition is common enough that Haskell gives us an operator for it:

```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
(.) g f x = g (f x)
```

`(.)` takes two functions `g` and `f` and an input `x`. It calls `f` on `x`, then passes the result to `g`. So `plus2` can also be written as:

```haskell
plus2 x = (increment . increment) x   -- with composition
plus2   =  increment . increment      -- with composition, pointfree
```

!!! question "Gradescope question: `incrementDouble`"
    Using `(.)`, pointfree style, and functions already defined in the file, define a function that first adds one to its argument and then doubles the result. `incrementDouble 1` should give `4`.

    ```haskell
    incrementDouble :: Int -> Int
    incrementDouble = undefined -- <REPLACE WITH YOUR SOLUTION>
    ```

!!! question "Gradescope question: composing inside `map`"
    Composition and pointfree style shine when you need a quick function to hand to another function, like `map`. Using `(.)`, `map`, `show`, `(3 *)`, and the list `[1, 2, 3]`, write a `ghci` expression that produces `["3", "6", "9"]`.

### Functors

So far everything we've glued is plain `Int -> Int`. But real values often come wrapped: a list of results, a result that might be missing. `map` already handled the list case. `fmap` is the same idea for *any* box.

```haskell
fmap double (Just 2)    -- Just 4
```

That works because `Maybe` is a functor: a type that defines `fmap`. Try it in `ghci`!

!!! question "Gradescope question: `f` with `fmap`"
    Given

    ```haskell
    onlyOdds :: Int -> Maybe Int
    onlyOdds i = if even i then Nothing else Just i
    ```

    use `fmap` and `double` to define `f`, which gives `Just (2 * n)` when `n` is odd and `Nothing` when `n` is even. Pointfree style is your choice. Remember you're working with `Maybe`s, not lists!

    ```haskell
    ghci> f 1
    Just 2
    ghci> f 2
    Nothing
    ghci> f 3
    Just 6
    ```

!!! question "Gradescope question: boxes inside a list"
    Using functions defined and discussed in the file, write an expression that turns `[Just 1, Just 2, Just 3]` into `[Just "2", Just "4", Just "6"]`.

    *Hint:* an error mentioning "Non type-variable argument..." usually means you're mapping a function across a list of things that can't be passed to it.

### Monads

Now we'll take a first look at monads, specifically the bind operator `>>=`. Suppose we have:

```haskell
-- minNum n is Just n if n is non-negative; otherwise it's Nothing
minNum :: Int -> Maybe Int
minNum i = if i < 0 then Nothing else Just i

-- maxNum n is Just n if n is less than 100; otherwise it's Just 100
maxNum :: Int -> Maybe Int
maxNum i = if i < 100 then Just i else Just 100
```

We'd like one combined operation: numbers below 0 become `Nothing`, and numbers above 100 are capped at 100. Plain composition doesn't work:

```
ghci> numLimits = minNum . maxNum

<interactive>:25:22: error:
    • Couldn't match type ‘Maybe Int’ with ‘Int’
      Expected type: Int -> Int
        Actual type: Int -> Maybe Int
    • In the second argument of ‘(.)’, namely ‘maxNum’
```

**Read this error carefully.** It's the wall this whole lab has been climbing toward. `fmap` could reach *into* a box, but `maxNum` *produces* a box, and `minNum` wants a plain `Int`. Neither `.` nor `fmap` can bridge that gap. `>>=` exists to do exactly this:

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

Part 1 showed `>>=` as a neat trick on `Maybe`. Part 2 asks the real question: **why would anyone design a language feature around this?** You'll see one program written three ways, and it's the same staircase you just climbed:

| File | How the program is written |
|---|---|
| `Program1.hs` | All the plumbing is done by hand: you thread the stack through every step yourself. |
| `Program2.hs` | A homemade combinator, `followedBy`, does the plumbing for you. |
| `Program3.hs` | Haskell's built-in `Monad` and `do` notation. |

As you read each one, pay attention to what the *programmer* still has to think about, and what has disappeared.

### The Stack-Based Calculator

The calculator keeps its arguments and results on a stack. Given a stack, each operation (say, multiplication) produces a pair: `(result, stack')`.

Open `Calculator.hs` and read it. The key pieces are:

- **how the stack works** (it should look familiar from [HW 3](../assignments/hw03.md)),
- the fact that **every calculator operation returns a pair**, and
- **how `binaryOperation` works**.

Then open `Program1.hs` and read it carefully. What does the program do, and how?

!!! question "Gradescope question: `Program1.hs`"
    What do you like about this implementation? What don't you like?

### Is There a Better Way?

One annoying thing about the current implementation is that it's hard to describe a *sequence* of calculations. Look at `binaryOperation`:

```haskell
binaryOperation f stack =
    let (right, stack1)  = pop stack
        (left,  stack2)  = pop stack1
        result           = f left right
        (_, stack3)      = push result stack2
    in (result, stack3)
```

It would be nice to write something closer to:

```
right  = pop
left   = pop
result = f left right
push result
result
```

Comparing what we *want* to say with what we *currently* say:

- We're forced to pass the stack from one operation to the next explicitly (`pop stack1`, …).
- Sometimes we want the value an operation produces (after a `pop`), and sometimes we don't (after a `push`).

The fix is to separate the plumbing from the operations, and write one **combinator** that takes two arguments, a first operation and a second function. When the combinator is given an initial stack, it:

- runs the first operation to get a value and a new stack, then
- feeds that value and stack into the second function.

In other words, the combinator does all the work of passing results from one operation to the next.

!!! question "Gradescope question: `followedBy`"
    Open `Combinators.hs` and look at how these ideas become code. The most important piece is `followedBy`. Explain what you understand `followedBy` to be doing.

!!! question "Gradescope question: `Program2.hs` vs. `Program1.hs`"
    Open `Program2.hs` and compare it to `Program1.hs`. What's your opinion of how they compare?

!!! question "Gradescope question: `tnpo`"
    In `Program2.hs`, implement a new operation `tnpo` that triples the value on top of the stack, adds 1, and pushes the result back on the stack. If `n` is on top before `tnpo`, then `3n+1` is on top after. Make `tnpo` the last operation `program` performs. Running the program should give `(211.0, [211.0])`.

    Challenge yourself to build `tnpo` using only existing calculator operations, not Haskell arithmetic.

### Monadic Calculators

*This part is more about **reading** code than writing it.*

Here's the punchline: **`followedBy`, which you just worked out by hand, *is* `>>=`** (the monadic "bind", also called "and then"), specialized to the calculator. You didn't learn a new concept in Part 2. You rediscovered one. The `Monad` typeclass just gives the pattern a standard name, so every monad can share `do` notation and every library function written for monads.

Open `MonadicCalculator.hs` and compare it to `Calculator.hs`. Some things to notice:

- There's a new type, `CalcStep`, which is an instance of the `Monad` typeclass. Haskell requires a monad to take exactly one type parameter. So `CalcStep` takes one, which means monadic calculators can work over `String`s, `Bool`s, `Cow`s, and so on.
- The `Monad` instance for `CalcStep` closely mirrors `makeResult` and `followedBy` from `Combinators.hs`.
- To be a `Monad`, a type must also be a `Functor` and an `Applicative`, so those instances are there too. You can mostly ignore them for now.
- The rest looks a lot like the original code, but now we get `do` notation. Compare the monadic `binaryOperation` to the original!

!!! question "Gradescope question: `Program3.hs`"
    Open `Program3.hs` and compare it to `Program1.hs`. What do you notice? What do you like? What don't you like?

!!! example "Optional, if you have time"
    Port your `tnpo` from `Program2.hs` to `Program3.hs`. There's an optional Gradescope box for it.

---

## Where This Leaves Us

Look at how far you came: from `map show [1, 2, 3]` to defining your own monad instance. Every step was the same idea, *compose small pieces*, pushed through a harder situation:

- `.` composes functions whose types line up.
- `fmap` composes a plain function with a boxed value.
- `>>=` composes functions that produce boxes. In the calculator, the "box" is a computation that carries a stack. That's what lets you write a sequence of steps without writing out the plumbing.

You'll keep running into that last idea. Any time a computation carries some extra context (a value that might be missing, a state threaded through each step, a parse that might fail), a monad is how Haskell lets you sequence it cleanly.

!!! question "Gradescope: wrap-up"
    Share any thoughts on this lab's format, plus any other comments or questions, directly on Gradescope.
