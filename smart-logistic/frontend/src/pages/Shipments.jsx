import { useState, useEffect } from 'react'
import API from '../api/axios'
import { useAuth } from '../context/AuthContext'

const statusColor = {
  pending: 'bg-yellow-100 text-yellow-800',
  assigned: 'bg-blue-100 text-blue-800',
  in_transit: 'bg-purple-100 text-purple-800',
  delivered: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
}

const priorityColor = {
  low: 'bg-gray-100 text-gray-700',
  normal: 'bg-blue-50 text-blue-700',
  high: 'bg-orange-100 text-orange-700',
  urgent: 'bg-red-100 text-red-700',
}

export default function Shipments() {
  const { user } = useAuth()
  const [shipments, setShipments] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [showAssign, setShowAssign] = useState(null)
  const [drivers, setDrivers] = useState([])
  const [vehicles, setVehicles] = useState([])
  const [form, setForm] = useState({
    origin: '', destination: '', weight: '', priority: 'normal',
    origin_lat: '', origin_lng: '', dest_lat: '', dest_lng: '',
  })
  const [assignForm, setAssignForm] = useState({ driver_id: '', vehicle_id: '' })

  const fetchShipments = async () => {
    try {
      const res = await API.get('/shipments/')
      setShipments(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchShipments() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await API.post('/shipments/', {
        ...form,
        weight: parseFloat(form.weight),
        origin_lat: form.origin_lat ? parseFloat(form.origin_lat) : null,
        origin_lng: form.origin_lng ? parseFloat(form.origin_lng) : null,
        dest_lat: form.dest_lat ? parseFloat(form.dest_lat) : null,
        dest_lng: form.dest_lng ? parseFloat(form.dest_lng) : null,
      })
      setShowCreate(false)
      setForm({ origin: '', destination: '', weight: '', priority: 'normal', origin_lat: '', origin_lng: '', dest_lat: '', dest_lng: '' })
      fetchShipments()
    } catch (err) { alert(err.response?.data?.detail || 'Error creating shipment') }
  }

  const openAssign = async (shipment) => {
    setShowAssign(shipment)
    try {
      const [dRes, vRes] = await Promise.all([
        API.get('/users/drivers'),
        API.get('/vehicles/?status=available'),
      ])
      setDrivers(dRes.data)
      setVehicles(vRes.data)
    } catch (err) { console.error(err) }
  }

  const handleAssign = async (e) => {
    e.preventDefault()
    try {
      await API.post(`/shipments/${showAssign.id}/assign`, {
        driver_id: parseInt(assignForm.driver_id),
        vehicle_id: parseInt(assignForm.vehicle_id),
      })
      setShowAssign(null)
      setAssignForm({ driver_id: '', vehicle_id: '' })
      fetchShipments()
    } catch (err) { alert(err.response?.data?.detail || 'Error assigning shipment') }
  }

  const updateStatus = async (id, status) => {
    try {
      await API.put(`/shipments/${id}`, { status })
      fetchShipments()
    } catch (err) { alert(err.response?.data?.detail || 'Error updating status') }
  }

  if (loading) return <div className="text-center py-10">Loading shipments...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Shipments</h1>
        {['admin', 'manager', 'customer'].includes(user?.role) && (
          <button onClick={() => setShowCreate(true)}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
            + New Shipment
          </button>
        )}
      </div>

      {/* Shipments Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-gray-50">
            <tr className="text-left text-gray-600">
              <th className="px-4 py-3">Tracking #</th>
              <th className="px-4 py-3">Origin</th>
              <th className="px-4 py-3">Destination</th>
              <th className="px-4 py-3">Weight (kg)</th>
              <th className="px-4 py-3">Priority</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">Actions</th>
            </tr>
          </thead>
          <tbody>
            {shipments.map((s) => (
              <tr key={s.id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-3 font-mono text-xs">{s.tracking_number}</td>
                <td className="px-4 py-3">{s.origin}</td>
                <td className="px-4 py-3">{s.destination}</td>
                <td className="px-4 py-3">{s.weight}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${priorityColor[s.priority]}`}>{s.priority}</span>
                </td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor[s.status]}`}>{s.status}</span>
                </td>
                <td className="px-4 py-3 space-x-1">
                  {s.status === 'pending' && ['admin', 'manager'].includes(user?.role) && (
                    <button onClick={() => openAssign(s)}
                      className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs hover:bg-blue-100">Assign</button>
                  )}
                  {s.status === 'in_transit' && (
                    <button onClick={() => updateStatus(s.id, 'delivered')}
                      className="px-2 py-1 bg-green-50 text-green-700 rounded text-xs hover:bg-green-100">Deliver</button>
                  )}
                  {s.status === 'pending' && (
                    <button onClick={() => updateStatus(s.id, 'cancelled')}
                      className="px-2 py-1 bg-red-50 text-red-700 rounded text-xs hover:bg-red-100">Cancel</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create Modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-lg">
            <h2 className="text-lg font-semibold mb-4">Create New Shipment</h2>
            <form onSubmit={handleCreate} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs text-gray-500">Origin</label>
                  <input value={form.origin} onChange={(e) => setForm({ ...form, origin: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" required />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Destination</label>
                  <input value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" required />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Origin Lat</label>
                  <input type="number" step="any" value={form.origin_lat} onChange={(e) => setForm({ ...form, origin_lat: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Origin Lng</label>
                  <input type="number" step="any" value={form.origin_lng} onChange={(e) => setForm({ ...form, origin_lng: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Dest Lat</label>
                  <input type="number" step="any" value={form.dest_lat} onChange={(e) => setForm({ ...form, dest_lat: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Dest Lng</label>
                  <input type="number" step="any" value={form.dest_lng} onChange={(e) => setForm({ ...form, dest_lng: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Weight (kg)</label>
                  <input type="number" value={form.weight} onChange={(e) => setForm({ ...form, weight: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm" required />
                </div>
                <div>
                  <label className="text-xs text-gray-500">Priority</label>
                  <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm">
                    <option value="low">Low</option>
                    <option value="normal">Normal</option>
                    <option value="high">High</option>
                    <option value="urgent">Urgent</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-2 pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Create</button>
                <button type="button" onClick={() => setShowCreate(false)}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Assign Modal */}
      {showAssign && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">Assign Shipment: {showAssign.tracking_number}</h2>
            <form onSubmit={handleAssign} className="space-y-3">
              <div>
                <label className="text-xs text-gray-500">Driver</label>
                <select value={assignForm.driver_id} onChange={(e) => setAssignForm({ ...assignForm, driver_id: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" required>
                  <option value="">Select driver</option>
                  {drivers.map((d) => <option key={d.id} value={d.id}>{d.full_name}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500">Vehicle</label>
                <select value={assignForm.vehicle_id} onChange={(e) => setAssignForm({ ...assignForm, vehicle_id: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" required>
                  <option value="">Select vehicle</option>
                  {vehicles.map((v) => <option key={v.id} value={v.id}>{v.plate_number} ({v.vehicle_type})</option>)}
                </select>
              </div>
              <div className="flex gap-2 pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Assign</button>
                <button type="button" onClick={() => setShowAssign(null)}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
