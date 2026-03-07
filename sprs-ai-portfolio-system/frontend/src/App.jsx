import { Navigate, Route, Routes } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import AddProjectPage from "./pages/AddProjectPage";
import PortfolioTablePage from "./pages/PortfolioTablePage";
import AnalyticsPage from "./pages/AnalyticsPage";
import RecommendationsPage from "./pages/RecommendationsPage";
import Layout from "./components/Layout";
import { hasRole, isAuthenticated } from "./utils/auth";

function ProtectedRoute({ children, allowedRoles = [] }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  if (!hasRole(allowedRoles)) {
    return <Navigate to="/" replace />;
  }
  return children;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
        <Route index element={<DashboardPage />} />
        <Route
          path="add-project"
          element={
            <ProtectedRoute allowedRoles={["admin", "project_manager"]}>
              <AddProjectPage />
            </ProtectedRoute>
          }
        />
        <Route path="portfolio" element={<PortfolioTablePage />} />
        <Route
          path="analytics"
          element={
            <ProtectedRoute allowedRoles={["admin", "project_manager"]}>
              <AnalyticsPage />
            </ProtectedRoute>
          }
        />
        <Route path="recommendations" element={<RecommendationsPage />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}
