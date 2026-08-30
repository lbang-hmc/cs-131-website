# Connecting to the Server with VS Code

Most of your CS131 work happens on the course programming server, not on your own machine — it's already set up with Haskell, GHC, and everything else the course needs. The easiest way to edit and run code there is VS Code's **Remote-SSH** extension, which opens a normal-feeling VS Code window (editor, integrated terminal, file explorer) that's actually operating on files over on the server.

The server's hostname is **`cs131.cs.hmc.edu`**. This guide walks through first login, installing the extension, connecting, and what to do once you're in.

## 1. First login and changing your password

The very first time you connect, do it from a plain terminal — either a standalone one or the terminal integrated into VS Code — rather than the extension, since you'll need a fresh password in hand before the extension can use it.

```bash
ssh <your-username>@cs131.cs.hmc.edu
```

Enter the password the instructors gave you (it'll likely be a long passphrase of several words separated by hyphens). You'll immediately be required to change it — you won't see anything as you type your new password, which is normal. Pick something you'll remember (a password manager helps), since you'll need it every time you reconnect.

## 2. Install the Remote-SSH extension

1. Open VS Code and go to the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`).
2. Search for **Remote - SSH** and install the one published by Microsoft (`ms-vscode-remote.remote-ssh`) — it's described as letting you "open a folder on a remote machine using SSH."

Once it's installed, you should see a small icon appear in the bottom-left corner of the VS Code window (usually green, though the exact color depends on your theme) — that's how you'll open remote connections going forward. You only need to install the extension once.

## 3. Connect to the server

1. Click that new icon in the bottom-left corner and choose **Connect to Host...** (or open the Command Palette with `Ctrl+Shift+P` / `Cmd+Shift+P` and run **Remote-SSH: Connect to Host...**).
2. Skip the extra configuration options and just enter `<your-username>@cs131.cs.hmc.edu`.
3. VS Code opens a new window and prompts you for a password — use the **new** password you set in step 1.

The first time you connect, VS Code needs to set up the SSH host and install some server-side components, so it can take a little while — after that, reconnecting is much faster. Once connected, the status bar in the bottom-left corner shows `SSH: cs131.cs.hmc.edu`, and you may be prompted to accept a few update dialogs along the way (safe to accept).

## 4. Working on the server

- **Open your files:** click the file explorer icon and choose **Open Folder**, then open your home directory (it has the same name as your username). The first time you do this, VS Code will ask for your password again and may ask whether to trust the folder — say yes to both.
- **Use a terminal:** open one with `` Ctrl+` `` — this is a real shell running on the server, not your local machine. Try `pwd` and `ls` to get oriented.
- **Try Haskell:** run `ghci` to get an interactive Haskell interpreter — similar to interpreters you may have used for Python or Racket. Type an expression and hit enter to evaluate it (e.g. `1 + 41`, or `sqrt 42`); type `:q` (or hit `Ctrl+D`) to quit back to the shell. (This is the same command used throughout the [labs](../labs/lab02.md) — you'll run it constantly this semester.)

## 5. Disconnecting and reconnecting

When you're done, click the remote-connection status item in the bottom-left corner and choose **Close Remote Connection** (scroll down if you don't see it right away, or just start typing "close remote connection" and let it autocomplete). VS Code keeps a list of recent connections, so reconnecting later is one click away — you'll just need to enter your password again.

---

From here, you're ready to work through the [labs](../labs/index.md) and homework assignments directly on the server.
