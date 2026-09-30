# Parser Combinator Reference

Starting in Module 6, you'll write parsers by gluing together small parsers with **parser combinators**. The course's combinator library lives in two files that ship with every parsing lab and assignment: `ParserBase.hs`, which holds the core machinery, and `ParserCombinators.hs`, which builds a toolkit on top of it. You'll only ever need one line to use the library (the [ParserBase Reference](parser-base.md) covers the engine underneath, if you're curious):

```haskell
import ParserCombinators
```

This page covers everything that import gives you, grouped by what you'd use it for. Keep it open while you work. You don't need to memorize it, and you **don't need to understand how the library is implemented**: several definitions are written in a terse, library-heavy style that doesn't look like what we write in class.

!!! note "Credit"
    The `ParserCombinators` library and its original documentation were written by the HMC CS 131 staff (Melissa O'Neill, Chris Stone, Ben Wiedermann, and Lucas Bang). This page is adapted from that documentation.

## Reading the Types

Many of the library's functions have more general types than the ones we use in class. For example, if you ask `ghci` for the type of `<|>`, you get:

```haskell
(<|>) :: Alternative f => f a -> f a -> f a
```

That's because the library reuses general Haskell features (the `Functor`, `Applicative`, `Alternative`, and `Monad` type classes) that `Parser` belongs to. **Everywhere you see a type variable like `f`, `m`, `p`, or `parser`, read it as `Parser`**:

```haskell
(<|>) :: Parser a -> Parser a -> Parser a
```

This page always gives the "think of it as" version with `Parser` filled in.

## At a Glance

| You want to... | Use |
|---|---|
| Run a parser on a string or file | `parse`, `parseFile` |
| Read one character (any, or of a certain kind) | `get`, `char`, `digit`, `letter`, `alphanum`, `space`, `getCharThat` |
| Match an exact string | `string`, `text` |
| Match a punctuation character, skipping whitespace first | `sym`, `openparen`, `closeparen`, `openbrace`, `closebrace` |
| Parse a name or a number | `ident`, `identifier`, `num`, `number`, `double` |
| Do one parser, then another | `<+>`, `<+->`, `<-+>`, `<-+->`, `<:>`, `<++>`, `>>=` |
| Try one parser, or else another | `<|>` |
| Change what a parser returns | `>>=:`, `>>:` |
| Keep a result only if it passes a test | `<=>` |
| Repeat a parser | `many`, `some`, `many1`, `skipMany`, `skipMany1` |
| Parse something that might not be there | `optional`, `perhaps` |
| Parse something inside delimiters | `parens`, `braces`, `between` |
| Parse a list with separators or terminators | `sepBy`, `sepBy1`, `endBy`, `endBy1` |
| Parse operators like `1 - 2 - 3` | `chainl1`, `chainr1` |
| Deal with whitespace | `whitespace`, `skipws` |
| Give better error messages | `<??>`, `<???>` |
| Always succeed or always fail | `return`, `pfail`, `fail` |

!!! note "How do you even say `<-+->` out loud?"
    This library is mostly punctuation: `<+->`, `<??>`, `>>=:`, `<=>`... Most of us type characters like these all the time without ever learning what to call them, which makes pair programming (or asking a question in office hours) surprisingly awkward. Is `<` "less than," "left angle bracket," or something else entirely? Programmers settled the matter long ago, in verse: read [Waka Waka Bang Splat](https://spot.colorado.edu/~sniderc/poetry/wakawaka.html). It only works if you read it aloud.

All of the examples below are real `ghci` sessions. When a parse fails, `ghci` also prints a few lines of `CallStack` after the error; those are left out here.

## The `Parser` Type

```haskell
data Parser a
```

A `Parser a` is something that can read an input string and, if it succeeds, produce a result of type `a`. A `Parser Char` produces a character, a `Parser Integer` produces a number, a `Parser Expr` might produce a whole abstract syntax tree.

## Running a Parser

```haskell
parse     :: Parser a -> String -> a
parseFile :: Parser a -> String -> IO a
```

`parse p input` runs the parser `p` on `input` and returns the result. The parser has to match **the entire input**. Leftover characters count as an error:

```
ghci> parse number "42"
42
ghci> parse number "12 34"
*** Exception: <input>:1:3 -- Different kind of character expected
```

`parseFile p path` does the same thing, but reads the input from the file at `path`. Because it reads a file, its result is wrapped in `IO`.

Error messages point at the problem as `line:column` (column 3 above is the space before `34`).

## Primitive Parsers

These are the building blocks everything else is made from.

```haskell
get :: Parser Char
```

Reads a single character, whatever it is. Fails only if there's no input left.

```
ghci> parse get "x"
'x'
ghci> parse get ""
*** Exception: <input>:1:1 -- Unexpected EOF
```

```haskell
return :: a -> Parser a
```

Always succeeds, reads nothing, and produces the value you give it. It's handy as a "base case," e.g., "if nothing else matched, produce `[]`."

```haskell
pfail :: Parser a
fail  :: String -> Parser a
```

Parsers that always fail. `fail` lets you choose the error message.

```
ghci> parse (fail "nope" :: Parser Int) "abc"
*** Exception: <input>:1:1 -- nope
```

## Sequencing: This, Then That

Each of these runs parser `p` on the input, then runs `q` on **whatever `p` left over**. If either one fails, the whole thing fails. What differs is what they produce, and the shape of the operator tells you which result it keeps: the `+` marks the result you keep and the `-` marks the one you throw away.

| Combinator | Think of the type as | Produces |
|---|---|---|
| `p <+> q` | `Parser a -> Parser b -> Parser (a, b)` | both results, as a pair |
| `p <+-> q` | `Parser a -> Parser b -> Parser a` | only `p`'s result |
| `p <-+> q` | `Parser a -> Parser b -> Parser b` | only `q`'s result |
| `p <-+-> q` | `Parser a -> Parser b -> Parser ()` | neither (just `()`) |
| `p <:> q` | `Parser a -> Parser [a] -> Parser [a]` | `p`'s result consed onto `q`'s list |
| `p <++> q` | `Parser [a] -> Parser [a] -> Parser [a]` | the two lists appended |

```
ghci> parse (get <+> get) "ab"
('a','b')
ghci> parse (get <+-> get) "ab"
'a'
ghci> parse (get <-+> get) "ab"
'b'
ghci> parse (get <-+-> get) "ab"
()
ghci> parse (digit <:> many letter) "1abc"
"1abc"
ghci> parse (string "ab" <++> string "cd") "abcd"
"abcd"
```

The "keep one side" versions are what you'll use to throw away punctuation. For example, `char '(' <-+> number <+-> char ')'` parses a parenthesized number and keeps just the number.

### And Then: `>>=`

```haskell
(>>=) :: Parser a -> (a -> Parser b) -> Parser b
```

The "and then" (or **bind**) operator. `p >>= f` runs `p`, hands its result to `f`, and then runs **the parser `f` returns**. Unlike the sequencing operators above, it lets the second parser depend on what the first one found. Here, the second parser looks for the same character that the first one read:

```
ghci> parse (get >>= \c -> char c) "zz"
'z'
ghci> parse (get >>= \c -> char c) "zy"
*** Exception: <input>:1:2 -- Expected 'z'
```

## Alternatives: This, or Else That

```haskell
(<|>) :: Parser a -> Parser a -> Parser a
```

`p <|> q` succeeds if either `p` or `q` succeeds. Both sides have to produce the same type.

```
ghci> parse (many (letter <|> digit)) "a1b2"
"a1b2"
```

## Transforming Results

```haskell
(>>=:) :: Parser a -> (a -> b) -> Parser b
(>>:)  :: Parser a -> b -> Parser b
```

`p >>=: f` runs `p` and passes its result through the ordinary function `f`. `p >>: v` runs `p`, ignores its result, and produces `v` instead. These are how you turn raw text into the values (and eventually AST nodes) you actually want.

```
ghci> parse (num >>=: (*2)) "21"
42
ghci> parse (text "yes" >>: True) "  yes"
True
```

`>>=:` pairs naturally with `<+>`: parse two things, then combine the pair with a lambda. That's exactly how the library defines `ident`:

```haskell
ident = letter <+> many alphanum  >>=: \(l, ls) -> l:ls
```

## Filtering Results

```haskell
(<=>) :: Parser a -> (a -> Bool) -> Parser a
```

`p <=> pred` runs `p` and keeps the result only if it satisfies `pred`. Otherwise it fails.

```
ghci> parse (get <=> (== 'x')) "x"
'x'
ghci> parse (get <=> (== 'x')) "y"
*** Exception: <input>:1:2 -- No parse (via pfail)
```

That error message isn't very helpful, which is why the library also provides `char`, below.

## Single Characters

```haskell
getCharThat :: (Char -> Bool) -> Parser Char
digit       :: Parser Char
letter      :: Parser Char
alphanum    :: Parser Char
space       :: Parser Char
char        :: Char -> Parser Char
```

| Parser | Reads one character that is... |
|---|---|
| `getCharThat pred` | anything satisfying `pred` |
| `digit` | a digit, `0`–`9` |
| `letter` | a letter, upper- or lowercase |
| `alphanum` | a letter or a digit |
| `space` | whitespace (space, tab, newline, etc.) |
| `char c` | exactly `c` |

```
ghci> parse (some (getCharThat (`elem` "aeiou"))) "aei"
"aei"
ghci> parse (char 'x') "y"
*** Exception: <input>:1:1 -- Expected 'x'
```

Compare that last error with the `get <=> (== 'x')` version in the previous section. `char` does the same job but adds a clearer message.

## Strings

```haskell
string    :: String -> Parser String
text      :: String -> Parser String
litstring :: Parser String
```

`string s` matches exactly the characters of `s`, next in the input. `text s` does the same but **skips any whitespace before it** first.

```
ghci> parse (string "hello") "hello"
"hello"
ghci> parse (text "hello") "   hello"
"hello"
```

`litstring` parses a double-quoted string literal (skipping any whitespace before it) and produces what's between the quotes:

```
ghci> parse litstring "  \"hello world\""
"hello world"
```

!!! warning "No escaped quotes"
    The library's documentation says `litstring` understands the escape `\"` for a quote inside the string, but it doesn't: the backslash is read as an ordinary character, and the quote right after it ends the string. Stick to string literals without embedded quotes. (`stringchar :: Parser Char`, the one-character helper `litstring` is built from, is also exported, and has the same limitation.)

## Symbols and Delimiters

```haskell
sym        :: Char -> Parser Char
openparen  :: Parser Char
closeparen :: Parser Char
openbrace  :: Parser Char
closebrace :: Parser Char
parens     :: Parser a -> Parser a
braces     :: Parser a -> Parser a
between    :: Parser open -> Parser close -> Parser a -> Parser a
```

`sym c` is like `char c`, but it skips whitespace before the character. `openparen`, `closeparen`, `openbrace`, and `closebrace` are just `sym '('`, `sym ')'`, `sym '{'`, and `sym '}'`.

`parens p` parses a `p` wrapped in parentheses and keeps only `p`'s result. `braces p` does the same with curly braces. Both skip whitespace before each delimiter.

```
ghci> parse (parens number) "( 42 )"
42
ghci> parse (braces (identifier `sepBy` sym ',')) "{a, b, c}"
["a","b","c"]
```

`between open close p` is the general version, for whatever delimiters you like. Note the argument order: **the delimiters come first**, then the thing inside them.

```
ghci> parse (between (char '<') (char '>') ident) "<tag>"
"tag"
```

## Whitespace

```haskell
whitespace :: Parser ()
skipws     :: Parser a -> Parser a
```

`whitespace` consumes zero or more whitespace characters and produces `()`. `skipws p` skips any leading whitespace, then runs `p`.

```
ghci> parse (whitespace <-+> get) "   z"
'z'
```

!!! tip "Leading vs. trailing whitespace"
    The library's convention is to skip whitespace **before** each token, never after. That's why `text`, `sym`, `identifier`, `number`, and friends all skip leading whitespace. If your input might end with trailing spaces or a newline, finish your top-level parser with `<+-> whitespace` so that `parse` doesn't complain about leftover input.

## Identifiers and Numbers

```haskell
ident      :: Parser String
identifier :: Parser String
num        :: Parser Integer
number     :: Parser Integer
double     :: Parser Double
```

`ident` parses an identifier: a letter followed by zero or more letters and digits. `num` parses an integer, with an optional leading `-`. `identifier` and `number` are the same, but skip leading whitespace first. **Most of the time, you want the whitespace-skipping versions.**

`double` parses a decimal number, including scientific notation (like `3.14e2`), skipping leading whitespace.

```
ghci> parse ident "x42"
"x42"
ghci> parse identifier "   foo7"
"foo7"
ghci> parse ident "42x"
*** Exception: <input>:1:1 -- <ident> expected
ghci> parse number "  -17"
-17
ghci> parse double " 3.14e2"
314.0
```

## Repetition

```haskell
many      :: Parser a -> Parser [a]
some      :: Parser a -> Parser [a]
many1     :: Parser a -> Parser [a]
skipMany  :: Parser a -> Parser ()
skipMany1 :: Parser a -> Parser ()
```

`many p` matches `p` **zero or more** times and produces a list of the results. `some p` matches it **one or more** times. `many1` is just another name for `some`. `skipMany` and `skipMany1` are the same as `many` and `some`, but throw the results away.

```
ghci> parse (many digit) ""
""
ghci> parse (some digit) ""
*** Exception: <input>:1:1 -- Different kind of character expected
ghci> parse (skipMany (char 'a') <-+> get) "aaab"
'b'
```

!!! warning "`many` never fails"
    Because zero matches is fine, `many p` always succeeds. That makes it easy to write a parser that quietly matches nothing when you expected it to match something. If there has to be at least one, use `some`.

## Optional Pieces

```haskell
optional :: Parser a -> Parser (Maybe a)
optional :: Parser a -> Parser [a]
perhaps  :: Parser [a] -> Parser [a]
```

`optional p` tries to parse a `p`, but still succeeds if there isn't one. It can produce its result as either a `Maybe` or a list, whichever your code needs; Haskell works out which from the context:

```
ghci> parse (optional (char '-')) "" :: Maybe Char
Nothing
ghci> parse (optional (char '-')) "-" :: String
"-"
```

`perhaps p` is for parsers whose result already has an "empty" value, like a `String` (`""`), a list (`[]`), or a `Maybe` (`Nothing`). If `p` doesn't match, `perhaps p` produces that empty value.

```
ghci> parse (perhaps (string "abc")) ""
""
```

## Lists with Separators

```haskell
sepBy  :: Parser a -> Parser sep -> Parser [a]
sepBy1 :: Parser a -> Parser sep -> Parser [a]
endBy  :: Parser a -> Parser sep -> Parser [a]
endBy1 :: Parser a -> Parser sep -> Parser [a]
```

``p `sepBy` sep`` parses zero or more `p`s with a `sep` **between** each pair, like `1, 2, 3`. `endBy` is similar, but with a `sep` **after every** `p`, like `1; 2;`. In both cases the separators are thrown away. The `1` versions require at least one `p`.

```
ghci> parse (number `sepBy` sym ',') "1, 2 ,3"
[1,2,3]
ghci> parse (number `sepBy` sym ',') ""
[]
ghci> parse (number `endBy` sym ';') "1; 2;"
[1,2]
```

The library also has `manyEndingWith end p` and `someEndingWith end p`, which read `p`s until they reach an `end`. In practice, `many p <+-> end` does the same job, so you shouldn't need them.

## Chains of Operators

```haskell
chainl1 :: Parser a -> Parser (a -> a -> a) -> Parser a
chainr1 :: Parser a -> Parser (a -> a -> a) -> Parser a
```

`chainl1 p op` parses one or more `p`s separated by `op`s, where each `op` produces **a function that combines two results**. It then combines them, grouping from the left, like `foldl`. `chainr1` does the same, but groups from the right, like `foldr`. The difference matters for operators like subtraction:

```
ghci> parse (chainl1 number (sym '-' >>: (-))) "10 - 3 - 2"
5
ghci> parse (chainr1 number (sym '-' >>: (-))) "10 - 3 - 2"
9
```

The first computes `(10 - 3) - 2`, the second `10 - (3 - 2)`. Most arithmetic operators are left-associative, so `chainl1` is usually what you want.

### Putting It Together: Arithmetic

These combinators are enough to write a complete parser for arithmetic expressions that produces an AST with the correct precedence (`*` before `+`) and handles parentheses:

```haskell
import ParserCombinators

data Expr = Num Integer
          | Plus Expr Expr
          | Times Expr Expr
          deriving Show

expr, term, factor :: Parser Expr
expr   = chainl1 term   (sym '+' >>: Plus)
term   = chainl1 factor (sym '*' >>: Times)
factor = (number >>=: Num) <|> parens expr
```

```
ghci> parse expr "1 + 2 * (3 + 4)"
Plus (Num 1) (Times (Num 2) (Plus (Num 3) (Num 4)))
```

Each level of the grammar gets its own parser. Constructors like `Plus` and `Times` are already two-argument functions, which is exactly what `chainl1` needs from its operator parser.

## Error Messages

```haskell
(<??>)  :: Parser a -> String -> Parser a
(<???>) :: Parser a -> String -> Parser a
```

Both attach your own error message to a parser, to replace the default one when it fails. They differ in how aggressive they are:

- `p <??> msg` **always** replaces `p`'s error with `msg`, throwing away any information about how far `p` got.
- `p <???> msg` replaces the error only if `p` got **nowhere** (failed on its very first character). If `p` made some progress before failing, its own, more specific error message is kept.

```haskell
ab = char 'a' <+> char 'b'
```

```
ghci> parse (ab <??> "an ab pair expected") "ax"
*** Exception: <input>:1:1 -- an ab pair expected
ghci> parse (ab <???> "an ab pair expected") "ax"
*** Exception: <input>:1:2 -- Expected 'b'
ghci> parse (ab <???> "an ab pair expected") "zz"
*** Exception: <input>:1:1 -- an ab pair expected
```

## Operator Precedence

When you mix operators without parentheses, these fixities decide how they group. A higher number binds more tightly.

| Operators | Fixity |
|---|---|
| `<=>` | `infix 7` |
| `<+>`, `<+->`, `<-+>`, `<-+->` | `infixl 6` |
| `<:>`, `<++>` | `infixr 5` |
| `<|>`, `<??>`, `<???>` | `infixl 3` |
| `>>=:`, `>>:`, `>>=` | `infixl 1` |

In practice, that means two things:

- **Transform last.** `p <+> q >>=: f` means `(p <+> q) >>=: f`, so you can sequence several parsers and then transform the combined result, with no parentheses.
- **Parenthesize alternatives that each transform.** `a >>=: f <|> b >>=: g` does *not* do what it looks like. Write `(a >>=: f) <|> (b >>=: g)`, as in `factor` above.
