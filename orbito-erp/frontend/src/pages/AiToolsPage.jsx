import { useEffect, useState } from "react";
import api from "../lib/api";

function normalizeAiResult(data) {
  const analysis = data?.analysis || {};
  return {
    success: Boolean(data?.success),
    ai_source: data?.ai_source || data?.source || "unknown",
    shortlisted: Boolean(data?.shortlisted),
    threshold: Number(data?.threshold ?? 0),
    workflow: data?.workflow || null,
    analysis: {
      match_score: Number(analysis?.match_score ?? 0),
      recommendation: String(analysis?.recommendation || ""),
      summary: String(analysis?.summary || ""),
      strengths: Array.isArray(analysis?.strengths) ? analysis.strengths : [],
      missing_skills: Array.isArray(analysis?.missing_skills) ? analysis.missing_skills : [],
    },
  };
}

function toPrettyJson(value) {
  try {
    return JSON.stringify(value, null, 2);
  } catch {
    return "Unable to render response JSON safely.";
  }
}

function extractErrorMessage(err, fallback) {
  const detail = err?.response?.data?.detail;
  if (Array.isArray(detail)) {
    const msg = detail
      .map((item) => {
        const loc = Array.isArray(item?.loc) ? item.loc.join(".") : "field";
        return `${loc}: ${item?.msg || "invalid"}`;
      })
      .join(" | ");
    return msg || fallback;
  }
  if (typeof detail === "string") {
    return detail;
  }
  if (typeof err?.message === "string" && err.message) {
    return err.message;
  }
  return fallback;
}

function getAiSourceBadge(value) {
  const source = String(value || "unknown").toLowerCase();
  if (source.includes("local")) {
    return { label: "Local Fallback", className: "ai-badge ai-badge-local" };
  }
  if (source.includes("gemini")) {
    return { label: "Gemini", className: "ai-badge ai-badge-gemini" };
  }
  return { label: source || "unknown", className: "ai-badge ai-badge-unknown" };
}

