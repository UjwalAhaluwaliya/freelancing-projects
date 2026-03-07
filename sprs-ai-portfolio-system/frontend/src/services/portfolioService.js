import api from "./api";

export async function login(payload) {
  const { data } = await api.post("/auth/login", payload);
  return data;
}

export async function addProject(payload) {
  const { data } = await api.post("/add_project", payload);
  return data;
}

export async function getProjects() {
  const { data } = await api.get("/projects");
  return data;
}

export async function analyzePortfolio(payload = {}) {
  const { data } = await api.post("/analyze_portfolio", payload);
  return data;
}

export async function getRecommendations(analysisId = "") {
  const { data } = await api.get("/recommendations", {
    params: analysisId ? { analysis_id: analysisId } : {}
  });
  return data;
}

export async function getDashboardMetrics() {
  const { data } = await api.get("/dashboard_metrics");
  return data;
}
