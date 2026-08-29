# Lab 3: Tuples, Stacks, and Currying

This lab is entirely a `ghci` session — no files to edit, just you, the interpreter, and a handful of related problems on tuples, list-based stacks, and one of Haskell's more mind-bending features: currying. Each part gives you a few different correct implementations of the same idea and asks what you make of the differences — there's rarely a single "right answer" to those comparisons, we're just after your honest reaction.

!!! note "How you'll get set up"
    We're still finalizing the workflow for accessing the programming server for this course. Instructions will be posted here once they're ready — for now, this page covers what the lab actually asks you to do.

## Getting Connected

- [ ] I am able to get to the `ghci` prompt.

## Functions with Tuples

**Warmup with pairs.** Recall that Haskell pairs (two-element tuples) come with `fst` and `snd` to extract the first and second elements:

```haskell
fst (3, 4) -- 3
snd (3, 4) -- 4
```

Given this expression, work out what you predict the result to be *before* you run it:

```haskell
snd (snd (fst (((1,2),(3,4)),((5,6),(7,8)))))
```

Then check it in `ghci` — did you predict correctly?

**Swapping.** Define a function `swap` that accepts a pair and swaps the two positions:

```haskell
swap pair = (snd pair, fst pair)
```

Try it out on an input pair of your choosing.

Now consider an alternative definition, `swap'` ("swap prime" — note the trailing `'`, a common Haskell naming convention for "a variant of"):

```haskell
swap' (x, y) = (y, x)
```

Try this one too.

!!! question "Think about it"
    `swap` and `swap'` compute the same thing two different ways. What are your thoughts on the two implementations?

**Rotating.** Write a function `leftRotate3` that behaves like this:

```
Prelude> leftRotate3 (1, 2, 3)
(2, 3, 1)
```

That is: the element in position 1 moves to position 3, position 2 moves to position 1, and position 3 moves to position 2.

!!! question "Try it"
    How would you implement `leftRotate3` in `ghci`?

## Stacks via Lists

We'll think of a stack as a list of items, `[a]`, where the "top" of the stack is the front of the list.

**`isEmpty`** should evaluate to `True` if the stack is empty:

```haskell
isEmpty :: [a] -> Bool
```

Three correct ways to write it:

```haskell
isEmpty stack = if length stack == 0 then True else False
```

```haskell
isEmpty stack = length stack == 0
```

```haskell
isEmpty [] = True
isEmpty (x:xs) = False
```

!!! question "Think about it"
    All three are correct but take different approaches. What are the merits or drawbacks of each?

**`push`** takes an item `x :: a` and a stack `[a]`, and returns a new stack with `x` added to the top:

```haskell
push :: a -> [a] -> [a]
```

Two ways to write it — using the cons operator directly:

```haskell
push x stack = x : stack
```

...or observing that `push` *is* the cons operator, so just say so:

```haskell
push = (:)
```

!!! question "Think about it"
    Compare and contrast these two. What do you like or dislike about each? There's no correct answer — just looking for your honest reaction.

**`pop`** takes a stack and returns both the popped item and the updated stack:

```haskell
pop :: [a] -> (a, [a])
```

Three correct, but different, implementations:

```haskell
pop stack = (head stack, tail stack)
```

```haskell
pop [] = error "cannot pop empty stack!"
pop stack = let popped_element = head stack
                rest_of_stack = tail stack
            in
                (popped_element, rest_of_stack)
```

```haskell
pop [] = error "cannot pop empty stack!"
pop (x:xs) = (x, xs)
```

!!! question "Think about it"
    Same question as above — compare and contrast. What do you like or dislike about each?

## Currying and Uncurrying

**Currying.** Define a function `f` in `ghci`:

```haskell
f (x, y) = x + 2 * y
```

Try `f (4, 5)` and note the result.

Now create a new function from `f` using the built-in `curry`:

```haskell
g = curry f
```

Call `g 4 5` and note the result. Then check the type of `curry` itself:

```
:type curry
```

!!! question "Think about it"
    In light of `f (4, 5)`, `g = curry f`, `g 4 5`, and `:type curry` — explain in your own words what `curry` does.

One more: define `h = curry f 4`.

!!! question "Try it"
    Before running it, what do you expect `h 5` to evaluate to? Explain your reasoning, then check it.

**Uncurrying.** Now go the other direction. Define `g` in `ghci`:

```haskell
g x y = x + 2 * y
```

Try `g 4 5` and note the result. Then create `f` using `uncurry`:

```haskell
f = uncurry g
```

Call `f (4, 5)` and note the result, then check the type of `uncurry`:

```
:type uncurry
```

!!! question "Think about it"
    In light of `g 4 5`, `f = uncurry g`, `f (4, 5)`, and `:type uncurry` — explain in your own words what `uncurry` does.

## Where This Leaves Us

Currying is one of those ideas that clicks into place once you've played with it directly rather than just read the definition — the fact that `f (x, y)` and `g x y` are two shapes for "the same" function, convertible in either direction, comes up again and again in functional programming. Next up: [HW 3](../assignments/hw03.md), which builds on tuples, datatypes, and this kind of function manipulation.
