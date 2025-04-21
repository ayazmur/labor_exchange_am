from dataclasses import dataclass
from datetime import datetime

@dataclass
class Job:
    id: int
    user_id: int
    title: str
    description: str
    salary_from: str
    salary_to: str
    is_active: bool = True
    created_at: datetime = None
