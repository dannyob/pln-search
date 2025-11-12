"""Command-line interface for pln-search."""

import sys
import click
from pln_search import __version__
from pln_search.config import ConfigManager
from pln_search.auth import OAuth2Flow, AuthenticationError
from pln_search.api import PLNAPIClient, APIError
from pln_search.formatters import OutputFormatter


@click.group(invoke_without_command=True)
@click.option("--members", "search_type", flag_value="members", help="Search members only")
@click.option("--teams", "search_type", flag_value="teams", help="Search teams only")
@click.option("--projects", "search_type", flag_value="projects", help="Search projects only")
@click.option("--limit", default=20, help="Maximum results to show", type=int)
@click.option("--json", "output_json", is_flag=True, help="Output JSON")
@click.option("--no-color", is_flag=True, help="Plain text output")
@click.option("--version", is_flag=True, help="Show version")
@click.argument("query", required=False)
@click.pass_context
def main(ctx, search_type, limit, output_json, no_color, version, query):
    """PLN Search - Search the PLN Directory API.

    Examples:
        pln-search "John Doe"                 # Global search
        pln-search --members "John"           # Search members
        pln-search --teams "Protocol"         # Search teams
        pln-search --projects "IPFS"          # Search projects
        pln-search "query" --json             # JSON output
    """
    # Handle version flag
    if version:
        click.echo(f"pln-search version {__version__}")
        return

    # If no query and no subcommand, show help
    if not query and ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())
        return

    # Only run search if query provided
    if query:
        try:
            _run_search(query, search_type, limit, output_json, no_color)
        except AuthenticationError as e:
            click.echo(f"✗ {e}", err=True)
            sys.exit(2)
        except APIError as e:
            click.echo(f"✗ {e}", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"✗ Unexpected error: {e}", err=True)
            sys.exit(1)


def _run_search(query: str, search_type: str, limit: int, output_json: bool, no_color: bool):
    """Run search and display results."""
    # Initialize components
    config = ConfigManager()
    auth = OAuth2Flow(config.get_api_base_url(), config)
    client = PLNAPIClient(config.get_api_base_url(), auth)

    # Determine output format
    if output_json:
        format_type = "json"
    elif no_color:
        format_type = "plain"
    else:
        format_type = "auto"

    formatter = OutputFormatter(format_type)

    # Execute search based on type
    if search_type == "members":
        results = client.search_members(query, limit)
        formatter.format_members(results)
    elif search_type == "teams":
        results = client.search_teams(query, limit)
        formatter.format_teams(results)
    elif search_type == "projects":
        results = client.search_projects(query, limit)
        formatter.format_projects(results)
    else:
        # Global search - search all types
        members = client.search_members(query, limit)
        teams = client.search_teams(query, limit)
        projects = client.search_projects(query, limit)

        formatter.format_members(members)
        formatter.format_teams(teams)
        formatter.format_projects(projects)


@main.group()
def auth():
    """Authentication commands."""
    pass


@auth.command("login")
def auth_login():
    """Start OAuth2 authentication flow."""
    try:
        config = ConfigManager()
        auth_flow = OAuth2Flow(config.get_api_base_url(), config)
        auth_flow.start_auth_flow()
    except Exception as e:
        click.echo(f"✗ Authentication failed: {e}", err=True)
        sys.exit(1)


@auth.command("status")
def auth_status():
    """Check authentication status."""
    config = ConfigManager()
    creds = config.load_credentials()

    if creds:
        user_info = creds.get("user_info", {})
        click.echo("✓ Authenticated")
        if user_info.get("name"):
            click.echo(f"  User: {user_info['name']}")
        if user_info.get("email"):
            click.echo(f"  Email: {user_info['email']}")
    else:
        click.echo("✗ Not authenticated")
        click.echo("  Run: pln-search auth login")
        sys.exit(2)


@auth.command("logout")
def auth_logout():
    """Remove stored credentials."""
    config = ConfigManager()
    config.clear_credentials()
    click.echo("✓ Logged out")


if __name__ == "__main__":
    main()
