import { useState, useEffect } from 'react'
import {
  PieChart, Pie, Cell, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import API from '../api/axios'

const STATUS_COLORS = {
  pending: '#f59e0b',
  assigned: '#3b82f6',
  in_transit: '#8b5cf6',
  delivered: '#10b981',
  cancelled: '#ef4444',
}

export default function Analytics() {
  const [performance, setPerformance] = useState([])
  const [fuel, setFuel] = useState([])
  const [trends, setTrends] = useState([])
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [perfRes, fuelRes, trendRes, sumRes] = await Promise.all([
          API.get('/analytics/delivery-performance'),
          API.get('/analytics/fuel-report'),
          API.get('/analytics/trends'),
          API.get('/analytics/summary'),
        ])
        setPerformance(perfRes.data)
        setFuel(fuelRes.data)
        setTrends(trendRes.data)
        setSummary(sumRes.data)
      } catch (err) { console.error(err) }
      finally { setLoading(false) }
    }
    fetchAll()
  }, [])

  if (loading) return <div className="text-center py-10">Loading analytics...</div>

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Analytics & Reports</h1>

      {/* Summary Row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Total Shipments</p>
          <p className="text-2xl font-bold text-blue-600">{summary?.total_shipments}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">On-Time Rate</p>
          <p className="text-2xl font-bold text-green-600">{summary?.on_time_rate}%</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Active Vehicles</p>
          <p className="text-2xl font-bold text-purple-600">{summary?.active_vehicles}</p>
        </div>
        <div className="bg-white rounded-xl shadow-sm p-4 border border-gray-100 text-center">
          <p className="text-sm text-gray-500">Total Drivers</p>
          <p className="text-2xl font-bold text-indigo-600">{summary?.total_drivers}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Delivery Performance Pie */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="text-lg font-semibold mb-4">Delivery Performance</h2>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={performance.filter((p) => p.count > 0)} dataKey="count" nameKey="status"
                cx="50%" cy="50%" outerRadius={100} label={({ status, count }) => `${status}: ${count}`}>
                {performance.map((entry) => (
                  <Cell key={entry.status} fill={STATUS_COLORS[entry.status] || '#94a3b8'} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Fuel Report Bar */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="text-lg font-semibold mb-4">Vehicle Fuel Levels</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={fuel}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="plate_number" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} domain={[0, 100]} />
              <Tooltip />
              <Bar dataKey="fuel_level" fill="#3b82f6" radius={[4, 4, 0, 0]}>
                {fuel.map((entry, idx) => (
                  <Cell key={idx} fill={entry.fuel_level > 50 ? '#10b981' : entry.fuel_level > 20 ? '#f59e0b' : '#ef4444'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Monthly Trends Line */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="text-lg font-semibold mb-4">Monthly Shipment Volume</h2>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={trends}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line type="monotone" dataKey="shipments" stroke="#8b5cf6" strokeWidth={2} dot={{ fill: '#8b5cf6' }} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Vehicle Mileage Bar */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h2 className="text-lg font-semibold mb-4">Vehicle Mileage</h2>
          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={fuel}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="plate_number" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="mileage" fill="#8b5cf6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