export default function AiToolsPage() {
  const [jobForm, setJobForm] = useState({
    title: "",
    skills: "",
    experience: "",
    department: "",
  });
  const [jobDescription, setJobDescription] = useState("");
  const [jobSource, setJobSource] = useState("");

  const [scoreForm, setScoreForm] = useState({
    resume_text: "",
    job_description: "",
    shortlist_threshold: 70,
  });
  const [scoreResult, setScoreResult] = useState(null);
  const [pdfForm, setPdfForm] = useState({
    file: null,
    job_description: "",
    shortlist_threshold: 70,
    candidate_id: "",
  });
  const [pdfScoreResult, setPdfScoreResult] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [policyQuestion, setPolicyQuestion] = useState("");
  const [policyReply, setPolicyReply] = useState("");
  const [policySource, setPolicySource] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadCandidates() {
      try {
        const response = await api.get("/candidates");
        setCandidates(response.data?.data || []);
      } catch {
        setCandidates([]);
      }
    }
    loadCandidates();
  }, []);

  async function generateJobDescription(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setJobDescription("");
    setJobSource("");
    try {
      const response = await api.post("/ai/generate-job", jobForm);
      setJobDescription(response.data?.job_description || "");
      setJobSource(response.data?.ai_source || response.data?.source || "unknown");
    } catch (err) {
      setError(extractErrorMessage(err, "Job description generation failed"));
    } finally {
      setLoading(false);
    }
  }

  async function scoreResume(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setScoreResult(null);
    try {
      const response = await api.post("/ai/score-resume", scoreForm);
      setScoreResult(normalizeAiResult(response.data));
    } catch (err) {
      setError(extractErrorMessage(err, "Resume scoring failed"));
    } finally {
      setLoading(false);
    }
  }

  async function askPolicy(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPolicyReply("");
    setPolicySource("");
    try {
      const response = await api.post("/ai/policy-chat", { question: policyQuestion });
      const reply = response.data?.reply || response.data?.message || JSON.stringify(response.data);
      setPolicySource(response.data?.ai_source || response.data?.source || "unknown");
      setPolicyReply(reply);
    } catch (err) {
      setError(extractErrorMessage(err, "Policy chatbot request failed"));
    } finally {
      setLoading(false);
    }
  }

  async function scoreResumePdf(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPdfScoreResult(null);
    try {
      const formData = new FormData();
      formData.append("resume_file", pdfForm.file);
      formData.append("job_description", pdfForm.job_description);
      formData.append("shortlist_threshold", String(pdfForm.shortlist_threshold));
      if (pdfForm.candidate_id) {
        formData.append("candidate_id", pdfForm.candidate_id);
      }
      const response = await api.post("/ai/score-resume-pdf", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setPdfScoreResult(normalizeAiResult(response.data));
    } catch (err) {
      setError(extractErrorMessage(err, "PDF resume scoring failed"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section>
      <h2>AI Hiring Tools</h2>
      <p className="muted">Generate job descriptions and automate resume shortlisting.</p>
      {error ? <p className="error-text">{error}</p> : null}

      <div className="split-grid">
        <form className="card form-card" onSubmit={generateJobDescription}>
          <h3>Job Description Generator</h3>
          <input
            placeholder="Job title"
            value={jobForm.title}
            onChange={(event) => setJobForm({ ...jobForm, title: event.target.value })}
            required
          />
          <input
            placeholder="Skills (comma separated)"
            value={jobForm.skills}
            onChange={(event) => setJobForm({ ...jobForm, skills: event.target.value })}
            required
          />
          <input
            placeholder="Experience"
            value={jobForm.experience}
            onChange={(event) => setJobForm({ ...jobForm, experience: event.target.value })}
            required
          />
          <input
            placeholder="Department"
            value={jobForm.department}
            onChange={(event) => setJobForm({ ...jobForm, department: event.target.value })}
            required
          />
          <button type="submit" disabled={loading}>
            Generate
          </button>
          {jobDescription ? (
            <span className={getAiSourceBadge(jobSource).className}>
              AI Source: {getAiSourceBadge(jobSource).label}
            </span>
          ) : null}
          {jobDescription ? <pre className="result-block">{jobDescription}</pre> : null}
        </form>

        <form className="card form-card" onSubmit={scoreResume}>
          <h3>Resume Scoring</h3>
          <textarea
            placeholder="Paste resume text"
            value={scoreForm.resume_text}
            onChange={(event) => setScoreForm({ ...scoreForm, resume_text: event.target.value })}
            required
          />
          <textarea
            placeholder="Paste job description"
            value={scoreForm.job_description}
            onChange={(event) =>
              setScoreForm({ ...scoreForm, job_description: event.target.value })
            }
            required
          />
          <input
            type="number"
            min="0"
            max="100"
            value={scoreForm.shortlist_threshold}
            onChange={(event) =>
              setScoreForm({
                ...scoreForm,
                shortlist_threshold: Number(event.target.value),
              })
            }
          />
          <button type="submit" disabled={loading}>
            Score Resume
          </button>
          {scoreResult ? (
            <span className={getAiSourceBadge(scoreResult.ai_source).className}>
              AI Source: {getAiSourceBadge(scoreResult.ai_source).label}
            </span>
          ) : null}
          {scoreResult ? (
            <pre className="result-block">{toPrettyJson(scoreResult)}</pre>
          ) : null}
        </form>

        <form className="card form-card" onSubmit={scoreResumePdf}>
          <h3>Resume Scoring (PDF Upload)</h3>
          <select
            value={pdfForm.candidate_id}
            onChange={(event) =>
              setPdfForm({ ...pdfForm, candidate_id: event.target.value })
            }
          >
            <option value="">Select candidate (optional)</option>
            {candidates.map((c) => (
              <option key={c.id} value={c.id}>
                {c.full_name} ({c.email})
              </option>
            ))}
          </select>
          <input
            type="file"
            accept="application/pdf"
            onChange={(event) =>
              setPdfForm({ ...pdfForm, file: event.target.files?.[0] || null })
            }
            required
          />
          <textarea
            placeholder="Paste job description"
            value={pdfForm.job_description}
            onChange={(event) =>
              setPdfForm({ ...pdfForm, job_description: event.target.value })
            }
            required
          />
          <input
            type="number"
            min="0"
            max="100"
            value={pdfForm.shortlist_threshold}
            onChange={(event) =>
              setPdfForm({
                ...pdfForm,
                shortlist_threshold: Number(event.target.value),
              })
            }
          />
          <button type="submit" disabled={loading || !pdfForm.file}>
            Score PDF Resume
          </button>
          {pdfScoreResult ? (
            <span className={getAiSourceBadge(pdfScoreResult.ai_source).className}>
              AI Source: {getAiSourceBadge(pdfScoreResult.ai_source).label}
            </span>
          ) : null}
          {pdfScoreResult ? (
            <pre className="result-block">{toPrettyJson(pdfScoreResult)}</pre>
          ) : null}
        </form>

        <form className="card form-card" onSubmit={askPolicy}>
          <h3>Policy Chatbot</h3>
          <textarea
            placeholder="Ask HR policy question"
            value={policyQuestion}
            onChange={(event) => setPolicyQuestion(event.target.value)}
            required
          />
          <button type="submit" disabled={loading}>
            Ask
          </button>
          {policyReply ? (
            <span className={getAiSourceBadge(policySource).className}>
              AI Source: {getAiSourceBadge(policySource).label}
            </span>
          ) : null}
          {policyReply ? <pre className="result-block">{policyReply}</pre> : null}
        </form>
      </div>
    </section>
  );
}
