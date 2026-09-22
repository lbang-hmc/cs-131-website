# Lab 4: Boolean Expressions

In this lab, you'll work with a small algebraic datatype, `BoolExpr`, that represents boolean expressions built out of literals (`T`/`F`) and `And`, `Or`, `Not`, and `Implies`. You'll complete an `eval` function that evaluates a `BoolExpr` down to a Haskell `Bool`, and a `prettyPrint` function that converts one to a readable `String` — the same evaluator/pretty-printer pattern you'll see again and again once you start building interpreters for bigger languages.

## Objectives

- Understand and use Haskell's algebraic datatypes.
- Implement functions that evaluate boolean expressions to Haskell `Bool` values.
- Implement a pretty-printer for boolean expressions.
- Build more comfort with functional-programming style generally.

!!! note "How you'll get the starter code"
    The starter code is a small public repository, [`hmc-cs-131-fa-2026/lab4`](https://github.com/hmc-cs-131-fa-2026/lab4), containing the `BoolExpr` datatype and partial `eval`/`prettyPrint` implementations for you to complete. On the course server, clone it directly — no need to make your own copy first:

    ```bash
    cd cs131
    git clone https://github.com/hmc-cs-131-fa-2026/lab4.git
    cd lab4
    ```

    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a terminal on the server yet.

!!! note "Gradescope"
    As you work, complete the corresponding **Lab 04** assignment on Gradescope.

    Most questions ask you to submit an expression, an implementation, or a predicted/actual result.

- [ ] I was able to get the starter code set up.

!!! question "Gradescope check: starter code"
    Confirm this on Gradescope.

## Expressions

Load the starter file and inspect the two provided example expressions:

```haskell
-- expr0 represents (T & F)
expr0 :: BoolExpr
expr0 = And T F

-- expr1 represents (T & F) | ~F
expr1 :: BoolExpr
expr1 = Or (And T F) (Not F)
```

Now define `expr2` and `expr3` yourself. `expr2` should represent `~ (T & F) | (T -> F)`:

```haskell
-- expr2 should represent ~ (T & F) | (T -> F)
expr2 :: BoolExpr
expr2 = undefined
```

```haskell
-- TODO: Create your own expression with each operator
expr3 :: BoolExpr
expr3 = undefined
```

!!! question "Gradescope: expr2 and expr3"
    Submit your definitions of `expr2` and `expr3`.

## Completing the `eval` Function

The starter code gives you `eval` for literals and `And`; fill in `Or`, `Not`, and `Implies`:

```haskell
-- evaluate a BoolExpr to result in a Haskell Bool
-- TODO: implement eval for Or, Not, and Implies
eval :: BoolExpr -> Bool
eval T = True
eval F = False
eval (And a b) = eval a && eval b
eval (Or a b) = undefined
eval (Not a) = undefined
eval (Implies a b) = undefined
```

!!! question "Gradescope: eval for Or, Not, Implies"
    Submit your implementations of `eval` for `Or`, `Not`, and `Implies`.

## Testing the `eval` Function

Make sure these all evaluate to what you expect:

```haskell
-- TODO: make sure these evaluate to the correct value
val0 = eval expr0
val1 = eval expr1
val2 = eval expr2
val3 = eval expr3
```

!!! question "Gradescope: eval results"
    What do you predict `val0` through `val3` should be, given how you defined `expr2` and `expr3`? Check your predictions in `ghci`, then submit each result.

## Implementing Pretty Printing

Complete `prettyPrint`, which converts a `BoolExpr` into its string representation. Again, the `And` and literal cases are provided:

```haskell
-- pretty print a bool expression
-- TODO: implement pretty printing for Or, Not, Implies
prettyPrint :: BoolExpr -> String
prettyPrint T = "T"
prettyPrint F = "F"
prettyPrint (And a b) = "(" ++ prettyPrint a ++ " & " ++ prettyPrint b ++ ")"
prettyPrint (Or a b) = undefined
prettyPrint (Not a) = undefined
prettyPrint (Implies a b) = undefined
```

!!! question "Gradescope: prettyPrint for Or, Not, Implies"
    Submit your implementations of `prettyPrint` for `Or`, `Not`, and `Implies`.

## Testing the `prettyPrint` Function

```haskell
-- make sure these convert to the correct strings
str0 = prettyPrint expr0
str1 = prettyPrint expr1
str2 = prettyPrint expr2
str3 = prettyPrint expr3
```

!!! question "Gradescope: prettyPrint results"
    What string do you expect `str0` through `str3` to produce? Check your predictions in `ghci`, then submit each result.

## Where This Leaves Us

`eval` and `prettyPrint` are both doing the same thing structurally — walking a `BoolExpr` tree and producing something different at each case — the same evaluator/pretty-printer pattern from Module 04.1 and 04.2, now applied to booleans instead of arithmetic. HW 4 asks you to build this same pattern again, for two little languages of your own.

!!! question "Gradescope: wrap-up"
    Leave any optional comments about the lab in the final Gradescope question, then move on to HW 4.

Next up: [HW 4](../assignments/hw04.md).
