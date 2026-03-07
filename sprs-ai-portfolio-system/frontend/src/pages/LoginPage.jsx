import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../services/portfolioService";
import { setSession } from "../utils/auth";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await login({ email, password });
      setSession({
        access_token: response.data.access_token,
        user: response.data.user,
        loggedInAt: Date.now()
      });
      navigate("/", { replace: true });
    } catch (err) {
      setError(err.response?.data?.message || err.message || "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-shell">
      <div className="login-orb orb-one" />
      <div className="login-orb orb-two" />

      <section className="login-layout">
        <aside className="login-hero">
          <p className="hero-kicker">AI Powered Portfolio Intelligence</p>
          <h1>Strategic Portfolio Rationalization</h1>
          <p>
            Turn complex project portfolios into clear decisions with ML-guided recommendations, risk signals,
            and optimization insights.
          </p>
          <div className="hero-tags">
            <span>RETAIN</span>
            <span>ENHANCE</span>
            <span>CONSOLIDATE</span>
            <span>DEFER</span>
            <span>RETIRE</span>
          </div>
          <div className="demo-accounts">
            <p>Demo Accounts</p>
            <small>Admin: admin@sprs.local / admin123</small>
            <small>Manager: pm@sprs.local / pm123</small>
            <small>Employee: employee@sprs.local / employee123</small>
          </div>
        </aside>

        <form className="card login-card modern-login" onSubmit={handleSubmit}>
          <h2>Welcome Back</h2>
          <p className="login-subtitle">Sign in to access your portfolio command center.</p>

          <label className="field-label" htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@company.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <label className="field-label" htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />

          {error ? <p className="error">{error}</p> : null}
          <button className="btn login-btn" type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Enter Platform"}
          </button>
        </form>
      </section>
    </div>
  );
}
