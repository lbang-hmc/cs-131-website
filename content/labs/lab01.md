# Lab 01: Getting Connected and Running Haskell

This first lab is intentionally short. The goal is to make sure you can use the basic tools we will rely on throughout CS 131:

- connect to the CS 131 programming server from a terminal,
- connect to the same server through VS Code,
- open a terminal that is actually running on the server,
- start `ghci`,
- evaluate a few simple Haskell expressions,
- create a Haskell source file, and
- load that file into `ghci`.

There is no programming challenge to solve today. If something does not work, **ask for help immediately**. Getting your environment working is the point of the lab.

!!! note "Gradescope"
    As you work, complete the corresponding **Lab 01** assignment on Gradescope.

    Most questions are simple completion checks. A few ask you to paste output or briefly describe what happened.

---

## Part 1: First Login from a Terminal

For your **first** connection to the server, use a plain terminal rather than VS Code's Remote-SSH extension.

Open a terminal and run:

```bash
ssh <your-username>@cs131.cs.hmc.edu
```

Replace `<your-username>` with the username provided to you for the course.

The first time you connect:

1. You may be asked whether you trust the host. Answer `yes`.
2. Enter the temporary password provided by the instructors.
3. You should immediately be prompted to choose a new password.
4. When typing a password, **nothing appears on the screen**. This is normal.

Once you are connected, try:

```bash
pwd
```

and:

```bash
ls
```

`pwd` shows your current directory. `ls` shows the files and directories there.

!!! question "Gradescope check: terminal connection"
    Complete the terminal-connection question on Gradescope.

If you cannot connect, stop here and ask for help before moving on.

---

## Part 2: Install VS Code Remote-SSH

Most of our work will be easiest through VS Code while connected remotely to the server.

Open VS Code and install Microsoft's **Remote - SSH** extension:

1. Open the Extensions panel with `Ctrl+Shift+X` or `Cmd+Shift+X`.
2. Search for **Remote - SSH**.
3. Install the extension published by **Microsoft** with identifier:

   ```text
   ms-vscode-remote.remote-ssh
   ```

You only need to install this extension once.

After installation, VS Code should show a remote-connection control in the bottom-left corner of the window.

!!! question "Gradescope check: Remote-SSH installed"
    Complete the Remote-SSH installation question on Gradescope.

---

## Part 3: Connect with VS Code

Now connect VS Code to the same server.

You can either:

- click the remote-connection control in the bottom-left corner and choose **Connect to Host...**, or
- open the Command Palette with `Ctrl+Shift+P` / `Cmd+Shift+P` and run:

```text
Remote-SSH: Connect to Host...
```

Enter:

```text
<your-username>@cs131.cs.hmc.edu
```

Use the new password you created during your terminal login.

The first connection may take a little while because VS Code installs some support software on the remote server.

Once connected, the bottom-left status area should indicate that you are connected to:

```text
cs131.cs.hmc.edu
```

Open the file explorer and choose **Open Folder**. Open your home directory.

You may be asked whether you trust the folder. Say yes.

!!! question "Gradescope check: VS Code connection"
    Complete the VS Code connection question on Gradescope.

---

## Part 4: Open a Terminal on the Server

Inside the remote VS Code window, open a terminal:

```text
Ctrl+`
```

or use **Terminal → New Terminal**.

This terminal is now running **on the CS 131 server**, not on your own computer.

Confirm by running:

```bash
hostname
```

and:

```bash
pwd
```

You should see the server's hostname and a path inside your home directory.

!!! question "Gradescope: confirm the remote terminal"
    Paste your `hostname` and `pwd` output into the corresponding Gradescope question.

---

## Part 5: Start `ghci`

In the terminal, run:

```bash
ghci
```

This starts the **Glasgow Haskell Compiler Interactive** environment, usually called `ghci`.

It is a REPL:

- **R**ead an expression,
- **E**valuate it,
- **P**rint the result,
- **L**oop back for another expression.

Try these:

```haskell
1 + 41
```

```haskell
2 * 3 + 4
```

```haskell
sqrt 49
```

```haskell
max 12 19
```

```haskell
"hello" ++ " world"
```

Then try one expression of your own.

Before pressing Enter each time, make a quick prediction about the result.

!!! question "Gradescope: a GHCi result"
    Paste the expression you invented and the output `ghci` produced.

To leave `ghci`, type:

```text
:q
```

or press `Ctrl+D`.

---

## Part 6: Create a Haskell File

Now create a small Haskell source file.

In your terminal, make a directory for this lab:

```bash
mkdir -p ~/cs131/lab01
cd ~/cs131/lab01
```

Confirm where you are:

```bash
pwd
```

In the VS Code file explorer, open the `cs131/lab01` directory if necessary.

Create a file called:

```text
lab01.hs
```

Put this code inside:

```haskell
x = 1 + 2

y = x + 3

double n = n * 2
```

Save the file.

---

## Part 7: Load the File into `ghci`

Back in the terminal, make sure you are still inside the `lab01` directory:

```bash
pwd
```

Start `ghci` again:

```bash
ghci
```

Then load the file:

```text
:load lab01.hs
```

You should see a message indicating that the file loaded successfully.

Now try:

```haskell
x
```

```haskell
y
```

```haskell
double 10
```

```haskell
double y
```

If you change the file in VS Code and save it, you can reload the file from inside `ghci` with:

```text
:r
```

Try changing:

```haskell
double n = n * 2
```

to:

```haskell
double n = n * 3
```

Save the file, run `:r`, and try `double 10` again.

!!! question "Gradescope: loading a Haskell file"
    Paste a short transcript showing that you successfully loaded `lab01.hs` and evaluated at least one of its definitions.

---

## Wrap Up

At this point you should be able to:

- connect to the server using `ssh`,
- connect using VS Code Remote-SSH,
- open a terminal running on the server,
- start and exit `ghci`,
- evaluate Haskell expressions,
- create and save a `.hs` file,
- load that file with `:load`, and
- reload it after editing with `:r`.

Those steps form the basic workflow we will use repeatedly throughout the course.

!!! question "Gradescope: wrap-up"
    Complete the final short reflection on Gradescope. If anything still does not work, say what happened so we can help get it fixed.
