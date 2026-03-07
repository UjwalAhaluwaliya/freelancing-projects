import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import API from '../api/axios'

const StatCard = ({ title, value, color, icon }) => (
  <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500">{title}</p>
        <p className="text-2xl font-bold mt-1" style={{ color }}>{value}</p>
      </div>
      <span className="text-3xl">{icon}</span>
    </div>
  </div>
)

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [trends, setTrends] = useState([])
  const [shipments, setShipments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sumRes, trendRes, shipRes] = await Promise.all([
          API.get('/analytics/summary'),
          API.get('/analytics/trends'),
          API.get('/shipments/?limit=5'),
        ])
        setSummary(sumRes.data)
        setTrends(trendRes.data)
        setShipments(shipRes.data)
      } catch (err) {
        console.error('Dashboard fetch error:', err)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) return <div className="text-center py-10">Loading dashboard...</div>

  const statusColor = {
    pending: 'bg-yellow-100 text-yellow-800',
    assigned: 'bg-blue-100 text-blue-800',
    in_transit: 'bg-purple-100 text-purple-800',
    delivered: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard title="Total Shipments" value={summary?.total_shipments || 0} color="#3b82f6" icon="📦" />
        <StatCard title="Active Vehicles" value={summary?.active_vehicles || 0} color="#10b981" icon="🚛" />
        <StatCard title="On-Time Rate" value={`${summary?.on_time_rate || 0}%`} color="#f59e0b" icon="⏱️" />
        <StatCard title="Pending Orders" value={summary?.pending || 0} color="#ef4444" icon="⏳" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Trends Chart */}
        <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Monthly Shipment Trends</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 12 }} />
              <YAxis tick={{ fontSize: 12 }} />
              <Tooltip />
              <Bar dataKey="shipments" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Recent Shipments */}
        <div className="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h2 className="text-lg font-semibold mb-4">Recent Shipments</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-gray-500 border-b">
                  <th className="pb-2">Tracking #</th>
                  <th className="pb-2">Destination</th>
                  <th className="pb-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {shipments.map((s) => (
                  <tr key={s.id} className="border-b last:border-0">
                    <td className="py-2 font-mono text-xs">{s.tracking_number}</td>
                    <td className="py-2">{s.destination}</td>
                    <td className="py-2">
                      <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor[s.status] || ''}`}>
                        {s.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">In Transit</p>
          <p className="text-xl font-bold text-purple-600">{summary?.in_transit || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Delivered</p>
          <p className="text-xl font-bold text-green-600">{summary?.delivered || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Total Vehicles</p>
          <p className="text-xl font-bold text-blue-600">{summary?.total_vehicles || 0}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Total Drivers</p>
          <p className="text-xl font-bold text-indigo-600">{summary?.total_drivers || 0}</p>
        </div>
      </div>
    </div>
  )
}
