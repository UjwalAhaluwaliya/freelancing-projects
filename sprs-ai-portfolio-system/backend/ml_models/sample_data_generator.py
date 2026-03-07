from __future__ import annotations

import json
from pathlib import Path

import numpy as np


TECH_STACKS = [
    ["Python", "Flask", "MongoDB"],
    ["Java", "Spring", "PostgreSQL"],
    ["Node.js", "React", "MongoDB"],
    ["Python", "FastAPI", "Redis"],
    [".NET", "Azure", "SQL Server"],
]

DOMAINS = [
    "finance automation",
    "supply chain visibility",
    "cybersecurity hardening",
    "customer analytics",
    "HR digital workflow",
    "cloud migration",
    "data governance",
    "compliance modernization",
    "IT service optimization",
    "sales intelligence",
]

STATUSES = ["proposed", "active", "on_hold", "completed", "retired"]
RISK_LEVELS = ["low", "medium", "high"]


def generate_sample_projects(n: int = 50, seed: int = 42):
    rng = np.random.default_rng(seed)
    projects = []
    for idx in range(1, n + 1):
        domain = DOMAINS[idx % len(DOMAINS)]
        stack = TECH_STACKS[idx % len(TECH_STACKS)]
        budget = float(rng.integers(150000, 5000000))
        roi = float(np.round(rng.uniform(5.0, 45.0), 2))
        risk = RISK_LEVELS[int(rng.integers(0, len(RISK_LEVELS)))]
        duration = int(rng.integers(4, 30))
        alignment = float(np.round(rng.uniform(3.0, 10.0), 2))

        projects.append(
            {
                "project_name": f"Project {idx:02d} - {domain.title()}",
                "description": f"Initiative focused on {domain} with enterprise process improvements and measurable business outcomes.",
                "budget": budget,
                "expected_roi": roi,
                "risk_level": risk,
                "team_size": int(rng.integers(4, 35)),
                "technology_stack": stack,
                "duration": duration,
                "strategic_alignment_score": alignment,
                "status": STATUSES[int(rng.integers(0, len(STATUSES)))],
            }
        )

    return projects


def write_sample_dataset(output_path: Path):
    data = generate_sample_projects(n=50, seed=42)
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "sample_projects.json"
    write_sample_dataset(target)
    print(f"Generated: {target}")
