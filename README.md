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

## Development Status

**Implemented:**
- ✓ Data models (Member, Team, Project)
- ✓ Configuration management with XDG directories
- ✓ API client with search methods
- ✓ Output formatters (rich, plain, JSON)
- ✓ OAuth2 token refresh
- ✓ CLI commands
- ✓ Test suite

**TODO for production use:**
- [ ] Full OAuth2 browser flow (currently stub)
- [ ] Integration testing with real API
- [ ] Error message improvements
- [ ] Performance optimization
- [ ] PyPI packaging

## Testing

The project includes a comprehensive test suite. Note that OAuth2 browser authentication is currently a stub and requires manual token setup for testing against the real API.

For local development and testing, mock the API responses.
