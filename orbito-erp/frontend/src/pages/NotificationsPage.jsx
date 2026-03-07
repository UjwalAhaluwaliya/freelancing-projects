import { useEffect, useState } from "react";
import api from "../lib/api";

export default function NotificationsPage() {
  const [notifications, setNotifications] = useState([]);
  const [error, setError] = useState("");

  async function loadNotifications() {
    try {
      const response = await api.get("/notifications");
      setNotifications(response.data?.data || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load notifications");
    }
  }

  useEffect(() => {
    loadNotifications();
  }, []);

  async function markAsRead(id) {
    try {
      await api.put(`/notifications/${id}/read`);
      await loadNotifications();
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update notification");
    }
  }

  return (
    <section>
      <h2>Notifications</h2>
      <p className="muted">Track leave, ATS and hiring alerts.</p>
      {error ? <p className="error-text">{error}</p> : null}
      <div className="cards-grid">
        {notifications.map((item) => (
          <article key={item.id} className={item.is_read ? "card" : "card unread-card"}>
            <h3>{item.title}</h3>
            <p>{item.message}</p>
            <small>{new Date(item.created_at).toLocaleString()}</small>
            {!item.is_read ? (
              <button type="button" onClick={() => markAsRead(item.id)}>
                Mark as read
              </button>
            ) : null}
          </article>
        ))}
      </div>
    </section>
  );
}
