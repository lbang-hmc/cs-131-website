# Lab 4: Boolean Expressions

In this lab, you'll work with a small algebraic datatype, `BoolExpr`, that represents boolean expressions built out of literals (`T`/`F`) and `And`, `Or`, `Not`, and `Implies`. You'll complete an `eval` function that evaluates a `BoolExpr` down to a Haskell `Bool`, and a `prettyPrint` function that converts one to a readable `String` — the same evaluator/pretty-printer pattern you'll see again and again once you start building interpreters for bigger languages.

## Objectives

- Understand and use Haskell's algebraic datatypes.
- Implement functions that evaluate boolean expressions to Haskell `Bool` values.
- Implement a pretty-printer for boolean expressions.
- Build more comfort with functional-programming style generally.

!!! note "How you'll get the starter code"
    We're still finalizing the workflow for distributing starter code for this course. This lab was originally distributed as a small public repository containing the `BoolExpr` datatype and partial `eval`/`prettyPrint` implementations for you to complete — that setup will be posted here once it's ready. For now, this page covers what the lab asks of you.

- [ ] I was able to get the starter code set up.

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

Now define `expr2` and `expr3` yourself:

```haskell
-- TODO: Define expr2 as per instructions
expr2 :: BoolExpr
expr2 = undefined
```

```haskell
-- TODO: Create your own expression with each operator
expr3 :: BoolExpr
expr3 = undefined
```

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

## Testing the `eval` Function

Make sure these all evaluate to what you expect:

```haskell
-- TODO: make sure these evaluate to the correct value
val0 = eval expr0
val1 = eval expr1
val2 = eval expr2
val3 = eval expr3
```

!!! question "Try it"
    What do you predict `val0` through `val3` should be, given how you defined `expr2` and `expr3`? Check your predictions in `ghci`.

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

## Testing the `prettyPrint` Function

```haskell
-- make sure these convert to the correct strings
str0 = prettyPrint expr0
str1 = prettyPrint expr1
str2 = prettyPrint expr2
str3 = prettyPrint expr3
```

!!! question "Try it"
    What string do you expect `str0` through `str3` to produce? Check your predictions in `ghci`.

## Where This Leaves Us

`eval` and `prettyPrint` are both doing the same thing structurally — walking a `BoolExpr` tree and producing something different at each case — which is the core pattern behind interpreters and formatters alike, and one you'll meet again in Module 04.1 and 04.2. Next up: [HW 4](../assignments/hw04.md).
