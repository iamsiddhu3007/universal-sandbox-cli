# universal-sandbox-cli

Did you ever miss Linux when executing code?

Every time you want to run something in a Linux environment, you may have to go through multiple steps: setting up WSL, spinning up a VM, or managing Docker containers. After that, you still need to manually install tools like Claude Code, Codex, or the Antigravity CLI.

**universal-sandbox-cli** solves this by giving you an instant, ephemeral Linux environment that automatically mounts your local files and comes pre-installed with commonly used CLI tools.

Run a single command and the environment disappears when it finishes, or drop into an interactive shell when you need a full Linux terminal.

No boilerplate. No manual environment setup. No containers left behind.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

## Installation

### macOS

```bash
pip3 install universal-sandbox-cli
```

### Linux & Windows

```bash
pip install universal-sandbox-cli
```

## Usage

### 1. Run a Single Command

Execute any command inside an isolated Linux environment.

The sandbox starts, runs your command, prints the output, and automatically destroys the container when it finishes.

```bash
universal-sandbox-cli python3 script.py
universal-sandbox-cli codex --help
```

### 2. Drop Into an Interactive Shell

Need a full Linux terminal?

Run the CLI without any arguments to start an interactive root Bash shell.

```bash
universal-sandbox-cli
```

When you are finished, run:

```bash
exit
```

The container will be destroyed automatically.

### 3. Automatic Workspace Mounting

The sandbox automatically mounts your current working directory to:

```text
/workspace
```

inside the container.

This means files created or modified inside `/workspace` persist on your host machine even after the sandbox is destroyed.

## Pre-Installed Environments & Tools

### Runtimes

- Python 3 with native `venv`
- Node.js and npm
- Go
- Rust
- Java
- Ruby
- PHP

### CLI Tools

- `claude-code`
- `codex`
- `antigravity`
- `opencode`

### Core Utilities

- `git`
- `curl`
- `bash`
- `build-essential`

## License

MIT