# Lab 6: A First Look at Parsing piq

This lab is about the course's **parser combinator library** — the same one HW6 asks you to build a real `piq` parser with. Today you'll run the library's pieces directly in `ghci`, combine them yourself, and then write a *small, deliberately restricted* slice of real `piq` parsing: just `direction`, and just `dot`/`square`/`circle` with a plain number, not a full expression. You'll also run a couple of **broken** parsers on purpose, so you're comfortable reading parser error messages before HW6 hands you the whole grammar.

**This is not a preview of the HW6 solution.** The file you edit today, `PiqWarmup.hs`, is a different, smaller file than HW6's `PiqParser.hs`, and the functions you write here (`wholeWord`, `miniStmt`) aren't the ones you'll write there (`keyword`, `stmt`). The *technique* carries over; the code doesn't.

## Objectives

- Run and combine parsers from the course's `ParserCombinators` library directly in `ghci`.
- Build small parsers out of smaller ones with `<|>`, `<+>`, `<+->`, `>>:`, and `>>=:`.
- Write a few of the easiest pieces of real `piq` syntax yourself, at a small, safe scale.
- Read a parser's error message carefully enough to tell *where it says the problem is* from *where the problem actually is*.

!!! note "How you'll get the starter code"
    The starter code is a small public repository, [`hmc-cs-131-fa-2026/piq-parsing-lab`](https://github.com/hmc-cs-131-fa-2026/piq-parsing-lab). On the course server, clone it directly — no need to make your own copy first:

    ```bash
    cd cs131
    git clone https://github.com/hmc-cs-131-fa-2026/piq-parsing-lab.git
    cd piq-parsing-lab
    ```

    **Run every command below from this `piq-parsing-lab` folder.**

    See [Connecting to the Server with VS Code](../how-to/connecting-with-vscode.md) if you haven't gotten to a terminal on the server yet.

!!! note "Gradescope"
    As you work, keep notes in `answers.md` — its headings match the Gradescope questions below. When you're done, paste your answers into the **Lab 06** assignment on Gradescope and upload `PiqWarmup.hs` where asked.

    Boxes labeled **Gradescope question** need a submitted answer. Boxes labeled **Try it** don't — they're there so you actually run the command, not just read it.

- [ ] I was able to clone the repo and load `PiqWarmup.hs` in `ghci` with no errors.

!!! question "Gradescope check: starter code"
    Confirm this on Gradescope.

For the full writeup of every combinator mentioned below, see the [Parser Combinator Reference](../how-to/parser-combinators.md) — this lab exercises exactly what's documented there, nothing more.

---

## Part 1: Warmup with the Parser Combinator Library

For most of this part, load the library directly:

```
ghci ParserCombinators.hs
```

and run commands of the form `parse someParser "some string"`.

### 1.1 Parsing a Single Digit

```
parse digit "4"
parse digit "x"
parse digit "42"
parse (many digit) "42"
```

Some of these produce an error — that's expected. Explain why.

!!! question "Gradescope: parsing digits"
    What happened for each of the four commands above? Based on them, what do `digit` and `many` do?

### 1.2 `many` vs. `some`

```
parse (many digit) "4279"
parse (many digit) "42"
parse (many digit) ""

parse (some digit) "4279"
parse (some digit) "42"
parse (some digit) ""
```

!!! question "Gradescope: many vs. some"
    Based on these results, what's the difference between `many` and `some`?

### 1.3 Building Your Own Parser

Define, directly in `ghci`:

```haskell
digits = some digit
```

then run:

```
parse digits ""
parse digits "4"
parse digits "42"
parse digits "4279"
```

!!! question "Gradescope: the digits parser"
    What happened for each of the four inputs?

### 1.4 More Parsers Already in the Library

!!! question "Gradescope: predict, then confirm"
    Without running these first, predict what happens. Then confirm in `ghci` and submit both your predictions and what actually happened.

    ```
    parse letter "c"
    parse letter "3"

    parse space " "
    parse space "b"

    parse (char 'x') "x"
    parse (char 'x') "y"
    ```

### 1.5 Combining Parsers: `<|>`, `<+>`, `<+->`

`alphanum` combines two parsers with `<|>`:

```haskell
alphanum :: Parser Char
alphanum = digit <|> letter
```

```
parse alphanum "3"
parse alphanum "x"
parse alphanum "3x"
parse alphanum "$"
```

!!! question "Gradescope: the <|> combinator"
    Based on these results, what does `<|>` do?

Now `<+>`:

```
parse (digit <+> digit) "42"
parse (digit <+> letter) "4x"
parse (letter <+> digit) "y2"
parse (letter <+> letter) "xy"

parse (many digit <+> many letter) "1234hello"
parse (many digit <+> many letter) "hello"

parse (many digit <+> space <+> many letter <+> space <+> many letter) "10 hello world"
```

!!! question "Gradescope: the <+> combinator"
    What does `<+>` accomplish? Based on the last result above, is `<+>` left- or right-associative?

And `<+->`:

```
parse (many digit <+-> space <+> many letter <+-> space <+> many letter) "10 hello world"
parse (many digit <+-> space <+> many letter <+-> (space <+> many letter)) "10 hello world"
```

!!! question "Gradescope: the <+-> combinator"
    What does `<+->` change about the result? Why do those last two commands give different results, even though they look almost identical?

### 1.6 Transforming Results with `>>:`

`>>:` replaces a successful parse with a fixed value:

```
parse (digit >>: "a digit") "4"
parse (letter >>: "a letter") "x"
```

!!! question "Gradescope: letter_or_digit and letter_then_digit"
    Define `letter_or_digit` so that `parse letter_or_digit "x"` gives `"a letter"` and `parse letter_or_digit "4"` gives `"a digit"`.

    Then define `letter_then_digit` so that `parse letter_then_digit "x1"` gives `("a letter","a digit")`.

    Submit both definitions.

### 1.7 Transforming Results with `>>=:`

`>>=:` applies a function to the result:

```
parse (some letter >>=: reverse) "hello"
```

!!! question "Gradescope: two_words_reverser"
    Define `two_words_reverser` so that `parse two_words_reverser "hello world"` gives `("olleh","dlrow")` (it should parse two words separated by a space and reverse each one).

    Then, using an anonymous function, write a parser expression so that `parse (some letter >>=: YOUR_FUNCTION) "hello"` gives `"hello!"`.

    Submit both.

---

## Part 2: Parsing piq, Carefully

Now switch to the lab's own file:

```
ghci PiqWarmup.hs
```

This part is scoped **deliberately small**. You're not writing a real `piq` parser today — you're writing a few of its easiest pieces, seeing a couple of realistic bugs, and getting comfortable with what a parse error actually tells you (and doesn't).

### 2.1 Why `text "dot"` Isn't Enough

```
parse textDot "dot"
parse textDot "dotty"
```

Read `textDot`'s comment in `PiqWarmup.hs` for what's really going on with the second one — it's not as simple as "it correctly rejected dotty." Then compare:

```
parse (wholeWord "dot") "dot"
parse (wholeWord "dot") "dotty"
```

!!! question "Gradescope: text vs. wholeWord"
    In your own words, why doesn't the `textDot "dotty"` exception mean `textDot` noticed the real problem? How is `wholeWord`'s failure different?

### 2.2 Finishing `direction`

`direction` only handles `"left"` so far:

```haskell
direction :: Parser Direction
direction = (wholeWord "left" >>: Lt)
```

**Add alternatives** for `"right"` (`Rt`), `"up"` (`Up`), and `"down"` (`Dn`), the same way, combined with `<|>`. Then test it:

```
parse direction "right"
parse direction "up"
parse direction "down"
parse direction "diagonal"
parse direction "LEFT"
parse direction ""
```

!!! question "Gradescope: finishing direction"
    Submit your finished `direction`. What happened for the three bad inputs? Read the actual error messages — don't just say "it failed."

### 2.3 Diagnosing `squareWrong`

`squareWrong` is provided, broken on purpose. **Don't fix it** — just run it and explain it:

```
parse squareWrong "square 10"
parse squareWrong "squareness 10"
```

!!! question "Gradescope: diagnosing squareWrong"
    What's actually wrong with `squareWrong`? Why is the error message for the second command misleading about where the real bug is? (Compare it to what you saw in 2.1.)

### 2.4 Finishing `miniStmt`

`miniStmt` only handles `"dot"` so far. **Add a `"square"` alternative** — read the keyword `"square"` correctly this time (not the `squareWrong` way), then a number, and build `Square (Num n)`. Then **add one more alternative yourself**, for `"circle"` (just the radius), building `Circle (Num n)`.

Test as you go:

```
parse miniStmt "dot"
parse miniStmt "square 10"
parse miniStmt "circle 3"
parse miniStmt "squareness 10"
```

!!! question "Gradescope: finishing miniStmt"
    Submit your finished `miniStmt`. Confirm that the last line now correctly fails — unlike `squareWrong`.

### 2.5 Trying It on Files

The `snippets/` folder has five tiny files. Try parsing each one:

```
parseMiniStmtsFile "snippets/ok1.piqmini"
parseMiniStmtsFile "snippets/ok2.piqmini"
parseMiniStmtsFile "snippets/bad1-wrong-case.piqmini"
parseMiniStmtsFile "snippets/bad2-missing-number.piqmini"
parseMiniStmtsFile "snippets/bad3-not-a-keyword.piqmini"
```

Two should succeed. Three should fail, each for a different reason.

!!! question "Gradescope: trying it on files"
    What did the two successful files produce? Give a one-sentence explanation for each of the three that failed.

---

## Reflection

!!! question "Gradescope: reflection"
    Answer each of the following in 2–4 sentences:

    1. Of all the error messages you saw today, which one was the most misleading about where the real bug actually was? Why?
    2. What's one thing you'll watch out for when you start HW6, because of something you saw in this lab?
    3. Anything else — thoughts on this lab format, or questions you still have?

---

## Where This Leaves Us

Today you wrote exactly two things: the rest of `direction`, and `dot`/`square`/`circle` with a plain number. That's it. Everything else — full expressions, assignments, loops, procedures, and whole programs — is still ahead of you. HW6 asks you to build the real thing, with the real grammar from top to bottom, starting from a stub even sparser than today's. The techniques are the same ones you just practiced: build small parsers, combine them with `<|>`/`<+>`/`<+->`, shape their results with `>>:`/`>>=:`, and read the error message carefully before trusting where it says the problem is.

!!! question "Gradescope: wrap-up"
    Leave any optional comments about the lab in the final Gradescope question, then move on to HW6.
