# The Homework Workflow

Almost every homework assignment in CS131 follows the same shape: you make your own private copy of a starter repository on GitHub, clone it to the course server, write and test your code there, and then submit by pasting your test output (and, later in the semester, a PDF) into Gradescope.

This guide walks through that workflow end to end. The examples all use **HW 2** — the repository is `hw2`, the clone is named `cs-131-hw-02`, and so on — but the steps are the same for every assignment. Wherever you see `hw2` or `02`, substitute the number of the assignment you're actually working on.

!!! tip "Don't let GitHub get in the way"
    The point of this course is Haskell and programming languages, not fighting with `git`. If any step here gets you stuck, ask — post in the course forum, ask a grutor, ask in lab, or email the instructor at <bang@cs.hmc.edu>. Getting unstuck quickly is the goal.

## The Big Picture

1. **Get your own copy** of the assignment's starter repository, as a new *private* repo under your own GitHub account.
2. **Add your partner** to that repo, if you're pair-programming.
3. **Clone it** onto the course server.
4. **Write your code**, on the server.
5. **Run the tests** and save the output to a log file.
6. **Turn it in** on Gradescope.

Steps 4 and 5 are the assignment itself, and you'll repeat them many times as you work. Steps 1–3 are a one-time setup per assignment, and step 6 is a one-time finish.

## 1. Make your own copy of the starter repo

Each assignment's starter code lives in a **template repository** in the course's GitHub organization, **`hmc-cs-131-fa-2026`**. For HW 2 that's:

<https://github.com/hmc-cs-131-fa-2026/hw2>

(For another assignment, the URL follows the same pattern — `.../hmc-cs-131-fa-2026/hw3`, and so on.)

On that page:

1. Click **Use this template → Create a new repository**.
2. **Choose a name** you'll recognize later — something like `cs-131-hw-02` works well.
3. **Set the owner to your own GitHub account.** If you belong to other organizations, make sure it's *your account* that's selected, not one of them.
4. **Set visibility to Private.** Your coursework should not be public.
5. Click **Create repository**.

You now have your own copy of the starter code at `https://github.com/<your-username>/cs-131-hw-02`.

## 2. Add your partner (pair programming only)

If you're working with a partner on an assignment that allows it (HW 1 doesn't; most later ones do — see the pair-programming rules in the [syllabus](../syllabus.md)), add them to your repo so you can both push to it:

- On your repo's page, go to **Settings → Collaborators**, then **Add people**, and enter your partner's GitHub username.

Only one of you needs to create a repo; the other is added as a collaborator and clones that same repo.

## 3. Clone the repo onto the server

Do your work on the course server, where Haskell and everything else is already set up. [Connect with VS Code](connecting-with-vscode.md) or `ssh` in directly:

```bash
ssh <your-username>@cs131.cs.hmc.edu
```

Once you have a terminal on the server, move into a directory for your course work and clone your repo:

```bash
cd cs131            # or wherever you keep CS131 work; mkdir it first if needed
git clone https://github.com/<your-username>/cs-131-hw-02.git
cd cs-131-hw-02
```

A successful clone looks roughly like this:

```
Cloning into 'cs-131-hw-02'...
Username for 'https://github.com': <your-username>
Password for 'https://<your-username>@github.com':
remote: Enumerating objects: 12, done.
remote: Counting objects: 100% (12/12), done.
...
Receiving objects: 100% (12/12), done.
```

### The "password" is actually a token

When cloning over HTTPS, GitHub prompts for a **Username** and **Password** — but it will *not* accept your account password. What it wants in the password field is a **personal access token**. If you don't have one yet, see [Creating a personal access token](#creating-a-personal-access-token) below, then come back here.

A few things that trip people up:

- **Pasting into the terminal** is usually `Ctrl+Shift+V` (not `Ctrl+V`).
- **The token must be exact** — no leading/trailing spaces or newlines. Copy it carefully.
- **You won't see anything** as the token is "typed" into the password prompt. That's normal.

### Avoiding the token prompt every time

Retyping a token on every `git` operation gets old fast. Two common fixes:

- Have `git` remember it: `git config --global credential.helper store` (the token is then saved in a plaintext file in your home directory — fine on your own server account, but know that's the trade-off).
- Set up **SSH keys** and clone with the SSH URL (`git@github.com:<your-username>/cs-131-hw-02.git`) instead of HTTPS. GitHub's docs on "connecting to GitHub with SSH" walk through this; it's a bit more up-front work and then you never think about tokens again.

## 4. Write your code

Open the repo's files (in VS Code, or a [terminal editor](text-editors-on-the-server.md)) and work through the assignment. The starter code tells you which files to edit — for HW 2, that's `Functions.hs`, `Arithmetic.hs`, and a test file under `test/`.

Commit and push as you go, the same as any git project:

```bash
git add -A
git commit -m "Implement fib and step"
git push
```

Pushing regularly means your work is backed up and — if you're pair-programming — visible to your partner.

## 5. Run the tests and save the log

Every assignment ships with a test suite. Run it from the top level of the repo (the directory with the `.hs` files). See [Writing and Running Tests](writing-and-running-tests.md) for the full story; the command to run everything at once is:

```bash
runhaskell -itest test/Spec.hs
```

When you've gotten as far as you can, **run the suite one more time and capture its output to a file**, so you can submit it:

```bash
runhaskell -itest test/Spec.hs > testing.log
cat testing.log
```

`testing.log` now holds the full report — each test name, a pass/fail mark next to it, QuickCheck's `+++ OK, passed 100 tests` lines, and a summary like `45 examples, 29 failures` at the end. It's fine to submit a log with failures in it; submit the best state you were able to reach.

## 6. Turn it in on Gradescope

Submit on [Gradescope](https://www.gradescope.com), under this assignment's entry (for HW 2, **HW 02: FUNctional Programming**):

- **Paste the contents of `testing.log`** into the assignment's text-box question.
- Some assignments also ask you to **upload a PDF or specific files** — the assignment page says which. (HW 1 was paste-only; later assignments add an upload.)
- Don't forget the short **HW reflection**, submitted separately on Gradescope — every homework has one.

Make sure your final code is committed and pushed, too.

---

## Creating a personal access token

You need this once (or once per expiration period). On GitHub:

1. Click your profile picture → **Settings**.
2. In the left sidebar, scroll to **Developer settings**.
3. **Personal access tokens → Tokens (classic)**.
4. **Generate new token → Generate new token (classic)**.
5. Give it a note (e.g. "CS131 server"), and set the **expiration** to something comfortably past the end of the semester.
6. Under **scopes**, check **`repo`**.
7. Click **Generate token**.
8. **Copy the token and save it somewhere safe right now** — GitHub shows it exactly once. If you lose it, you can always generate another.

Use this token in the **password** field whenever `git` prompts you while talking to GitHub over HTTPS.
