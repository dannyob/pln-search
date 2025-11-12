# pln-search

CLI tool for searching the PLN Directory API.

## Documentation

- **Design Document:** [docs/plans/2025-11-11-pln-search-cli-design.md](docs/plans/2025-11-11-pln-search-cli-design.md)
- **Implementation Plan:** [docs/plans/2025-11-11-pln-search-implementation.md](docs/plans/2025-11-11-pln-search-implementation.md)

## Quick Start

Installation:
```bash
uv pip install -e .
```

Authentication:
```bash
pln-search auth login
```

Search:
```bash
pln-search "John Doe"                 # Global search
pln-search --members "John Doe"       # Search members
pln-search --teams "Protocol Labs"    # Search teams
pln-search --projects "IPFS"          # Search projects
```

## Development

See implementation plan for detailed task breakdown.
