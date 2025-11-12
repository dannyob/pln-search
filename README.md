# pln-search

Command-line tool for searching the PLN Directory API.

## Installation

```bash
uv pip install -e .
```

## Usage

### Authentication

The PLN Directory uses Privy for web authentication. Until we implement a full OAuth2 flow for CLI tools, you'll need to manually configure your authentication token:

**Step 1: Get your token from the browser**

1. Visit https://directory.plnetwork.io/ and log in
2. Open browser Developer Tools (F12 or right-click → Inspect)
3. Go to the Network tab
4. Browse the site (view members, teams, etc.)
5. Find a request to the API (look for requests to the API URL)
6. Click on the request and find the 'Authorization' header
7. Copy the token after 'Bearer ' (the long string)

**Step 2: Configure the token**

Option A - Interactive (recommended):
```bash
pln-search auth token --interactive
```

Option B - Command line:
```bash
pln-search auth token YOUR_TOKEN_HERE
```

**Check authentication status:**
```bash
pln-search auth status
```

**Logout (clear credentials):**
```bash
pln-search auth logout
```

### Searching

Search:
```bash
pln-search search "John Doe"                 # Global search
pln-search search --members "John Doe"       # Search members
pln-search search --teams "Protocol Labs"    # Search teams
pln-search search --projects "IPFS"          # Search projects
```

Options:
```bash
pln-search search "query" --limit 50         # Show up to 50 results
pln-search search "query" --json             # JSON output
pln-search search "query" --no-color         # Plain text output
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
