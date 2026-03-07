import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../state/AuthContext";

export default function LoginPage() {
  const { login, loading, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    const result = await login(email, password);
    if (!result.success) {
      setError(result.message);
    }
  }

  return (
    <div className="auth-wrap">
      <div className="auth-layout">
        <section className="auth-hero">
          <p className="hero-chip">ORBITO ERP</p>
          <h1>Run Hiring, HR and AI Workflows in One Neural Dashboard</h1>
          <p className="muted">
            Modern HR ops with ATS pipeline, leave engine, achievement metrics and Gemini-powered
            screening.
          </p>
          <div className="hero-wave">
            <span />
            <span />
            <span />
            <span />
            <span />
            <span />
          </div>
        </section>
        <form className="auth-card" onSubmit={handleSubmit}>
          <h1>Welcome Back</h1>
          <p className="muted">Orbito ERP access portal</p>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="hr@orbito.ai"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="********"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
          {error ? <p className="error-text">{error}</p> : null}
          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
      </div>
    </div>
  );
}
