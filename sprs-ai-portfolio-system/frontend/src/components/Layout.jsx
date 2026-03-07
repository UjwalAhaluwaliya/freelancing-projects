import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { getSession, logoutUser } from "../utils/auth";

const allLinks = [
  { to: "/", label: "Dashboard", roles: ["admin", "project_manager", "employee"] },
  { to: "/add-project", label: "Add Project", roles: ["admin", "project_manager"] },
  { to: "/portfolio", label: "Portfolio Table", roles: ["admin", "project_manager", "employee"] },
  { to: "/analytics", label: "Analytics", roles: ["admin", "project_manager"] },
  { to: "/recommendations", label: "Recommendations", roles: ["admin", "project_manager", "employee"] }
];

export default function Layout() {
  const navigate = useNavigate();
  const session = getSession();
  const role = session?.user?.role || "employee";

  const links = allLinks.filter((link) => link.roles.includes(role));

  function handleLogout() {
    logoutUser();
    navigate("/login", { replace: true });
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1 className="brand">SPRS</h1>
        <p className="brand-subtitle">Strategic Portfolio Intelligence</p>
        <div className="role-badge">Role: {role.replace("_", " ")}</div>

        <nav className="side-nav">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              end={link.to === "/"}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>
        <button className="btn btn-secondary" onClick={handleLogout}>
          Logout
        </button>
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
