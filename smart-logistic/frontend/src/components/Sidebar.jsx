import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊', roles: ['admin', 'manager', 'driver', 'customer'] },
  { path: '/shipments', label: 'Shipments', icon: '📦', roles: ['admin', 'manager', 'driver', 'customer'] },
  { path: '/vehicles', label: 'Vehicles', icon: '🚛', roles: ['admin', 'manager'] },
  { path: '/tracking', label: 'Tracking', icon: '📍', roles: ['admin', 'manager', 'driver', 'customer'] },
  { path: '/route-optimization', label: 'Route Optimization', icon: '🗺️', roles: ['admin', 'manager'] },
  { path: '/demand-forecast', label: 'Demand Forecast', icon: '📈', roles: ['admin', 'manager'] },
  { path: '/analytics', label: 'Analytics', icon: '📉', roles: ['admin', 'manager'] },
  { path: '/notifications', label: 'Notifications', icon: '🔔', roles: ['admin', 'manager', 'driver', 'customer'] },
  { path: '/users', label: 'User Management', icon: '👥', roles: ['admin'] },
  { path: '/chat', label: 'Help Chat', icon: '💬', roles: ['admin','manager','driver','customer'] },
]

export default function Sidebar() {
  const { user, logout } = useAuth()

  const filteredItems = navItems.filter((item) => item.roles.includes(user?.role))

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen flex flex-col">
      <div className="p-4 border-b border-gray-700">
        <h1 className="text-xl font-bold">AI Logistics</h1>
        <p className="text-sm text-gray-400 mt-1">{user?.full_name}</p>
        <span className="inline-block mt-1 px-2 py-0.5 text-xs bg-blue-600 rounded-full capitalize">
          {user?.role}
        </span>
      </div>

      <nav className="flex-1 p-2">
        {filteredItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg mb-1 transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <span>{item.icon}</span>
            <span className="text-sm">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-4 border-t border-gray-700">
        <button
          onClick={logout}
          className="w-full px-3 py-2 text-sm text-gray-300 hover:bg-gray-800 hover:text-white rounded-lg transition-colors"
        >
          Logout
        </button>
      </div>
    </aside>
  )
}
