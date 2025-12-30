from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any


@dataclass
class Task:
    id: int
    title: str
    completed: bool = False
    created_at: str | None = None

    def __post_init__(self):
        if self.created_at is None:
            # use timezone-aware UTC timestamp
            self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Task":
        return Task(
            id=int(d.get("id", 0)),
            title=str(d.get("title", "")),
            completed=bool(d.get("completed", False)),
            created_at=d.get("created_at"),
        )
