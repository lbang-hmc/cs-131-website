# ParserBase Reference

`ParserBase.hs` is the engine underneath the course's parser library. It defines the `Parser` type and the handful of primitives everything else is built from. The friendlier toolkit on top of it is covered in the [Parser Combinator Reference](parser-combinators.md).

**You almost never import `ParserBase` yourself.** `import ParserCombinators` already re-exports its essential pieces. This page is here for completeness: it lists what `ParserBase` provides, the few extras you'd need to import it directly for, and (if you're curious) how the parser type works under the hood. You don't need to understand its implementation, which uses some Haskell features we haven't covered.

!!! note "Credit"
    The `ParserBase` library and its original documentation were written by the HMC CS 131 staff (Melissa O'Neill, Chris Stone, Ben Wiedermann, and Lucas Bang). This page is adapted from that documentation.

## What `ParserCombinators` Already Gives You

These `ParserBase` names are re-exported by `ParserCombinators`, so a plain `import ParserCombinators` is enough to use them. Each is documented in the [Parser Combinator Reference](parser-combinators.md).

| Name | Think of the type as | What it does |
|---|---|---|
| `Parser a` | | A parser that produces a result of type `a` |
| `get` | `Parser Char` | Reads any single character |
| `pfail` | `Parser a` | Always fails |
| `parse` | `Parser a -> String -> a` | Runs a parser on a whole string |
| `parseFile` | `Parser a -> String -> IO a` | Runs a parser on the contents of a file |
| `<|>` | `Parser a -> Parser a -> Parser a` | Tries one parser, or else another |
| `many` | `Parser a -> Parser [a]` | Zero or more matches |
| `some` | `Parser a -> Parser [a]` | One or more matches |

## Extras That Need `import ParserBase`

`ParserCombinators` doesn't re-export these four, so to use them, import them from `ParserBase` alongside the usual import:

```haskell
import ParserCombinators
import ParserBase (eof, succeeding, (<||>), parseNamed)
```

### `eof`

```haskell
eof :: Parser ()
```

Succeeds (producing `()`) only if there is **no input left**. `parse` already requires a parser to consume its whole input, so you rarely need `eof` at the top level, but it can be handy in the middle of a larger parser.

```
ghci> parse (number <+-> eof) "42"
42
ghci> parse (get <+-> eof) "42"
*** Exception: <input>:1:2 -- EOF expected
```

### `succeeding`

```haskell
succeeding :: a -> Parser a -> Parser a
```

`succeeding x p` tries `p`. If `p` fails, it succeeds anyway, reads nothing, and produces the fallback value `x`.

```
ghci> parse (succeeding 0 number) "7"
7
ghci> parse (succeeding 0 number) ""
0
```

It behaves almost exactly like `p <|> return x`. The difference is that `succeeding` is *guaranteed* to succeed, which Haskell can take advantage of when parsing lazily.

### `<||>`

```haskell
(<||>) :: Parser a -> Parser a -> Parser a     -- infixl 3
```

Like `<|>`, it succeeds if either parser succeeds. The difference is in the error message when **both** fail: `<||>` always reports the error from the **second** parser, throwing away whatever the first one found. The `<??>` operator is built on it. See [How Errors Are Chosen](#how-errors-are-chosen) below for an example.

### `parseNamed`

```haskell
parseNamed :: Parser a -> String -> String -> a
```

`parseNamed p name input` is `parse` with a name of your choosing in error messages instead of `<input>`. (`parseFile` uses it to put the file name in its errors.)

```
ghci> parseNamed number "config.txt" "12x"
*** Exception: config.txt:1:3 -- Different kind of character expected
```

## Error Positions

Every error message has the form `name:line:column -- message`. Lines are numbered from 1.

!!! warning "Columns after the first line are off by one"
    On the first line of the input, columns are numbered from 1. After a newline, though, `get` resets the column to 0, so on every later line the column number is **one less** than you'd expect. For example, a problem at the second character of line 2 is reported as `2:1`.

## Under the Hood

Everything from here down is optional. It's useful context if you want to connect the library to the parsers you build yourself in Module 6.

### What a `Parser` Is

A `Parser` is a **function** wrapped in a type (the same idea as the parser functions you write by hand in class, with extra bookkeeping for error messages):

```haskell
type ParsePosn  = (Int, Int)            -- (line, column)
type ParseInput = (String, ParsePosn)   -- the remaining input, and where it starts
type ParseError = (String, ParsePosn)   -- an error message, and where it happened

newtype Parser a = ParsingFunction (ParseError -> ParseInput -> ParseResult a)

data ParseStatus a = Success a ParseInput
                   | Failure ParseError

type ParseResult a = (ParseError, ParseStatus a)
```

In words: a parser takes **the best error found so far** and **the input that's left to read**. It produces an updated best error, plus either `Success` (with a result and whatever input is left over) or `Failure` (with an error).

`newtype` works like `data` with exactly one constructor holding exactly one thing. It lets Haskell treat `Parser` as its own type, which is what allows it to belong to type classes like `Monad`.

### Where the Operations Come From

`ParserBase` makes `Parser` an instance of several standard Haskell type classes. Each instance supplies some of the operations you use, which is why their general types mention those classes:

| Instance | Provides | Used for |
|---|---|---|
| `Functor` | `fmap` | `>>=:` and `>>:` |
| `Applicative` | `pure`, `<*>` | `return`, and all the sequencing operators (`<+>`, `<+->`, ...) |
| `Monad` | `>>=` | "and then" |
| `MonadFail` | `fail` | failing with a message |
| `Alternative` | `empty`, `<|>`, `many`, `some` | choice and repetition |
| `MonadPlus` | `mzero`, `mplus` | `<=>` (via `mfilter`) and `perhaps` (via `join`) |

`ParserBase` also re-exports a few general-purpose Haskell functions that `ParserCombinators` is built from: `empty` (a parser that always fails, like `pfail`), `mfilter`, and `join`, along with the `Alternative` and `MonadPlus` classes themselves. You won't need them directly.

### How Errors Are Chosen

When a parse fails, many alternatives have usually failed along the way. Which one should the error message describe? `ParserBase`'s strategy is to report **the error that got deepest into the input**, on the theory that the parser that made the most progress is the one the author most likely meant.

That's what `<|>` does. `<||>` instead always reports the second parser's error. Here's the difference, with a parser that looks for `abc` or else `xx`, run on the input `abd`:

```haskell
abc = char 'a' <-+> char 'b' <+> char 'c'
xx  = char 'x' <+> char 'x'
```

```
ghci> parse (abc <|> xx) "abd"
*** Exception: <input>:1:3 -- Expected 'c'
ghci> parse (abc <||> xx) "abd"
*** Exception: <input>:1:1 -- Expected 'x'
```

`<|>` points at column 3, where `abc` got stuck, which is the useful answer. `<||>` reports that there's no `x` at the start, which is true but not very helpful.

### Backtracking

When the first parser in `p <|> q` fails, `q` starts over **from the same place `p` did**, no matter how much input `p` read before it failed. (Some parser libraries don't do this, and require you to mark the places where they should.) That means you can list alternatives that share a prefix without any special care:

```
ghci> parse ((string "ab" <+> string "c") <|> (string "a" <+> string "bd")) "abd"
("a","bd")
```

The trade-off is speed: a parser with many alternatives that share long prefixes can end up rereading the same input many times. For the languages in this course, that's never a problem.
