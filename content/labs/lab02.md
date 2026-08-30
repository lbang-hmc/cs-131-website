# Lab 2: GHCi Basics

This lab is your first real time in `ghci`, the interactive Haskell interpreter. There's no coding challenge to solve here — the point is just to get comfortable running Haskell, reading what it tells you, and building the habit of predicting an output *before* you run something and checking your prediction against reality. You'll be working with functions from Module 02.1 and 02.2, plus a few new ones (`filter`, `reverse`, `show`, `sort`) that behave a lot like `map` once you see the pattern.

!!! note "How you'll get set up"
    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a `ghci` prompt on the server yet. We're still finalizing the workflow for distributing starter files for this course — instructions will be posted here once that's ready.

## Getting Connected

Start by making sure you can reach the CS 131 programming server and get to a `ghci` prompt. Ask a grutor, the professor, or another student if you get stuck.

- [ ] I am able to access the server and run `ghci`.

## Sample Expressions, Part 1: `map`

Try evaluating each of these in `ghci`. For each one, note the result and, in your own words, write a sentence or two explaining what the code does.

```haskell
map (\x -> x / 2) [2.25, 3.5, 4.5, 7.2, 6.5]
```

```haskell
map (\x -> 2 / x) [2.25, 3.5, 4.5, 7.2, 6.5]
```

```haskell
map (/ 2) [2.25, 3.5, 4.5, 7.2, 6.5]
```

```haskell
map (2 /) [2.25, 3.5, 4.5, 7.2, 6.5]
```

!!! question "Think about it"
    Compare the notations `(\x -> x / 2)` and `(/ 2)`. What does `map` do? Have you seen something like `map` before?

## Sample Expressions, Part 2: `filter`, `reverse`, `show`

Same drill — try each, note the result, and explain what happened.

```haskell
filter (\x -> x > 5) [2.25, 3.5, 4.5, 7.2, 6.5]
filter (> 5) [2.25, 3.5, 4.5, 7.2, 6.5]
filter (> "Fun") ["C", "Fortran", "Haskell", "ML"]
```

!!! question "Think about it"
    In your own words, what does `filter` do?

```haskell
reverse [1,2,3,4,5]
reverse "Haskell"
```

```haskell
show 17
show [1,2,3,4]
```

!!! question "Think about it"
    In your own words, what does `show` do?

```haskell
reverse (show [1,2,3,4])
show (reverse [1,2,3,4])
```

Notice these two give different results even though they use the same two functions — think about why the order matters.

## Sample Expressions, Part 3: Lists and Strings

```haskell
[22..47]
take 15 [22..47]
drop 15 [22..47]
```

```haskell
1 : [2,3,4]
['h','e','l','l','o']
'h' : "ello"
```

```haskell
"Hello" ++ " " ++ "World"
[1,2,3,4] ++ [40,50,60,70]
[2,3,4] ++ [1]
```

!!! question "Think about it"
    What relationship do you notice between characters like `'h'`, `'e'`, `'l'`, `'o'`, strings like `"hello"`, and lists of integers like `[1,2,3]`? And what do you make of the `:` and `++` operators — how are they different from each other?

## Sample Expressions, Part 4: `Data.List`

A few useful functions — `partition` and `sort` — live in the `Data.List` module rather than the default Prelude, so you'll need to import it first:

```haskell
import Data.List
```

There's no output from an `import` — but something did change. What do you think happened?

```haskell
partition (> 5) [2.25, 3.5, 4.5, 7.2, 6.5]
partition (> "Fun") ["C", "Fortran", "Haskell", "ML"]
```

```haskell
sort [80, 38, 23, 40, 70, 24, 8, 92, 78, 80, 42, 19, 95, 87, 4]
sort "haskell = HASKELL"
```

!!! question "Think about it"
    What do you predict would happen if you ran `partition (> 5) [2.25, 3.5, 4.5, 7.2, 6.5]` *without* first running `import Data.List`? Quit `ghci` (`:quit` or Ctrl+D), restart it, and try it — read the error message carefully. What's your takeaway?

## Editing and Running Files on the Server

So far you've only typed expressions directly into `ghci`. Now try working from a file instead:

1. Connect to the server (e.g. via the VS Code remote extension).
2. `cd` into your `cs131` directory, and confirm with `pwd`.
3. Make a new directory for this lab and move into it: `mkdir lab2 && cd lab2`.
4. Create a file `lab2.hs` and add a few simple definitions to it, e.g.:

    ```haskell
    x = 1 + 2
    y = x + 3
    ```

    Save the file.
5. Navigate back into `lab2`, start `ghci`, and load your file:

    ```
    :load lab2.hs
    ```
6. Confirm the file does what you expect — check that `x` and `y` have the values you predicted, and try a computation like `x * 10`.

## Where This Leaves Us

You should now be comfortable getting to a `ghci` prompt, evaluating expressions, and loading your own files into it — the basic loop you'll use constantly for the rest of the course. Next up: [HW 2](../assignments/hw02.md), which has you writing real Haskell functions rather than just evaluating expressions.
