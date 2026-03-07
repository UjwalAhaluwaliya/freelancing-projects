import { Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./state/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import AppShell from "./components/AppShell";
import LoginPage from "./pages/LoginPage";
import HrDashboard from "./pages/HrDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";
import AtsPage from "./pages/AtsPage";
import AiToolsPage from "./pages/AiToolsPage";
import LeavePage from "./pages/LeavePage";
import NotificationsPage from "./pages/NotificationsPage";
import HrInterviewsPage from "./pages/HrInterviewsPage";
import HrLeaveApprovalsPage from "./pages/HrLeaveApprovalsPage";
import AdminUsersPage from "./pages/AdminUsersPage";

function DashboardEntry() {
  const { role } = useAuth();
  if (role === "admin") return <AdminDashboard />;
  if (role === "employee") return <EmployeeDashboard />;
  return <HrDashboard />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<DashboardEntry />} />
        <Route
          path="/hr/ats"
          element={
            <ProtectedRoute roles={["hr", "admin"]}>
              <AtsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/hr/ai"
          element={
            <ProtectedRoute roles={["hr", "admin"]}>
              <AiToolsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/hr/interviews"
          element={
            <ProtectedRoute roles={["hr", "admin"]}>
              <HrInterviewsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/hr/leaves"
          element={
            <ProtectedRoute roles={["hr", "admin"]}>
              <HrLeaveApprovalsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/users"
          element={
            <ProtectedRoute roles={["admin"]}>
              <AdminUsersPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/employee/leave"
          element={
            <ProtectedRoute roles={["employee"]}>
              <LeavePage />
            </ProtectedRoute>
          }
        />
        <Route path="/notifications" element={<NotificationsPage />} />
      </Route>

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
