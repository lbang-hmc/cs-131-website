# HW 9: How `letrec` Works

!!! warning "This page has the answer"
    In [HW 9](hw09.md#letrec-an-optional-challenge), writing `letrec` is an optional challenge. If you'd like to work it out yourself, stop here and go back. If you'd rather not, that's fine too: copy the code below, then read the rest of the page to see why it works.

## The code

Replace the placeholder `evalLetrec` in `RaskEval.hs` with this:

```haskell
evalLetrec :: Env -> [SExpr] -> Value
evalLetrec env [SList [SList [SSymbol f, SList [SSymbol "lambda", SList params, fbody]]], body] =
    let closure = VClosure env' (map symbolName params) fbody
        env'    = Map.insert f closure env
    in  eval env' body
```

Then `./run-tests 03` should pass the two `letrec` tests, once Stages 1 and 2 are done.

The rest of this page explains it, a piece at a time.

## The pattern

The long pattern just says what a `letrec` looks like: one binding, of a name to a `lambda`, then the `letrec`'s own body. For

```racket
(letrec ((down (lambda (n) (if (= n 0) '() (cons n (down (- n 1)))))))
  (down 2))
```

the pattern binds:

- `f` to `"down"`, the name being bound
- `params` to the `SExpr`s for the parameters, here just `n`
- `fbody` to the `lambda`'s body, the `(if ...)` expression
- `body` to the `letrec`'s own body, `(down 2)`

`map symbolName params` turns the parameter `SExpr`s into the `[String]` that `VClosure` wants. Anything that doesn't fit the pattern, such as two bindings, or a name bound to a number, matches no equation, so it's an error automatically.

## The problem to solve

A closure is a `VClosure env params body`. It remembers the environment it was made in, and `apply` runs the body in **that** environment, extended with the parameters:

```haskell
apply (VClosure closureEnv params body) args = ... eval (envExtend params args closureEnv) body
```

So the question for `letrec` is: which environment should the closure for `down` remember?

**The outer environment doesn't work.** Suppose you wrote the obvious thing:

```haskell
evalLetrec env [...] =
    let closure = VClosure env (map symbolName params) fbody      -- remembers env
    in  eval (Map.insert f closure env) body
```

The `letrec`'s body can see `down`, so `(down 2)` starts running. But the closure remembers `env`, the environment **outside** the `letrec`, where `down` isn't bound. When the body reaches `(down (- n 1))`, it looks up `down` in that environment and fails with `unbound identifier: down`. That's exactly what `let` did.

**What it needs is an environment that contains the closure itself.** Call that environment `env'`. It must be `env` plus one more binding, `down ↦ closure`. And `closure` must be a `VClosure` that remembers `env'`. Each one needs the other:

- `closure` = a closure that remembers `env'`
- `env'` = `env`, plus `down` bound to `closure`

## Tying the knot

Those two bullets are exactly the two lines of the solution:

```haskell
let closure = VClosure env' (map symbolName params) fbody
    env'    = Map.insert f closure env
```

`closure` is defined using `env'`, and `env'` is defined using `closure`. This is called **tying the knot**: building a circular structure with two definitions that refer to each other.

In most languages this is nonsense, because to compute `closure` you'd need `env'` first, and to compute `env'` you'd need `closure` first. **In Haskell it works, because Haskell is lazy.** A definition isn't evaluated until something needs its value, and even then, only as much as is needed:

- Building `VClosure env' ...` doesn't look inside `env'`. It just stores a reference to it.
- `Map.insert f closure env` doesn't look inside `closure`. It just stores a reference to it, under the key `f`.

So neither definition has to finish before the other one starts. Each holds a reference to the other, and the result is a closure whose environment contains the closure. Nothing goes around the loop until `down` is actually called, and by then both values exist.

The last line, `eval env' body`, runs the `letrec`'s body in `env'`, so the body can call `down` too.

## A trace

Here's `(letrec ((down ...)) (down 2))`, step by step. Write `C` for the closure, and `env'` for `env` plus `down ↦ C`.

1. `evalLetrec` builds `C` and `env'`, then evaluates the body `(down 2)` in `env'`.
2. `(down 2)` is an application. Looking up `down` in `env'` gives `C`, and `2` gives `2`.
3. `apply C [2]` runs the `(if ...)` body in `C`'s environment, `env'`, extended with `n ↦ 2`.
4. `(= n 0)` is `#f`, so it evaluates `(cons n (down (- n 1)))`. Looking up `down` finds `C` in `env'`, **the same closure**. So it calls `apply C [1]`, in `env'` extended with `n ↦ 1`.
5. Again `(= n 0)` is `#f`, and the same lookup finds `C` again: `apply C [0]`.
6. Now `(= n 0)` is `#t`, so the result is `'()`.
7. Returning back up: `(cons 1 '())` is `(1)`, then `(cons 2 '(1))` is `(2 1)`.

Every recursive call finds `down` because every call runs in an extension of `env'`, and `env'` has `down` in it.

## The same trick elsewhere

**Library files.** The library loader in `Rask.hs` makes every `lambda` in a library able to call itself. It uses the same knot, written in one line:

```haskell
define env name (SList [SSymbol "lambda", SList params, body]) =
    let closure = VClosure (Map.insert name closure env) (map symbolName params) body
    in  closure
```

Here `closure` refers to itself directly, through the environment it remembers.

**Strict languages.** In a language like Python, where every definition is evaluated right away, you can't write two definitions that need each other. Real interpreters for strict languages do something else. HW 9's second "Think about it" question asks you to work out what goes wrong, and why mutation fixes it.

**The Y combinator.** In [Module 08.3](../modules/08.3-self-application-recursion-fixed-points.md), you got recursion with no names at all. The Y combinator makes a function receive *itself* as an argument, through self-application. `letrec` gets the same result a different way: instead of passing the function to itself, it puts the function in its own environment. An optional question in HW 9's Stage 3 has you try Y in Raskell.

[Back to HW 9, Stage 3](hw09.md#letrec-an-optional-challenge)
