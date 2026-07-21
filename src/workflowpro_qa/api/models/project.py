from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProjectPayload:
    name: str
    description: str
    team_members: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "team_members": self.team_members,
        }


@dataclass(frozen=True)
class Project:
    id: int | str
    name: str
    status: str
    description: str | None = None

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> Project:
        return cls(
            id=data["id"],
            name=data["name"],
            status=data.get("status", "unknown"),
            description=data.get("description"),
        )
