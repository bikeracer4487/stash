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
```

### Code Generation
```bash
make generate        # Regenerate all GraphQL files
make generate-backend
make generate-ui
make generate-stash-box-client
make generate-dataloaders
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