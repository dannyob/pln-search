"""Data models for PLN API responses."""

from dataclasses import dataclass


@dataclass
class Member:
    """Member entity from PLN directory."""

    uid: str
    name: str
    email: str | None
    bio: str | None
    location: str | None
    skills: list[str]
    github_handler: str | None


@dataclass
class Team:
    """Team entity from PLN directory."""

    uid: str
    name: str
    short_description: str | None
    website: str | None
    member_count: int


@dataclass
class Project:
    """Project entity from PLN directory."""

    uid: str
    name: str
    description: str | None
    maintaining_team: str | None
    looking_for_funding: bool
