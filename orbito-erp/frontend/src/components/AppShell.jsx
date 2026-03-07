import { Link, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../state/AuthContext";

function NavItem({ to, label }) {
  const location = useLocation();
  const isActive = location.pathname === to;
  return (
    <Link className={isActive ? "nav-item active" : "nav-item"} to={to}>
      {label}
    </Link>
  );
}

export default function AppShell() {
  const { role, logout } = useAuth();

  const roleLinks = {
    admin: [
      { to: "/dashboard", label: "Admin Overview" },
      { to: "/admin/users", label: "Users" },
      { to: "/hr/ats", label: "ATS" },
      { to: "/hr/ai", label: "AI Tools" },
      { to: "/notifications", label: "Notifications" },
    ],
    hr: [
      { to: "/dashboard", label: "HR Overview" },
      { to: "/hr/ats", label: "ATS" },
      { to: "/hr/interviews", label: "Interviews" },
      { to: "/hr/leaves", label: "Leave Approvals" },
      { to: "/hr/ai", label: "AI Tools" },
      { to: "/notifications", label: "Notifications" },
    ],
    employee: [
      { to: "/dashboard", label: "My Dashboard" },
      { to: "/employee/leave", label: "Leave" },
      { to: "/notifications", label: "Notifications" },
    ],
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="brand-title">Orbito ERP</p>
          <p className="brand-subtitle">{role?.toUpperCase() || "USER"}</p>
        </div>
        <nav className="nav-list">
          {(roleLinks[role] || []).map((item) => (
            <NavItem key={item.to} to={item.to} label={item.label} />
          ))}
        </nav>
        <button type="button" className="ghost-button" onClick={logout}>
          Logout
        </button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
