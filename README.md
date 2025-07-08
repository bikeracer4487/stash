# Stash

A self-hosted webapp for managing and organizing your media.

## Building on Windows

### Prerequisites

To build Stash on Windows, you'll need:
- **Go** (version 1.24.3 or later) - [Download](https://golang.org/dl/)
- **MinGW-w64** (for Make and GCC) - [Download](https://sourceforge.net/projects/mingw-w64/files/)
- **Node.js** (LTS version) - [Download](https://nodejs.org/)
- **Yarn** - Install via npm: `npm install -g yarn`
- **Git** - [Download](https://git-scm.com/download/win)

### Quick Setup

1. **Install MinGW-w64**
   - Download the `x86_64-posix-seh` archive (not the installer)
   - Extract to `C:\mingw64`
   - Add `C:\mingw64\bin` to your system PATH

2. **Verify installations**
   ```cmd
   go version
   mingw32-make --version
   gcc --version
   node --version
   yarn --version
   ```

### Building Stash

1. **Clone the repository**
   ```cmd
   git clone https://github.com/stashapp/stash.git
   cd stash
   ```

2. **Install dependencies and build**
   ```cmd
   mingw32-make pre-ui     # Install UI dependencies
   mingw32-make generate   # Generate GraphQL files
   mingw32-make ui         # Build UI
   mingw32-make stash      # Build stash binary
   ```

   Or build everything at once:
   ```cmd
   mingw32-make release
   ```

### Development Mode

For active development:

```cmd
# Terminal 1 - Backend server (http://localhost:9999)
mingw32-make server-start

# Terminal 2 - UI dev server (http://localhost:3000)
mingw32-make ui-start
```

### Windows-Specific Notes

- Always use `mingw32-make` instead of `make` on Windows
- If you encounter antivirus warnings, add exclusions for the project directory
- For detailed setup instructions, see [docs/WINDOWS_DEVELOPMENT_SETUP.md](docs/WINDOWS_DEVELOPMENT_SETUP.md)

## Other Platforms

For building on macOS, Linux, and other platforms, refer to the [development documentation](docs/DEVELOPMENT.md).