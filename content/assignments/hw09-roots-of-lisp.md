# HW 9 Challenge: The Roots of Lisp

!!! note "Very ambitious, entirely optional, not graded"
    This challenge isn't part of HW 9. There's nothing to submit, and it doesn't affect your grade. Finish and submit HW 9 first. It's here for anyone who wants to keep going. ([Back to HW 9](hw09.md))

In 1960, John McCarthy showed that you can build a whole programming language from seven primitive operators and a way to write functions. He then wrote that language's `eval` **in the language itself**. Paul Graham's essay [*The Roots of Lisp*](https://paulgraham.com/rootsoflisp.html) walks through McCarthy's construction step by step, and ends with the complete evaluator on about one page. Read it first. Everything below assumes you have.

You can take the paper in either of two directions.

## Route A: Racket in Racket

`racket` is installed on the course server, and it already has every feature the paper's evaluator needs. Translate Graham's `eval.` and its helpers into Racket, then run his examples through it. Some translations you'll need:

- His `atom` is Racket's `(not (pair? x))`.
- His `eq` is Racket's `eq?`.
- His `defun` is Racket's `define`, and his `label` can be a `define` too.
- He writes `t` and `()` for true and false. You can keep them as data, or switch to `#t` and `#f`.

When it works, you have a Lisp interpreter written in a Lisp.

## Route B: A Lisp in Raskell

The more surprising route is to write McCarthy's evaluator **in Raskell**, a language you built, running on an interpreter you wrote. Then you have a Lisp running on Raskell, running on Haskell.

!!! implement "Implement (optional challenge): a Lisp in Raskell"
    Write Graham's evaluator as a Raskell library file, for example `rasklib/roots.rask`. Load it with `--lib`, and call your `eval` from the REPL or a program. Your first goal:

    ```racket
    (lisp-eval '(eq 'a 'a) '())        ; t
    ```

**What Raskell already has.** Almost everything:

| The paper uses | Raskell has |
| --- | --- |
| `quote`, `lambda`, `cond` | the same special forms |
| `car`, `cdr`, `cons` | `first`, `rest`, `cons` |
| `null.` | `empty?` |
| `and.`, `not.`, `append.`, `list.` | `and`, `not`, `append`, `list` |
| `defun`, `label` (recursion) | library definitions that call themselves, and `letrec` |

**What's missing: exactly two primitives.** Add them to your `RaskEval.hs`:

- **`eq?`**: are two values the same symbol? `eval` needs it to look up a variable name in the environment, and to recognize a form such as `(quote ...)` by its first symbol. Raskell's `=` compares only numbers.
- **`symbol?`**: is a value a symbol? `eval` needs it to tell a variable from a list. It can't simply try `first`, because `(first 'x)` is an error, and Raskell has no way to recover from one.

Each is two equations. Unlike every primitive you've written so far, these two must **never** fail on the wrong kind of value. `eval` asks `(eq? (first e) 'quote)` even when `(first e)` is a list, and it asks `symbol?` about everything. So the second equation of each gives `#f` for anything the first doesn't match.

Add them **after you submit**, or on a separate git branch, so that the `RaskEval.hs` you turn in is exactly the assignment. `rask-reference` doesn't have these two primitives, so for this challenge, your own interpreter is the only one that can run your code.

**The one snag: mutual recursion.** Graham's `eval.` calls `evcon.` (for `cond`) and `evlis.` (to evaluate arguments), and both of those call `eval.` back. But a Raskell library's definitions load in order, and each one can call only itself and the definitions above it. `letrec` binds only one name. You don't need a new Raskell feature to get around this. Think about where `eval` is already bound, and where `letrec` can go.

**Two smaller decisions:**

- **Booleans.** Your guest Lisp's `atom` and `eq` should return Graham's `t` and `()`, not Raskell's `#t` and `#f`. A one-line helper that converts one to the other keeps this tidy.
- **The `c...r` names.** Graham uses `cadr`, `caddr`, `caar`, `cadar`, and `caddar`. Define the ones you need, at the top of your library.

When your evaluator runs all of Graham's examples, including the `subst` function defined with `label`, you've done what McCarthy did, in a language you implemented yourself.

!!! question "Think about it (optional)"
    Graham's `eval` keeps variables in an association list, and it has no closures. A `lambda` is just a list, and its body is evaluated in whatever environment is current when it's called. Is its scope lexical or dynamic? Write a guest program whose answer would be different if you wrote the same program directly in Raskell.
