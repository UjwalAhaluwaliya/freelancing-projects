from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    project_name: str
    description: str
    budget: float
    expected_roi: float
    risk_level: str
    team_size: int
    technology_stack: List[str]
    duration: float
    strategic_alignment_score: float
    status: str
