# Lab 9: Exploring Raskell

[Module 09.1](../modules/09.1-from-lambda-calculus-to-s-expressions.md) introduced S-expressions, and [Module 09.2](../modules/09.2-building-a-small-lisp-interpreter.md) described how an interpreter for them is put together. In this lab, you meet the real thing: **Raskell**, a small Racket-like language whose interpreter is written in Haskell. You run it next to Racket, find where each stage of the interpreter lives, follow one program through it, and then add a feature yourself: the list operation `rest`. [HW 09](../assignments/hw09.md) grows this same interpreter into a language you can write real programs in.

## Objectives

- Run Raskell programs in the REPL and from files, and compare the results with Racket's.
- Find the parser, the syntax and value datatypes, the evaluator, and the REPL in the starter code.
- Trace one program through parsing, closure creation, and function application.
- Implement `rest`, and test it, including on inputs that should be errors.

!!! note "How you'll get the starter code"
    The starter code is a public repository, [`hmc-cs-131-fa-2026/raskell-lab`](https://github.com/hmc-cs-131-fa-2026/raskell-lab). On the course server, clone it directly. You don't need to make your own copy first:

    ```bash
    cd cs131
    git clone https://github.com/hmc-cs-131-fa-2026/raskell-lab.git
    cd raskell-lab
    ```

    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a terminal on the server yet.

!!! note "Gradescope"
    Answer the questions in the **Lab 09** assignment on Gradescope as you reach them, and upload your `RaskEval.hs` at the end. Lab credit is for completion, not correctness, but finish `rest`. HW 09 builds on it.

    Work on your own copy and submit individually. Talking problems over with the people around you is encouraged.

---

## Part 0: Start Raskell

From the `raskell-lab` folder, start the REPL:

```bash
./rask
```

The first time, `./rask` compiles the interpreter, which takes a few seconds. Then you get a `raskell>` prompt. Try:

```racket
((lambda (x) x) 'apple)
```

You should see `apple`. It's a **symbol value**, the data that `'apple` stands for. It's not a variable and not a quoted piece of syntax. Type `:q` to leave the REPL.

Raskell can also run a program stored in a file. The `examples/` folder has a few:

```bash
./rask --file examples/cat.rask
```

Finally, run the tests:

```bash
./run-tests
```

The tests in `00-baseline` should all pass. The ones in `01-rest` fail for now. Making them pass is Part 3.

!!! tip "Editing a program over several lines"
    In the REPL, an expression can span several lines. If you press Enter while a `(` is still open, Raskell shows a `...>` prompt and keeps reading. A `;` starts a comment, both in files and at the prompt.

---

## Part 1: Compare Racket with Raskell

Raskell is a **subset** of Racket, with a few small differences. Racket is installed on the course server, so you can check what a Racket-like expression *should* do. In a second terminal, start Racket:

```bash
racket
```

Evaluate each of these in **both** Racket and Raskell:

```racket
'(a b c)
(cons 'a '(b c))
((lambda (x) (cons x '())) 'apple)
```

You should see the same lists, with one difference in how they're printed. Racket's REPL puts a quote in front of a list or symbol result (`'(a b c)`), and Raskell doesn't (`(a b c)`). Leave Racket with `(exit)`.

Raskell doesn't do arithmetic or `if` yet. Try `(+ 1 2)` in both and see what happens. That isn't a bug in the starter. Arithmetic, conditionals, and more are what you add in the homework.

!!! question "Gradescope: Racket and Raskell"
    **Submit this response on Gradescope.**

    Paste what Racket printed and what Raskell printed for `(cons 'a '(b c))`. Then name one expression that works in Racket but that Raskell doesn't handle yet, and say what Raskell printed for it.

---

## Part 2: Find the stages of the interpreter

You won't write any code in this part. The goal is to get to know the interpreter you've been given. Being able to open someone else's language implementation, find its parts, and see how they fit together is a valuable skill. It's also what you need before you can add anything to it. In Part 3 you'll add a feature to this interpreter, and the homework is all about adding more. Time spent reading the code now will pay off in both.

Open the starter files in VS Code. Each one has one job:

| File | What it does |
| --- | --- |
| `RaskParser.hs` | Turns source text into an `SExpr`: the program's structure, before anything is evaluated. |
| `RaskAST.hs` | Defines `SExpr` and `Value` (what evaluating a program produces), plus printing and helpers for checking arguments. |
| `RaskEval.hs` | Evaluates an `SExpr` in an environment, producing either an error message or a `Value`. |
| `Rask.hs` | The REPL and the file runner. It reads input, calls the parser and the evaluator, and prints the result. |
| `ParserCombinators.hs`, `ParserBase.hs` | **PROVIDED: DO NOT EDIT.** The course's parser-combinator library, the same one you used for piq. You don't need to understand how these files are implemented. |

Skim `RaskAST.hs` first. Find the two datatypes, `SExpr` and `Value`, and notice that they're separate: one describes programs, the other describes results. Then open `RaskEval.hs` and find `eval`. Each equation handles one kind of expression.

`eval` takes an expression and returns its `Value`. When a Raskell program is wrong, the interpreter stops by calling Haskell's `error` with a message, such as `error "first: expected a nonempty list, got ()"`. Raskell catches it and prints `error: first: expected a nonempty list, got ()`, then keeps running.

Now follow this program through the interpreter:

```racket
((lambda (x) (cons x '())) 'cat)
```

In Haskell, the same program is

```haskell
(\x -> x : []) "cat"
```

It's an anonymous function that puts its argument in a one-element list, applied to `"cat"`. The result is `["cat"]`. The Raskell version produces `(cat)`. `cons` is Haskell's `:`.

The Haskell version is a slight cheat. Haskell has no built-in symbols, so we used the string `"cat"` in place of the symbol `'cat` just to give you something familiar. Symbols are a feature Racket and Raskell have and Haskell doesn't. A symbol is a name used as data: you can put it in a list and pass it around, and it never gets looked up as a variable.

The Raskell program is in `examples/cat.rask`. Work through these steps (with a partner, if you like). Line numbers refer to the starter files, before you've edited anything.

1. **Parse.** The parser turns the text into one `SExpr`:

    ```haskell
    SList
      [ SList                                -- the lambda expression
          [ SSymbol "lambda"
          , SList [SSymbol "x"]              -- parameter list
          , SList [ SSymbol "cons"           -- body: (cons x '())
                  , SSymbol "x"
                  , SList [SSymbol "quote", SList []] ] ]
      , SList [SSymbol "quote", SSymbol "cat"]   -- the argument 'cat
      ]
    ```

    - Notice that the parser has expanded both quotes: `'cat` became `(quote cat)` and `'()` became `(quote ())`.
    - To check this yourself, load `RaskParser.hs` in `ghci` and evaluate `parseRask "((lambda (x) (cons x '())) 'cat)"`.

2. **Evaluate the function.** Start at `eval` in `RaskEval.hs` (line 41). It has one equation for each kind of expression, and Haskell tries them in order.
    - The outer list doesn't start with `quote` or `lambda`, so it reaches the **application** equation (lines 61–62).
    - Line 62 evaluates the first element, `fexpr`, which is the `lambda` expression. (Ignore `forceValue` and `forceAll`. They only make sure Haskell, which is lazy, finishes computing the function and its arguments before the call.)
    - That call matches the `lambda` equation (line 55), which calls `evalLambda` (line 87).
    - The result is a `VClosure` (see the definition of `Value` in `RaskAST.hs`, lines 51–52). It holds three things:
        - the environment where the `lambda` was evaluated, which here is `initEnv` (just the primitives);
        - the parameter names, `["x"]`;
        - the body, still unevaluated: the `SExpr` for `(cons x '())`.

3. **Evaluate the argument.** Back in the application equation, line 62 also evaluates each argument expression, with `map (eval env) argexprs`.
    - Our only argument is `(quote cat)`. It matches the `quote` equation (line 54), which calls `evalQuote` (lines 80–81).
    - `evalQuote` hands the unevaluated `SExpr` to `quoteToValue` (`RaskAST.hs`, lines 85–89).
    - The symbol `cat` becomes the value `VSymbol "cat"`. Nothing is evaluated, so `cat` is never looked up as a variable.

4. **Apply.** Line 62 then calls `apply` with the closure from step 2 and the list of argument values from step 3.
    - A closure matches the `VClosure` equation (lines 67–71).
    - On line 71, `envExtend` (lines 28–29) binds the parameter names to the argument values.
    - It extends `closureEnv`, the environment stored in the closure, where the function was *made*, not the one where it's *called*. That's what makes Raskell's scope lexical.
    - The new environment is `initEnv` plus one binding: `x` ↦ `VSymbol "cat"`.

5. **Evaluate the body.** Line 71 then calls `eval` on the body, `(cons x '())`, in the extended environment. This is another ordinary application, so we're back on lines 61–62.
    - Evaluating the symbol `cons` looks it up (line 48) and finds the primitive that `initEnv` put there (lines 32–33).
    - Evaluating `x` looks it up too.
    - Evaluating `'()` goes through `evalQuote` again.
    - `apply` uses its `VPrim` equation (line 66), which calls `primCons` (lines 105–107).
    - Looking up `x` finds `VSymbol "cat"`, from the binding made in step 4.
    - `primCons` receives `[VSymbol "cat", VList []]` and returns `VList [VSymbol "cat"]`, which prints as `(cat)`.

!!! question "Gradescope: Tracing a program"
    **Submit this response on Gradescope.**

    In two to three sentences: why does the argument have to be `'cat` and not just `cat`? Try `((lambda (x) (cons x '())) cat)` in Raskell, and use what you saw in the trace to explain the error.

---

## Part 3: Implement `rest`

`first` already works: `(first '(a b c))` is `a`. Your job is its partner, `rest`, which returns everything *after* the first element:

| Expression | Result |
| --- | --- |
| `(rest '(a b c))` | `(b c)` |
| `(rest '(z))` | `()` |
| `(rest '(a (b c) d))` | `((b c) d)` |
| `(rest (cons 'a '(b c)))` | `(b c)` |
| `(rest '())` | an error |
| `(rest 'a)` | an error |

`rest` needs a **nonempty** list. Anything else is an error, and it should be a Raskell error message, not a Haskell crash.

In `RaskEval.hs`, find `primRest` (search for `TODO`). Right now it always gives the error `rest: not implemented yet`. Replace it with a real implementation.

Before you write anything, read `primFirst` just above it, closely. Like every primitive, it receives its arguments **already evaluated**, as a list of `Value`s. Its type is

```haskell
primRest :: [Value] -> Value
```

- Look at how `primFirst` is written as two equations. The first, `primFirst [xs]`, matches exactly one argument. The second matches anything else and reports the wrong number of arguments with `error`.
- `expectList` (in `RaskAST.hs`) returns the elements of a list value, or stops with an error if the value isn't a list.
- Think about the data: a nonempty list has a first element and the rest of the list. What should `rest` return for each?
- Your result has to be a `Value`. What constructor wraps a list of values?

You don't need to change the parser, `Value`, or `eval`. `rest` is already listed in the `primitives` table, so the evaluator can find it.

`./rask` recompiles automatically when you change a `.hs` file. If your code has a type error, you'll see GHC's message when you run `./rask` or `./run-tests`.

---

## Part 4: Test it

Run the tests for `rest`:

```bash
./run-tests 01
```

Each test is a small `.rask` file in `tests/01-rest/`. Its first line says what output it expects. A test that expects `error` passes for any Raskell error message. When a test fails, `run-tests` shows the program, what it expected, and what your interpreter printed.

Then run all the tests with `./run-tests`, to make sure `00-baseline` still passes.

Finally, write a test of your own. Make it an expression that uses `rest` **together with** another feature, such as a `lambda`, `cons`, `first`, or another `rest`. For example, write a function that returns the second element of a list. Run it in the REPL, or save it in a file and use `./rask --file`.

!!! question "Gradescope: Checking `rest`"
    **Submit these responses on Gradescope.**

    1. Do all the tests pass? If not, which ones still fail?
    2. Paste the expression you wrote, and what Raskell printed for it.
    3. In two to four sentences, explain how `(rest '(a b c))` becomes `(b c)`. Start from the source text and name the parts of the interpreter it passes through on the way.

!!! example "If you finish early - nothing to submit"
    - What happens if you evaluate `('a 'b)`, where the first element isn't a function? Find the line of `RaskEval.hs` that produces the message.
    - Compare `'(cons 'a '())` with `(cons 'a '())`. Why are the results different?
    - Look at how `apply` handles a `VPrim` and how it handles a `VClosure`. Why does only one of them call `eval`?

---

## Submitting

Make sure `./run-tests` compiles and runs, then upload your `RaskEval.hs` to **Lab 09** on Gradescope and answer the questions there.
