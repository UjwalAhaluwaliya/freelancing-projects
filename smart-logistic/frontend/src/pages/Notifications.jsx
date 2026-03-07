import { useState, useEffect } from 'react'
import API from '../api/axios'

const typeColors = {
  dispatch: 'bg-blue-100 text-blue-800',
  delivery: 'bg-green-100 text-green-800',
  delay: 'bg-red-100 text-red-800',
  system: 'bg-gray-100 text-gray-800',
}

const typeIcons = {
  dispatch: '🚀',
  delivery: '✅',
  delay: '⚠️',
  system: '🔧',
}

export default function Notifications() {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchNotifications = async () => {
    try {
      const res = await API.get('/notifications/')
      setNotifications(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchNotifications() }, [])

  const markAsRead = async (id) => {
    try {
      await API.put(`/notifications/${id}/read`)
      fetchNotifications()
    } catch (err) { console.error(err) }
  }

  const markAllRead = async () => {
    try {
      await API.put('/notifications/read-all')
      fetchNotifications()
    } catch (err) { console.error(err) }
  }

  if (loading) return <div className="text-center py-10">Loading notifications...</div>

  const unreadCount = notifications.filter((n) => !n.is_read).length

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
          <p className="text-sm text-gray-500 mt-1">{unreadCount} unread</p>
        </div>
        {unreadCount > 0 && (
          <button onClick={markAllRead}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
            Mark All Read
          </button>
        )}
      </div>

      <div className="space-y-3">
        {notifications.map((n) => (
          <div key={n.id}
            className={`bg-white rounded-xl shadow-sm border p-4 flex items-start gap-4 transition-colors ${
              n.is_read ? 'border-gray-100' : 'border-blue-200 bg-blue-50/30'
            }`}>
            <span className="text-2xl">{typeIcons[n.notification_type] || '📌'}</span>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h3 className={`font-medium ${n.is_read ? 'text-gray-700' : 'text-gray-900'}`}>{n.title}</h3>
                <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${typeColors[n.notification_type]}`}>
                  {n.notification_type}
                </span>
              </div>
              <p className="text-sm text-gray-600">{n.message}</p>
              <p className="text-xs text-gray-400 mt-1">{new Date(n.created_at).toLocaleString()}</p>
            </div>
            {!n.is_read && (
              <button onClick={() => markAsRead(n.id)}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs hover:bg-blue-100 whitespace-nowrap">
                Mark Read
              </button>
            )}
          </div>
        ))}
        {notifications.length === 0 && (
          <div className="text-center py-10 text-gray-500">No notifications yet</div>
        )}
      </div>
    </div>
  )
}
