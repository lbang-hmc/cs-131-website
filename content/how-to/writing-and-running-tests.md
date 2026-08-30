# Writing and Running Tests

Every CS131 assignment ships with a set of tests you're expected to run against your own code, and you'll often add a few of your own. This guide covers both: the commands you'll run constantly, and — for when you want to understand what's actually going on, or need to write a new test from scratch — how Haskell's testing tools fit together.

## Quick Reference: Running Tests

Run these from the directory that contains the code under test (i.e., the code you're writing) — not from inside `ghci`.

Run **all the tests for an assignment**:

```bash
runhaskell -itest test/Spec.hs
```

Run **all the tests in a single file**:

```bash
runhaskell -itest test/<TestFile>.hs
```

For example, `runhaskell -itest test/FactSpec.hs`. You'll see both of these throughout the [assignments](../assignments/index.md) — some ask you to run a single spec file this way, others send you to `ghci` instead: load the spec file directly (`ghci test/FactSpec.hs`) and then run `main` at the prompt. Both approaches run the same tests; the difference is just whether you want to stay in an interactive session afterward.

## How It Fits Together

The rest of this guide builds up *why* those commands work, using a small running example — a `fact` (factorial) function. Some of the Haskell used below (`$`, `do`, `IO`) hasn't necessarily come up in the modules yet, but you don't need to understand it deeply to write and run tests — copying, pasting, and modifying an existing test is enough to get going.

### Modules

Suppose we write `fact` in a file `MyCode.hs`:

```haskell
fact :: Integer -> Integer
fact 0 = 1
fact n = n * fact (n - 1)
```

Loading it in `ghci` shows Haskell compiling it as a module called `Main` — every file gets a module automatically, even if you don't name one:

```
$ ghci MyCode.hs
[1 of 1] Compiling Main             ( MyCode.hs, interpreted )
Ok, one module loaded.
*MyCode>
```

To let *other* files (like our test files) `import` this code, we give it its own module name. In Haskell, a module's name has to match its file name:

```haskell
module MyCode where

fact :: Integer -> Integer
fact 0 = 1
fact n = n * fact (n - 1)
```

Now `ghci` reports the module as `MyCode` instead of `Main`, and `fact` still works exactly the same in the REPL — nothing else has changed.

### Test File Organization

Test code lives separately from the code under test, following a convention that lets Haskell's testing tools find your tests automatically:

- The file with the code under test (`MyCode.hs`) lives in the top-level directory.
- All test files live in a subdirectory called `test`.
- Each test file's name ends in `Spec.hs`.

So for our factorial code:

```
MyCode.hs
test/
    FactSpec.hs
```

### Writing a Test

Inside `test/FactSpec.hs`, a first unit test for `fact 0 = 1` looks like this:

```haskell
module FactSpec where

import MyCode           -- the code under test
import Test.Hspec       -- for unit testing

{- Testing fact -}
spec :: Spec
spec =
    describe "fact" $ do
        specify "fact 0 = 1" $
            fact 0 `shouldBe` 1

main :: IO ()
main = hspec spec
```

A few pieces worth naming:

- The module declaration (`module FactSpec where`) and the two imports — one for the code under test, one for [Hspec](https://hspec.github.io/), the testing library (already installed on the server).
- `spec :: Spec` is the test itself: a `describe` block naming what's being tested, containing one or more `specify` cases, each giving a description and an assertion (`shouldBe`).
- `main = hspec spec` runs the test using Hspec's own `hspec` function. (Some starter files use `context` in place of `describe` — they're interchangeable aliases in Hspec.)

To run it, load the spec file in `ghci` from the top-level directory (the one containing `MyCode.hs`) and call `main`:

```
$ ghci test/FactSpec.hs
[1 of 2] Compiling MyCode           ( MyCode.hs, interpreted )
[2 of 2] Compiling FactSpec         ( test/FactSpec.hs, interpreted )
Ok, two modules loaded.
*FactSpec> main

fact
    fact 0 = 1

Finished in 0.0010 seconds
1 example, 0 failures
```

Adding more cases just means more `specify` lines inside the same `describe` block; after editing the file, reload it in `ghci` (`:load test/FactSpec.hs`) and run `main` again to see the updated results.

### Property-Based Testing

Unit tests check one input/output pair at a time. **Property-based testing** goes further: instead of listing example cases, you describe a *property* the function should always satisfy, and the [QuickCheck](https://hspec.github.io/writing-specs.html) library generates a batch of test inputs to check it against.

Say `MyCode.hs` adds:

```haskell
mySuccessor :: Integer -> Integer
mySuccessor n = succ n
```

`test/SuccessorSpec.hs` can test both the specific case and the general property:

```haskell
module SuccessorSpec where

import MyCode           -- the code under test
import Test.Hspec       -- for unit testing
import Test.QuickCheck  -- for property-based testing

{- Testing mySuccessor -}
spec :: Spec
spec =
    describe "MyCode.mySuccessor" $ do
        -- Unit testing: test one input/output pair for this function
        specify "mySuccessor 0 = 1" $
            mySuccessor 0 `shouldBe` 1

        -- Property-based testing: generate input/output pairs according
        -- to a specification
        specify "mySuccessor n = n + 1" $ property $
            \n -> mySuccessor n == n + 1

main :: IO ()
main = hspec spec
```

The second `specify` reads as "for all `n`, `mySuccessor n` equals `n + 1`." Running it shows QuickCheck generating a batch of inputs (100 by default) and checking the property against each one:

```
*SuccessorSpec> main
MyCode.mySuccessor
   mySuccessor 0 = 1
   mySuccessor n = n + 1
         +++ OK, passed 100 tests.

Finished in 0.0077 seconds
2 examples, 0 failures
```

### Running Everything at Once

As a project grows, re-running each spec file by hand gets old. Hspec's **automated test discovery** finds every `*Spec.hs` file in `test/` and combines them into one suite, as long as:

- Every test file lives in `test/` and ends in `Spec.hs`.
- Each one defines `spec :: Spec`.
- A file `test/Spec.hs` exists containing exactly this line:

    ```haskell
    {-# OPTIONS_GHC -F -pgmF hspec-discover #-}
    ```

- You load it with the `-itest` flag, which tells Haskell where to find the other test files:

    ```
    $ ghci -itest test/Spec.hs
    [1 of 4] Compiling MyCode           ( MyCode.hs, interpreted )
    [2 of 4] Compiling FactSpec         ( test/FactSpec.hs, interpreted )
    [3 of 4] Compiling SuccessorSpec    ( test/SuccessorSpec.hs, interpreted )
    [4 of 4] Compiling Main             ( test/Spec.hs, interpreted )
    Ok, four modules loaded.
    *Main> main
    ```

This is exactly what the `runhaskell -itest test/Spec.hs` shortcut at the top of this page runs for you in one step, without needing to open `ghci` at all — which is why most assignments just ask you to run that one command to check everything at once.

---

Ready to put this to use? Most [assignments](../assignments/index.md) include a `**Testing:**` note telling you exactly which command to run and which file to add your own tests to.
