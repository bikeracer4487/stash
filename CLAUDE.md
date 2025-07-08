# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stash is a self-hosted webapp written in Go that organizes and serves adult content. It consists of:
- **Backend**: Go server with GraphQL API (`/internal/api`, `/pkg`)
- **Frontend**: React/TypeScript UI (`/ui/v2.5`) built with Vite
- **Database**: SQLite with custom migration system (`/pkg/sqlite`)
- **Media Processing**: FFmpeg integration for video/image processing

## Common Development Commands

### Initial Setup
```bash
make pre-ui          # Install UI dependencies (run once)
make generate        # Generate GraphQL files for both backend and UI
```

### Development Server
```bash
# Terminal 1 - Backend (runs on http://localhost:9999)
make server-start

# Terminal 2 - UI dev server (runs on http://localhost:3000)
make ui-start
```

### Building
```bash
make stash           # Build stash binary only
make phasher         # Build phasher binary only
make build           # Build both binaries
make build-release   # Build release versions with optimizations
make ui              # Build UI for production
make release         # Full release build (pre-ui → generate → ui → build-release)

# Cross-compilation (requires Docker)
make start-compiler-container  # Start build container
make build-cc-all             # Build for all platforms in container
make remove-compiler-container # Clean up container
```

### Code Generation
```bash
make generate        # Regenerate all GraphQL files
make generate-backend
make generate-ui
make generate-stash-box-client
make generate-dataloaders
make generate-test-mocks    # Generate test mocks using mockery
```

### Testing
```bash
make test            # Run unit tests
make it              # Run all tests including integration
go test ./pkg/scene  # Run tests for specific package
```

### Code Quality
```bash
# Backend
make fmt             # Format Go code
make lint            # Run golangci-lint
make validate-backend # Run all backend checks (lint + tests)
make validate        # Run all validation (backend + UI)

# Frontend
make fmt-ui          # Format UI code
make validate-ui     # Run ESLint, Stylelint, and TypeScript checks

# Quick checks for changed files only
make fmt-ui-quick
make validate-ui-quick
```

### Environment Variables
- `STASH_CONFIG_FILE`: Config file location (default: `config.yml`)
- `VITE_APP_PLATFORM_URL`: Backend URL for UI development (default: `http://localhost:9999`)

### Build Environment Variables
- `OUTPUT`: Set custom binary name for both stash and phasher
- `STASH_OUTPUT`: Set custom name for stash binary only
- `PHASHER_OUTPUT`: Set custom name for phasher binary only
- `GO_BUILD_FLAGS`: Add extra Go build flags
- `GO_BUILD_TAGS`: Add extra build tags
- `STASH_NOLEGACY`: Disable legacy browser support
- `STASH_SOURCEMAPS`: Enable UI sourcemaps

## Architecture Patterns

### GraphQL Code Generation
The project uses code generation extensively:
- Backend GraphQL server uses `gqlgen` configured in `gqlgen.yml`
- Frontend uses generated TypeScript types from GraphQL schema
- Changes to `graphql/schema/**/*.graphql` require running `make generate`

### Database Migrations
- SQLite migrations in `/pkg/sqlite/migrations/`
- Numbered SQL files with optional Go migration hooks
- Custom migration system handles schema updates automatically

### Plugin System
- Plugins can be written in JavaScript, Python, or as external processes
- Plugin configuration in YAML files
- Hooks into various lifecycle events (scene creation, scanning, etc.)

### Frontend Architecture
- React with TypeScript
- Apollo Client for GraphQL
- Bootstrap for UI components
- Internationalization support (32 languages)
- Component structure mirrors backend models (Scenes, Performers, Studios, etc.)

### Backend Service Pattern
Each major entity follows a consistent pattern:
- Repository interface in `/pkg/models/`
- SQLite implementation in `/pkg/sqlite/`
- Service layer in `/pkg/{entity}/`
- GraphQL resolver in `/internal/api/`
- Import/export functionality for data portability

### Media Processing
- FFmpeg wrapper in `/pkg/ffmpeg/`
- Transcoding, thumbnail generation, and sprite generation
- Support for various video and image formats
- Streaming capabilities with HLS/DASH support

## Design Philosophy
Based on the project's contribution guidelines, follow these principles:
- **Minimal core with plugin extensibility**: Core features should be minimal while being extensible via plugins
- **Offline and portable**: The application should run from USB without dependencies (except ffmpeg)
- **Generic interfaces**: External system interfaces should be as generic as possible
- **Feature scrutiny**: Large features should be considered for third-party plugins instead of core

## Code Standards
- Go code must be formatted with `gofmt`
- Must pass golangci-lint checks (configured in `.golangci.yml`)
- TypeScript follows strict typing with interface names starting with 'I'
- Frontend extends airbnb-typescript standards
- All code should be well-commented for maintainability

## Docker Support
- Production Docker image includes all dependencies including ffmpeg
- Default binding to port 9999
- Production deployments should use a reverse proxy (NGINX/Traefik)
- Build with: `make docker-build`

## PR Branch Creation Guidelines
When I ask you to create a PR branch, that means I want you to create a new branch in the repo but then normalize it to the parent repo for PR prep by removing all Claude-created settings and documentation files and then pushing these changes to the new branch (named PR-branch). For this purpose, create a "CLAUDE_FILES.md" file for keeping track of these files which currently consists only of CLAUDE.md and docs/WINDOWS_DEVELOPMENT_SETUP.md . Lastly, to prep for PR, you will need to sync the parent repo's README.md to our branch. If the 'PR-branch' already exists, then remove it and create a new one.