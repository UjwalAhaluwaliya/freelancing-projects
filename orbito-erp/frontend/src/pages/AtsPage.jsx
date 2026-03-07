import { useEffect, useMemo, useState } from "react";
import api from "../lib/api";

const STAGES = ["applied", "screening", "interview", "offer", "hired", "rejected"];
const PAGE_SIZE = 5;

const initialCandidate = {
  full_name: "",
  email: "",
  phone: "",
  skills: "",
  total_experience: "",
  resume_url: "",
};

const initialJob = {
  title: "",
  description: "",
  location: "",
  employment_type: "",
  experience_level: "",
};

function Pagination({ page, totalPages, onPageChange }) {
  return (
    <div className="pager">
      <button type="button" onClick={() => onPageChange(page - 1)} disabled={page <= 1}>
        Prev
      </button>
      <span>
        Page {page} / {totalPages}
      </span>
      <button
        type="button"
        onClick={() => onPageChange(page + 1)}
        disabled={page >= totalPages}
      >
        Next
      </button>
    </div>
  );
}

function slicePage(rows, page) {
  const start = (page - 1) * PAGE_SIZE;
  return rows.slice(start, start + PAGE_SIZE);
}

export default function AtsPage() {
  const [applications, setApplications] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [candidateForm, setCandidateForm] = useState(initialCandidate);
  const [jobForm, setJobForm] = useState(initialJob);
  const [applicationForm, setApplicationForm] = useState({ candidate_id: "", job_id: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [savingId, setSavingId] = useState(null);
  const [loading, setLoading] = useState(false);

  const [candidateSearch, setCandidateSearch] = useState("");
  const [jobSearch, setJobSearch] = useState("");
  const [applicationStageFilter, setApplicationStageFilter] = useState("all");

  const [candidatePage, setCandidatePage] = useState(1);
  const [jobPage, setJobPage] = useState(1);
  const [applicationPage, setApplicationPage] = useState(1);

  const candidateOptions = useMemo(
    () =>
      candidates.map((item) => ({
        id: item.id,
        label: `${item.full_name} (${item.email})`,
      })),
    [candidates],
  );

  const jobOptions = useMemo(
    () =>
      jobs.map((item) => ({
        id: item.id,
        label: `${item.title}${item.location ? ` - ${item.location}` : ""}`,
      })),
    [jobs],
  );

  const filteredCandidates = useMemo(() => {
    const q = candidateSearch.trim().toLowerCase();
    if (!q) return candidates;
    return candidates.filter((item) =>
      `${item.full_name || ""} ${item.email || ""} ${item.phone || ""}`.toLowerCase().includes(q),
    );
  }, [candidateSearch, candidates]);

  const filteredJobs = useMemo(() => {
    const q = jobSearch.trim().toLowerCase();
    if (!q) return jobs;
    return jobs.filter((item) =>
      `${item.title || ""} ${item.location || ""} ${item.experience_level || ""}`
        .toLowerCase()
        .includes(q),
    );
  }, [jobSearch, jobs]);

  const filteredApplications = useMemo(() => {
    if (applicationStageFilter === "all") return applications;
    return applications.filter((item) => item.stage === applicationStageFilter);
  }, [applicationStageFilter, applications]);

  const totalCandidatePages = Math.max(1, Math.ceil(filteredCandidates.length / PAGE_SIZE));
  const totalJobPages = Math.max(1, Math.ceil(filteredJobs.length / PAGE_SIZE));
  const totalApplicationPages = Math.max(1, Math.ceil(filteredApplications.length / PAGE_SIZE));

  const visibleCandidates = slicePage(filteredCandidates, candidatePage);
  const visibleJobs = slicePage(filteredJobs, jobPage);
  const visibleApplications = slicePage(filteredApplications, applicationPage);

  async function loadAtsData() {
    setLoading(true);
    try {
      const [applicationsRes, candidatesRes, jobsRes] = await Promise.all([
        api.get("/applications"),
        api.get("/candidates"),
        api.get("/jobs"),
      ]);
      setApplications(applicationsRes.data?.data || []);
      setCandidates(candidatesRes.data?.data || []);
      setJobs(jobsRes.data?.data || []);
      setError("");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load ATS data");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadAtsData();
  }, []);

  useEffect(() => {
    setCandidatePage(1);
  }, [candidateSearch]);

  useEffect(() => {
    setJobPage(1);
  }, [jobSearch]);

  useEffect(() => {
    setApplicationPage(1);
  }, [applicationStageFilter]);

  useEffect(() => {
    if (candidatePage > totalCandidatePages) setCandidatePage(totalCandidatePages);
  }, [candidatePage, totalCandidatePages]);

  useEffect(() => {
    if (jobPage > totalJobPages) setJobPage(totalJobPages);
  }, [jobPage, totalJobPages]);

  useEffect(() => {
    if (applicationPage > totalApplicationPages) setApplicationPage(totalApplicationPages);
  }, [applicationPage, totalApplicationPages]);

  async function updateStage(applicationId, stage) {
    setSavingId(applicationId);
    setError("");
    setSuccess("");
    try {
      await api.put(`/applications/${applicationId}/stage`, { stage });
      await loadAtsData();
      setSuccess("Application stage updated.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update stage");
    } finally {
      setSavingId(null);
    }
  }

  async function createCandidate(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/candidates", {
        ...candidateForm,
        skills: candidateForm.skills
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean),
        total_experience: candidateForm.total_experience
          ? Number(candidateForm.total_experience)
          : null,
      });
      setCandidateForm(initialCandidate);
      await loadAtsData();
      setSuccess("Candidate created.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to create candidate");
    }
  }

  async function createJob(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/jobs", {
        ...jobForm,
      });
      setJobForm(initialJob);
      await loadAtsData();
      setSuccess("Job created.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to create job");
    }
  }

  async function createApplication(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/applications", applicationForm);
      setApplicationForm({ candidate_id: "", job_id: "" });
      await loadAtsData();
      setSuccess("Application created.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to create application");
    }
  }

  return (
    <section>
      <h2>ATS Pipeline</h2>
      <p className="muted">Create records, filter data, and move applications across stages.</p>
      {error ? <p className="error-text">{error}</p> : null}
      {success ? <p className="success-text">{success}</p> : null}

      <div className="split-grid">
        <form className="card form-card" onSubmit={createCandidate}>
          <h3>Add Candidate</h3>
          <input
            placeholder="Full name"
            value={candidateForm.full_name}
            onChange={(event) =>
              setCandidateForm({ ...candidateForm, full_name: event.target.value })
            }
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={candidateForm.email}
            onChange={(event) => setCandidateForm({ ...candidateForm, email: event.target.value })}
            required
          />
          <input
            placeholder="Phone"
            value={candidateForm.phone}
            onChange={(event) => setCandidateForm({ ...candidateForm, phone: event.target.value })}
          />
          <input
            placeholder="Skills (comma separated)"
            value={candidateForm.skills}
            onChange={(event) => setCandidateForm({ ...candidateForm, skills: event.target.value })}
          />
          <input
            type="number"
            min="0"
            placeholder="Total Experience (years)"
            value={candidateForm.total_experience}
            onChange={(event) =>
              setCandidateForm({ ...candidateForm, total_experience: event.target.value })
            }
          />
          <input
            placeholder="Resume URL"
            value={candidateForm.resume_url}
            onChange={(event) =>
              setCandidateForm({ ...candidateForm, resume_url: event.target.value })
            }
          />
          <button type="submit">Create Candidate</button>
        </form>

        <form className="card form-card" onSubmit={createJob}>
          <h3>Add Job</h3>
          <input
            placeholder="Job title"
            value={jobForm.title}
            onChange={(event) => setJobForm({ ...jobForm, title: event.target.value })}
            required
          />
          <input
            placeholder="Location"
            value={jobForm.location}
            onChange={(event) => setJobForm({ ...jobForm, location: event.target.value })}
          />
          <input
            placeholder="Employment type"
            value={jobForm.employment_type}
            onChange={(event) => setJobForm({ ...jobForm, employment_type: event.target.value })}
          />
          <input
            placeholder="Experience level"
            value={jobForm.experience_level}
            onChange={(event) => setJobForm({ ...jobForm, experience_level: event.target.value })}
          />
          <textarea
            placeholder="Description"
            value={jobForm.description}
            onChange={(event) => setJobForm({ ...jobForm, description: event.target.value })}
            required
          />
          <button type="submit">Create Job</button>
        </form>

        <form className="card form-card" onSubmit={createApplication}>
          <h3>Create Application</h3>
          <select
            value={applicationForm.candidate_id}
            onChange={(event) =>
              setApplicationForm({ ...applicationForm, candidate_id: event.target.value })
            }
            required
          >
            <option value="">Select candidate</option>
            {candidateOptions.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
          <select
            value={applicationForm.job_id}
            onChange={(event) => setApplicationForm({ ...applicationForm, job_id: event.target.value })}
            required
          >
            <option value="">Select job</option>
            {jobOptions.map((item) => (
              <option key={item.id} value={item.id}>
                {item.label}
              </option>
            ))}
          </select>
          <button type="submit">Create Application</button>
        </form>
      </div>

      <div className="table-wrap">
        <div className="filter-row">
          <h3>Applications</h3>
          <select
            value={applicationStageFilter}
            onChange={(event) => setApplicationStageFilter(event.target.value)}
          >
            <option value="all">All stages</option>
            {STAGES.map((stage) => (
              <option key={stage} value={stage}>
                {stage}
              </option>
            ))}
          </select>
        </div>
        <table>
          <thead>
            <tr>
              <th>Application ID</th>
              <th>Candidate ID</th>
              <th>Job ID</th>
              <th>Current Stage</th>
              <th>Move Stage</th>
            </tr>
          </thead>
          <tbody>
            {visibleApplications.map((item) => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td>{item.candidate_id}</td>
                <td>{item.job_id}</td>
                <td>{item.stage}</td>
                <td>
                  <select
                    disabled={savingId === item.id || loading}
                    value={item.stage}
                    onChange={(event) => updateStage(item.id, event.target.value)}
                  >
                    {STAGES.map((stage) => (
                      <option key={stage} value={stage}>
                        {stage}
                      </option>
                    ))}
                  </select>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <Pagination
          page={applicationPage}
          totalPages={totalApplicationPages}
          onPageChange={setApplicationPage}
        />
      </div>

      <div className="split-grid">
        <div className="table-wrap">
          <div className="filter-row">
            <h3>Candidates</h3>
            <input
              placeholder="Search candidate"
              value={candidateSearch}
              onChange={(event) => setCandidateSearch(event.target.value)}
            />
          </div>
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Experience</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {visibleCandidates.map((item) => (
                <tr key={item.id}>
                  <td>{item.full_name}</td>
                  <td>{item.email}</td>
                  <td>{item.phone || "-"}</td>
                  <td>{item.total_experience ?? "-"}</td>
                  <td>{item.overall_score ?? "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <Pagination
            page={candidatePage}
            totalPages={totalCandidatePages}
            onPageChange={setCandidatePage}
          />
        </div>

        <div className="table-wrap">
          <div className="filter-row">
            <h3>Jobs</h3>
            <input
              placeholder="Search jobs"
              value={jobSearch}
              onChange={(event) => setJobSearch(event.target.value)}
            />
          </div>
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Location</th>
                <th>Type</th>
                <th>Experience</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {visibleJobs.map((item) => (
                <tr key={item.id}>
                  <td>{item.title}</td>
                  <td>{item.location || "-"}</td>
                  <td>{item.employment_type || "-"}</td>
                  <td>{item.experience_level || "-"}</td>
                  <td>{item.status || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <Pagination page={jobPage} totalPages={totalJobPages} onPageChange={setJobPage} />
        </div>
      </div>
    </section>
  );
}
