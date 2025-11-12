# pln-search

Command-line tool for searching the PLN Directory API.

## Installation

```bash
uv pip install -e .
```

## Usage

Authenticate:
```bash
pln-search auth
```

Search:
```bash
pln-search "John Doe"                 # Global search
pln-search --members "John Doe"       # Search members
pln-search --teams "Protocol Labs"    # Search teams
pln-search --projects "IPFS"          # Search projects
```

Options:
```bash
pln-search "query" --limit 50         # Show up to 50 results
pln-search "query" --json             # JSON output
pln-search "query" --no-color         # Plain text output
```

## Development

Install dependencies:
```bash
make install-dev
```

Run tests:
```bash
make test
```

Format code:
```bash
make format
```
