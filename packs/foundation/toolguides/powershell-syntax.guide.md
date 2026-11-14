# PowerShell Syntax Guide

## Overview

This guide helps AI agents use correct PowerShell syntax when working with spec-kitty workflows.

## When to use

Read this if you are working in a PowerShell environment.

## Usage

### Using the spec-kitty CLI

Spec-kitty uses a Python CLI that works across all platforms. There are no
PowerShell wrapper scripts: call the CLI directly, with its normal
double-dash flags, from PowerShell exactly as you would from Bash.

**Common commands:**

- `spec-kitty agent mission create <slug> --json` - Create a new mission
- `spec-kitty verify-setup` - Check environment and paths
- `spec-kitty agent action implement <WPID> --agent <name> --mission <handle>` - Start implementing a work package (moves it to `in_progress`)
- `spec-kitty agent action review <WPID> --agent <name> --mission <handle>` - Start reviewing a work package
- `spec-kitty agent tasks move-task <WPID> --to for_review --mission <handle>` - Complete implementation (move to review)
- `spec-kitty consolidate` - Consolidate completed mission

### Parameter Naming Convention

CLI flags keep their double-dash spelling on every shell (`--json`,
`--mission`, `--include-tasks`). PowerShell's PascalCase `-Param` convention
applies only to PowerShell cmdlets and your own functions, never to
`spec-kitty` flags.

### Examples

**Create a mission:**

```powershell
spec-kitty agent mission create "user-authentication" `
  --friendly-name "User Authentication" `
  --json
```

**Check prerequisites:**

```powershell
spec-kitty agent mission check-prerequisites --json --include-tasks --mission <handle>
```

**Move task to review (after implementation):**

```powershell
spec-kitty agent tasks move-task WP01 --to for_review --mission <handle> --note "Ready for review"
```

## Windows PowerShell 5.1 and PowerShell 7 (`pwsh`)

Check which one you are in before you chain commands:

```powershell
$PSVersionTable.PSVersion
```

- **PowerShell 7 (`pwsh`, version 7.x)** supports `&&` and `||`. They behave as in
  Bash: the second command runs only if the first succeeded (`&&`) or failed (`||`).
- **Windows PowerShell 5.1** has no `&&` or `||`. Check the result yourself.

`;` is not a replacement for `&&` in either version: it runs the next command even
when the previous one failed.

## Quick Reference: Bash vs PowerShell

| Task | Bash | PowerShell |
|------|------|------------|
| **Run B only if A succeeded** | `cmd1 && cmd2` | pwsh 7: `cmd1 && cmd2`. 5.1, after a native program: `cmd1; if ($LASTEXITCODE -eq 0) { cmd2 }`; after a cmdlet: `cmd1; if ($?) { cmd2 }` |
| **Run B whatever A did** | `cmd1; cmd2` | `cmd1; cmd2` |
| **Cmdlet parameters** (not `spec-kitty` flags) | `ls --recurse` | `Get-ChildItem -Recurse` |
| **Environment variable** | `$VAR_NAME` | `$env:VAR_NAME` |
| **Current directory** | `pwd` | `Get-Location` (or `pwd` alias) |
| **List files** | `ls -la` | `Get-ChildItem` (or `ls` alias) |
| **File exists check** | `[ -f file.txt ]` | `Test-Path file.txt` |
| **Home directory** | `~/projects` | `$HOME/projects` or `$HOME\projects` |

