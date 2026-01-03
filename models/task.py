from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, Any, Optional


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    deadline: Optional[str] = None
    priority: str = "Normal"
    completed: bool = False
    created_at: Optional[str] = None

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
            description=str(d.get("description", "")),
            deadline=d.get("deadline"),
            priority=str(d.get("priority", "Normal")),
            completed=bool(d.get("completed", False)),
            created_at=d.get("created_at"),
        )
