import { useEffect, useMemo, useState } from "react";
import api from "../lib/api";

export default function AdminUsersPage() {
  const [profiles, setProfiles] = useState([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [form, setForm] = useState({
    email: "",
    full_name: "",
    role: "employee",
    password: "",
  });
  const [editForm, setEditForm] = useState({
    profile_id: "",
    full_name: "",
    role: "employee",
    department: "",
    password: "",
  });
  const [inlineEditId, setInlineEditId] = useState("");

  const selectedProfile = useMemo(
    () => profiles.find((p) => p.id === editForm.profile_id) || null,
    [profiles, editForm.profile_id],
  );

  async function loadProfiles() {
    try {
      const response = await api.get("/profiles");
      setProfiles(response.data?.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load users");
    }
  }

  useEffect(() => {
    loadProfiles();
  }, []);

  useEffect(() => {
    if (!selectedProfile) {
      return;
    }
    setEditForm((prev) => ({
      ...prev,
      full_name: selectedProfile.full_name || "",
      role: selectedProfile.role || "employee",
      department: selectedProfile.department || "",
      password: "",
    }));
  }, [selectedProfile]);

  function startInlineEdit(profile) {
    setInlineEditId(profile.id);
    setEditForm({
      profile_id: profile.id,
      full_name: profile.full_name || "",
      role: profile.role || "employee",
      department: profile.department || "",
      password: "",
    });
  }

  function cancelInlineEdit() {
    setInlineEditId("");
    setEditForm((prev) => ({ ...prev, password: "" }));
  }

  async function createUser(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/auth/register", null, {
        params: {
          email: form.email,
          full_name: form.full_name,
          role: form.role,
          password: form.password,
        },
      });
      setForm({ email: "", full_name: "", role: "employee", password: "" });
      setSuccess("User created.");
      await loadProfiles();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to create user");
    }
  }

  async function updateUser(event) {
    event.preventDefault();
    setError("");
    setSuccess("");
    if (!editForm.profile_id) {
      setError("Select a user to update.");
      return;
    }
    try {
      const payload = {
        full_name: editForm.full_name,
        role: editForm.role,
        department: editForm.department,
      };
      if (editForm.password.trim()) {
        payload.password = editForm.password.trim();
      }
      await api.put(`/profiles/${editForm.profile_id}`, payload);
      setSuccess("User updated successfully.");
      setEditForm((prev) => ({ ...prev, password: "" }));
      setInlineEditId("");
      await loadProfiles();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update user");
    }
  }

  return (
    <section>
      <h2>User Management</h2>
      <p className="muted">Create, edit role/department, and reset user password.</p>
      {error ? <p className="error-text">{error}</p> : null}
      {success ? <p className="success-text">{success}</p> : null}

      <div className="split-grid">
        <form className="card form-card" onSubmit={createUser}>
          <h3>Create User</h3>
          <input
            type="email"
            placeholder="Email"
            value={form.email}
            onChange={(event) => setForm({ ...form, email: event.target.value })}
            required
          />
          <input
            placeholder="Full name"
            value={form.full_name}
            onChange={(event) => setForm({ ...form, full_name: event.target.value })}
            required
          />
          <select
            value={form.role}
            onChange={(event) => setForm({ ...form, role: event.target.value })}
          >
            <option value="employee">employee</option>
            <option value="hr">hr</option>
            <option value="admin">admin</option>
          </select>
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
            required
          />
          <button type="submit">Create</button>
        </form>

        <form className="card form-card" onSubmit={updateUser}>
          <h3>Update Existing User</h3>
          <select
            value={editForm.profile_id}
            onChange={(event) => setEditForm({ ...editForm, profile_id: event.target.value })}
            required
          >
            <option value="">Select user</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>
                {p.full_name} ({p.email})
              </option>
            ))}
          </select>
          <input
            placeholder="Full name"
            value={editForm.full_name}
            onChange={(event) => setEditForm({ ...editForm, full_name: event.target.value })}
            required
          />
          <select
            value={editForm.role}
            onChange={(event) => setEditForm({ ...editForm, role: event.target.value })}
          >
            <option value="employee">employee</option>
            <option value="hr">hr</option>
            <option value="admin">admin</option>
          </select>
          <input
            placeholder="Department"
            value={editForm.department}
            onChange={(event) => setEditForm({ ...editForm, department: event.target.value })}
          />
          <input
            type="password"
            placeholder="New password (optional)"
            value={editForm.password}
            onChange={(event) => setEditForm({ ...editForm, password: event.target.value })}
          />
          <button type="submit">Update</button>
        </form>
      </div>

      <div className="table-wrap">
        <div className="filter-row">
          <h3>Existing Users</h3>
        </div>
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Department</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {profiles.map((p) => (
              <tr key={p.id}>
                <td>
                  {inlineEditId === p.id ? (
                    <input
                      value={editForm.full_name}
                      onChange={(event) =>
                        setEditForm({ ...editForm, full_name: event.target.value })
                      }
                    />
                  ) : (
                    p.full_name
                  )}
                </td>
                <td>{p.email}</td>
                <td>
                  {inlineEditId === p.id ? (
                    <select
                      value={editForm.role}
                      onChange={(event) => setEditForm({ ...editForm, role: event.target.value })}
                    >
                      <option value="employee">employee</option>
                      <option value="hr">hr</option>
                      <option value="admin">admin</option>
                    </select>
                  ) : (
                    p.role
                  )}
                </td>
                <td>
                  {inlineEditId === p.id ? (
                    <input
                      value={editForm.department}
                      onChange={(event) =>
                        setEditForm({ ...editForm, department: event.target.value })
                      }
                      placeholder="Department"
                    />
                  ) : (
                    p.department || "-"
                  )}
                </td>
                <td>
                  {inlineEditId === p.id ? (
                    <>
                      <input
                        type="password"
                        placeholder="Set new password (optional)"
                        value={editForm.password}
                        onChange={(event) =>
                          setEditForm({ ...editForm, password: event.target.value })
                        }
                      />
                      <div className="action-row">
                        <button type="button" className="table-btn" onClick={updateUser}>
                          Save
                        </button>
                        <button
                          type="button"
                          className="ghost-button table-btn"
                          onClick={cancelInlineEdit}
                        >
                          Cancel
                        </button>
                      </div>
                    </>
                  ) : (
                    <button type="button" className="table-btn" onClick={() => startInlineEdit(p)}>
                      Edit
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