`$LASTEXITCODE` holds the exit code of the last native program, such as
`spec-kitty` or `git`. `$?` is `$true` when the last command succeeded; use it after
a cmdlet. Paths take either `/` or `\` in both versions.

## Location Verification (PowerShell)

**Check your current location:**

```powershell
Get-Location
git branch --show-current
```

**Expected when implementing a work package:**

- Location: the checkout that `spec-kitty agent action implement` prints. Change into
  that path; do not build it yourself.
- Branch: whatever `git branch --show-current` shows there; it must not be `main`.
  Do not guess the branch name.

## Environment Variables

**Setting a variable for this session:**

```powershell
$env:MY_VARIABLE = "value"
```

**Reading it:**

```powershell
$env:MY_VARIABLE
```

**Checking if it is set:**

```powershell
if ($env:MY_VARIABLE) {
    Write-Host "Variable is set"
}
```

## File Operations

**Check if file exists:**

```powershell
if (Test-Path "spec.md") {
    Write-Host "Spec exists"
}
```

**Read file:**

```powershell
$content = Get-Content "spec.md" -Raw
```

**Create directory:**

```powershell
New-Item -ItemType Directory -Path "notes" -Force
```

## Workflow Tips

1. **Always use full parameter names** in scripts (not abbreviations)
2. **Chain on success** with `&&` on pwsh 7. On 5.1 use `if ($LASTEXITCODE -eq 0)` after a native program such as `spec-kitty` or `git`, and `if ($?)` after a cmdlet. A `;` does not stop after a failure
3. **Either separator** works in paths; keep what the CLI printed
4. **`$PID`** holds the current PowerShell process ID: pass `--shell-pid $PID` to `spec-kitty agent tasks move-task`. (`$$` is not the process ID in PowerShell)
5. **Tab completion** works for parameter names in PowerShell

## When to Use What

**Use PowerShell syntax when:**

- You're in a Windows PowerShell or `pwsh` terminal

**Use Bash syntax when:**

- You're in a bash/zsh/fish terminal

**Using spec-kitty commands:**
All spec-kitty commands work the same way on PowerShell and Bash:

```powershell
spec-kitty agent action implement WP01 --agent claude --mission <handle>  # Moves to in_progress
spec-kitty agent tasks move-task WP01 --to for_review --mission <handle>  # Completion step
spec-kitty verify-setup
spec-kitty agent tasks status --mission <handle>
```

The CLI is cross-platform and handles path differences automatically.

## Debugging PowerShell Issues

**Common errors and solutions:**

1. **"A parameter cannot be found that matches parameter name" on a cmdlet**
   - You gave a cmdlet a Bash-style parameter (`Get-ChildItem --recurse`)
   - Fix: use the cmdlet's own parameter (`-Recurse`). This applies to cmdlets only:
     `spec-kitty` flags always keep `--` (`--json`)

2. **"The token '&&' is not a valid statement separator in this version"**
   - You are in Windows PowerShell 5.1, which has no `&&`
   - Fix: `cmd1; if ($LASTEXITCODE -eq 0) { cmd2 }`, or run the commands in `pwsh` 7

3. **"Cannot find path"**
   - The path does not exist from your current location
   - Fix: check `Get-Location` and `Test-Path <path>`. The separator is not the cause

4. **`spec-kitty` is not recognized, or a command fails on start-up**
   - The CLI is missing from `PATH` or the install is broken
   - Check: `Get-Command spec-kitty` shows whether it is on `PATH`; if it is, run
     `spec-kitty verify-setup --diagnostics`

## Cautions

### ❌ Don't Use `;` Where a Failure Must Stop You

```powershell
# WRONG (the work package moves to review even if the tests failed):
pytest; spec-kitty agent tasks move-task WP01 --to for_review --mission <handle>

# CORRECT on pwsh 7:
pytest && spec-kitty agent tasks move-task WP01 --to for_review --mission <handle>

# CORRECT on Windows PowerShell 5.1:
pytest; if ($LASTEXITCODE -eq 0) { spec-kitty agent tasks move-task WP01 --to for_review --mission <handle> }
```

### ❌ Don't Use Bash-Style Parameters on Cmdlets

```powershell
# WRONG (cmdlets take PascalCase parameters):
Get-ChildItem --recurse --filter *.md

# CORRECT:
Get-ChildItem -Recurse -Filter *.md

# The spec-kitty CLI is not a cmdlet: keep its double-dash flags.
spec-kitty agent tasks status --json --mission <handle>
```

### Path Separators in PowerShell

PowerShell accepts `/` and `\` in paths, in 5.1 and in pwsh 7, so both of these work:

```powershell
cd ./docs/guides
cd .\docs\guides
```

Some older Windows programs (for example `cmd.exe` built-ins) accept only `\`. The
spec-kitty CLI and git accept either.
