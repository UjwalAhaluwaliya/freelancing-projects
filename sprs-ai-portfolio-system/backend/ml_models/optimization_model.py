from __future__ import annotations

from typing import Dict, List, Set

try:
    from pulp import LpBinary, LpMaximize, LpProblem, LpStatus, LpVariable, lpSum, value

    PULP_AVAILABLE = True
except ImportError:  # pragma: no cover - runtime fallback for missing dependency
    PULP_AVAILABLE = False


def _fallback_greedy(project_ids: List[str], budgets: List[float], utilities: List[float], max_budget: float, blocked_ids: Set[str]) -> Dict:
    candidates = []
    for idx, pid in enumerate(project_ids):
        if pid in blocked_ids:
            continue
        cost = budgets[idx]
        utility = utilities[idx]
        ratio = utility / cost if cost > 0 else 0.0
        candidates.append((ratio, pid, cost, utility))

    candidates.sort(reverse=True)
    selected = []
    used_budget = 0.0
    objective = 0.0
    for _, pid, cost, utility in candidates:
        if used_budget + cost <= max_budget:
            selected.append(pid)
            used_budget += cost
            objective += utility

    return {
        "status": "FALLBACK_GREEDY",
        "selected_projects": selected,
        "objective_value": round(float(objective), 4),
        "max_budget": float(max_budget),
    }


def optimize_project_selection(
    project_ids: List[str],
    budgets: List[float],
    utilities: List[float],
    max_budget: float,
    blocked_ids: Set[str] | None = None,
) -> Dict:
    blocked_ids = blocked_ids or set()

    if not PULP_AVAILABLE:
        return _fallback_greedy(project_ids, budgets, utilities, max_budget, blocked_ids)

    problem = LpProblem("portfolio_optimization", LpMaximize)
    decision_vars = {
        pid: LpVariable(f"x_{idx}", cat=LpBinary)
        for idx, pid in enumerate(project_ids)
    }

    problem += lpSum(
        utilities[idx] * decision_vars[project_ids[idx]]
        for idx in range(len(project_ids))
    )

    problem += lpSum(
        budgets[idx] * decision_vars[project_ids[idx]]
        for idx in range(len(project_ids))
    ) <= max_budget

    for pid in blocked_ids:
        if pid in decision_vars:
            problem += decision_vars[pid] == 0

    problem.solve()

    selected = [pid for pid in project_ids if value(decision_vars[pid]) == 1]

    return {
        "status": LpStatus[problem.status],
        "selected_projects": selected,
        "objective_value": round(float(value(problem.objective)), 4) if value(problem.objective) is not None else 0.0,
        "max_budget": float(max_budget),
    }
