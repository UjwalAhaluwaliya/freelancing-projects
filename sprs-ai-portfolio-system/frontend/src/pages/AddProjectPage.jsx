import { useState } from "react";
import ProjectForm from "../components/ProjectForm";
import { addProject } from "../services/portfolioService";

export default function AddProjectPage() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleSubmit(payload) {
    setLoading(true);
    setMessage("");
    try {
      await addProject(payload);
      setMessage("Project added successfully.");
    } catch (error) {
      setMessage(error.response?.data?.message || "Failed to add project.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page-grid">
      <ProjectForm onSubmit={handleSubmit} loading={loading} />
      {message ? <p className="notice">{message}</p> : null}
    </div>
  );
}
