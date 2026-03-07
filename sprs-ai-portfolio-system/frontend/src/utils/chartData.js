export function buildRoiBuckets(projects) {
  const buckets = [
    { bucket: "0-10", count: 0 },
    { bucket: "11-20", count: 0 },
    { bucket: "21-30", count: 0 },
    { bucket: "31-40", count: 0 },
    { bucket: "41+", count: 0 }
  ];

  projects.forEach((p) => {
    const roi = Number(p.expected_roi || 0);
    if (roi <= 10) buckets[0].count += 1;
    else if (roi <= 20) buckets[1].count += 1;
    else if (roi <= 30) buckets[2].count += 1;
    else if (roi <= 40) buckets[3].count += 1;
    else buckets[4].count += 1;
  });

  return buckets;
}

export function buildRiskDistribution(projects) {
  const map = { low: 0, medium: 0, high: 0 };
  projects.forEach((p) => {
    const risk = String(p.risk_level || "medium").toLowerCase();
    map[risk] = (map[risk] || 0) + 1;
  });
  return Object.entries(map).map(([name, value]) => ({ name, value }));
}

export function buildPriorityScores(projects) {
  return projects
    .map((p) => ({
      name: p.project_name,
      score:
        Number(p.strategic_alignment_score || 0) * 0.4 +
        Number(p.expected_roi || 0) * 0.4 +
        (p.risk_level === "low" ? 20 : p.risk_level === "medium" ? 10 : 4) * 0.2
    }))
    .sort((a, b) => b.score - a.score);
}

export function buildClusterPoints(projects) {
  return projects.map((p) => ({
    budget: Number(p.budget || 0),
    roi: Number(p.expected_roi || 0),
    cluster: p.cluster_id || 0,
    name: p.project_name
  }));
}
