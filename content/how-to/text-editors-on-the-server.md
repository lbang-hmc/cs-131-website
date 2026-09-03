# Text Editors on the Server

If you'd rather work entirely in the terminal instead of [connecting with VS Code](connecting-with-vscode.md), the course server has several terminal text editors installed. Any of them will do fine for editing Haskell this semester — pick whichever feels comfortable.

All of them are launched the same way: type the editor's command followed by a filename. If the file doesn't exist yet, it's created when you save.

```bash
vim   Lab01.hs
nvim  Lab01.hs
micro Lab01.hs
hx    Lab01.hs
```

## vim

The editor you'll find on essentially every Unix machine ever. **vim** is *modal*: you start in "normal" mode where keys are commands (move, delete, change), and press `i` to enter "insert" mode where you actually type. `Esc` gets you back to normal mode. Save and quit with `:wq`, quit without saving with `:q!`.

It has a steep first hour and a very long payoff. If you've never used it, run `vimtutor` at the shell for a 30‑minute built‑in walkthrough.

## neovim

**neovim** (command `nvim`) is a modernized fork of vim. The editing model and keystrokes are the same — everything in the vim section above applies — but it ships with saner defaults, better terminal support, and a nicer plugin system. If you like vim's approach, there's no real reason not to use `nvim` instead.

## micro

**micro** is the one to reach for if modal editing sounds like a hassle. It behaves the way you'd expect a modern editor to: `Ctrl+S` saves, `Ctrl+Q` quits, `Ctrl+C`/`Ctrl+V` copy and paste, arrow keys move, and the mouse works for clicking and selecting. Syntax highlighting is on out of the box. Press `Ctrl+E` to type a command, or `Ctrl+G` for help.

## helix

**helix** (command `hx`) is a newer modal editor. It's in the same family as vim but flips the order of operations — you *select* something first, then act on it, with the selection always visible — which many people find easier to learn. It comes with syntax highlighting and code intelligence built in, no configuration or plugins required. Press `Space` then `?` to browse commands; save and quit with `:wq` like vim.

## Want a different editor?

If you'd like a particular editor (emacs, nano, a specific plugin, whatever) installed on the server, just email <bang@cs.hmc.edu> and I'll get it set up.
