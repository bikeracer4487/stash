# Windows Development Setup Guide for Stash

This guide provides step-by-step instructions for setting up a development environment on Windows to build Stash from source.

## Prerequisites Overview

To build Stash on Windows, you'll need:
- **Go** (version 1.24.3 or later)
- **Make** (via MinGW-w64, Git Bash, or Chocolatey)
- **Node.js** (for UI builds)
- **Yarn** (JavaScript package manager)
- **GCC** (C compiler, comes with MinGW-w64)
- **Git** (version control)

## Step 1: Install Go

1. **Download Go for Windows**
   - Visit the official Go downloads page: https://golang.org/dl/
   - Download the Windows installer (`.msi` file) for your system architecture (typically `amd64` for 64-bit systems)
   - Current minimum version required: Go 1.24.3

2. **Install Go**
   - Run the downloaded `.msi` installer
   - Follow the installation wizard (default settings are fine)
   - Default installation path: `C:\Program Files\Go`

3. **Verify Go Installation**
   - Open Command Prompt or PowerShell
   - Run: `go version`
   - You should see output like: `go version go1.24.3 windows/amd64`

## Step 2: Install MinGW-w64 (for Make and GCC)

MinGW-w64 provides both the `make` command and the GCC compiler required for building Stash.

1. **Download MinGW-w64**
   - Visit: https://sourceforge.net/projects/mingw-w64/files/
   - Scroll down to "MinGW-W64 GCC-8.1.0" (or latest version)
   - Download: `x86_64-posix-seh` (e.g., `x86_64-8.1.0-release-posix-seh-rt_v6-rev0.7z`)
   - **Important**: Do NOT use the installer - download the archive directly

2. **Extract MinGW-w64**
   - Extract the downloaded archive to `C:\mingw64` (or your preferred location)
   - The folder structure should be: `C:\mingw64\bin`, `C:\mingw64\include`, etc.

3. **Add MinGW-w64 to System PATH**
   - Right-click "This PC" or "My Computer" → Properties
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "System variables", find and select "Path", then click "Edit"
   - Click "New" and add: `C:\mingw64\bin`
   - Click "OK" to close all dialogs

4. **Verify MinGW-w64 Installation**
   - Open a **new** Command Prompt (to load the updated PATH)
   - Run: `mingw32-make --version`
   - Run: `gcc --version`
   - Both commands should show version information

**Note**: On Windows with MinGW, you'll use `mingw32-make` instead of `make` for all build commands.

### Alternative: Install Make via Chocolatey

If you prefer using Chocolatey package manager:

1. Install Chocolatey (if not already installed): https://chocolatey.org/install
2. Open PowerShell as Administrator
3. Run: `choco install make mingw`

### Alternative: Use Git Bash

If you have Git for Windows installed, it includes a version of Make:
- The make command is available as `make` in Git Bash
- However, you'll still need to install MinGW-w64 for the GCC compiler

## Step 3: Install Node.js

1. **Download Node.js**
   - Visit: https://nodejs.org/
   - Download the Windows Installer (`.msi`) for the LTS version
   - Choose the 64-bit version

2. **Install Node.js**
   - Run the installer
   - Follow the installation wizard (default settings are fine)
   - Make sure "Add to PATH" is checked

3. **Verify Node.js Installation**
   - Open Command Prompt
   - Run: `node --version`
   - Run: `npm --version`
   - Both should display version numbers

## Step 4: Install Yarn

1. **Install Yarn using npm**
   - Open Command Prompt as Administrator
   - Run: `npm install -g yarn`

2. **Alternative: Install Yarn using Chocolatey**
   - If you have Chocolatey installed:
   - Run: `choco install yarn`

3. **Verify Yarn Installation**
   - Run: `yarn --version`
   - Should display the Yarn version number

## Step 5: Install Git (if not already installed)

1. **Download Git for Windows**
   - Visit: https://git-scm.com/download/win
   - Download the installer

2. **Install Git**
   - Run the installer
   - Default settings are generally fine
   - Make sure Git is added to PATH

3. **Verify Git Installation**
   - Run: `git --version`

## Step 6: Install GolangCI-Lint (Optional but Recommended)

GolangCI-Lint is used for code quality checks.

1. **Using PowerShell**
   ```powershell
   # Run this in PowerShell as Administrator
   (Invoke-WebRequest -Uri https://install.goreleaser.com/github.com/golangci/golangci-lint.ps1 -UseBasicParsing).Content | Invoke-Expression
   ```

2. **Using Chocolatey**
   ```cmd
   choco install golangci-lint
   ```

3. **Verify Installation**
   - Run: `golangci-lint --version`

## Verification: Check All Installations

Open a new Command Prompt and verify all tools are installed correctly:

```cmd
go version
mingw32-make --version
gcc --version
node --version
npm --version
yarn --version
git --version
golangci-lint --version
```

All commands should return version information without errors.

## Building Stash

Now that you have all dependencies installed, you can build Stash:

1. **Clone the Repository**
   ```cmd
   git clone https://github.com/stashapp/stash.git
   cd stash
   ```

2. **Install UI Dependencies**
   ```cmd
   mingw32-make pre-ui
   ```

3. **Generate Required Files**
   ```cmd
   mingw32-make generate
   ```

4. **Build the UI**
   ```cmd
   mingw32-make ui
   ```

5. **Build Stash Binary**
   ```cmd
   mingw32-make stash
   ```

   Or build everything at once:
   ```cmd
   mingw32-make release
   ```

## Windows-Specific Considerations

### 1. Command Differences
- Always use `mingw32-make` instead of `make` on Windows
- Example: `mingw32-make build` instead of `make build`

### 2. Path Separators
- Windows uses backslashes (`\`) for paths, but most tools accept forward slashes (`/`)
- In environment variables and configs, you may need to use forward slashes or escape backslashes

### 3. Antivirus Software
- Some antivirus programs may flag the compiled binaries
- You may need to add exclusions for the project directory and compiled executables

### 4. File Permissions
- Windows doesn't have Unix-style file permissions
- This is usually not an issue, but be aware when working with scripts

### 5. Line Endings
- Configure Git to handle line endings properly:
  ```cmd
  git config --global core.autocrlf true
  ```

### 6. PowerShell vs Command Prompt
- Some commands may work differently in PowerShell vs Command Prompt
- When in doubt, use Command Prompt for build commands

### 7. Long Path Support
- Enable long path support in Windows if you encounter path length issues:
  - Run `gpedit.msc` (Group Policy Editor)
  - Navigate to: Computer Configuration → Administrative Templates → System → Filesystem
  - Enable "Enable Win32 long paths"

## Troubleshooting

### "mingw32-make: command not found"
- Ensure `C:\mingw64\bin` is in your PATH
- Restart your command prompt after adding to PATH

### "go: command not found"
- Ensure Go is installed and `C:\Program Files\Go\bin` is in your PATH

### Build errors related to GCC
- Make sure you downloaded the correct MinGW-w64 version (x86_64-posix-seh)
- Verify GCC is accessible: `gcc --version`

### "yarn: command not found"
- Ensure Node.js is installed first
- Try installing yarn with npm: `npm install -g yarn`

### Permission errors
- Run Command Prompt as Administrator
- Check if antivirus is blocking operations

## Development Workflow

For active development on Windows:

1. **Start the development server**
   ```cmd
   mingw32-make server-start
   ```

2. **In a separate terminal, start the UI development server**
   ```cmd
   mingw32-make ui-start
   ```

3. **Access the development UI**
   - Open browser to: http://localhost:3000/

Remember to restart the server when making backend changes, while frontend changes will hot-reload automatically.