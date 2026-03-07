import { useState, useEffect } from 'react'
import API from '../api/axios'

const statusColor = {
  available: 'bg-green-100 text-green-800',
  in_transit: 'bg-purple-100 text-purple-800',
  maintenance: 'bg-orange-100 text-orange-800',
}

export default function Vehicles() {
  const [vehicles, setVehicles] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)
  const [form, setForm] = useState({ plate_number: '', vehicle_type: 'truck', capacity: '', fuel_type: 'diesel' })

  const fetchVehicles = async () => {
    try {
      const res = await API.get('/vehicles/')
      setVehicles(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchVehicles() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await API.post('/vehicles/', { ...form, capacity: parseFloat(form.capacity) })
      setShowCreate(false)
      setForm({ plate_number: '', vehicle_type: 'truck', capacity: '', fuel_type: 'diesel' })
      fetchVehicles()
    } catch (err) { alert(err.response?.data?.detail || 'Error creating vehicle') }
  }

  const updateStatus = async (id, status) => {
    try {
      await API.put(`/vehicles/${id}`, { status })
      fetchVehicles()
    } catch (err) { alert(err.response?.data?.detail || 'Error') }
  }

  if (loading) return <div className="text-center py-10">Loading vehicles...</div>

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Vehicles</h1>
        <button onClick={() => setShowCreate(true)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium">
          + Add Vehicle
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {vehicles.map((v) => (
          <div key={v.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-lg">{v.plate_number}</h3>
              <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${statusColor[v.status]}`}>{v.status}</span>
            </div>
            <div className="space-y-2 text-sm text-gray-600">
              <p>Type: <span className="font-medium capitalize">{v.vehicle_type}</span></p>
              <p>Capacity: <span className="font-medium">{v.capacity} kg</span></p>
              <p>Fuel: <span className="font-medium capitalize">{v.fuel_type}</span></p>
              <p>Mileage: <span className="font-medium">{v.mileage.toLocaleString()} km</span></p>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span>Fuel Level</span>
                  <span>{v.fuel_level}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${v.fuel_level > 50 ? 'bg-green-500' : v.fuel_level > 20 ? 'bg-yellow-500' : 'bg-red-500'}`}
                    style={{ width: `${v.fuel_level}%` }}
                  />
                </div>
              </div>
            </div>
            <div className="flex gap-2 mt-4">
              {v.status !== 'available' && (
                <button onClick={() => updateStatus(v.id, 'available')}
                  className="px-3 py-1.5 bg-green-50 text-green-700 rounded-lg text-xs hover:bg-green-100">
                  Set Available
                </button>
              )}
              {v.status !== 'maintenance' && (
                <button onClick={() => updateStatus(v.id, 'maintenance')}
                  className="px-3 py-1.5 bg-orange-50 text-orange-700 rounded-lg text-xs hover:bg-orange-100">
                  Maintenance
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Create Modal */}
      {showCreate && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md">
            <h2 className="text-lg font-semibold mb-4">Add New Vehicle</h2>
            <form onSubmit={handleCreate} className="space-y-3">
              <div>
                <label className="text-xs text-gray-500">Plate Number</label>
                <input value={form.plate_number} onChange={(e) => setForm({ ...form, plate_number: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" required />
              </div>
              <div>
                <label className="text-xs text-gray-500">Type</label>
                <select value={form.vehicle_type} onChange={(e) => setForm({ ...form, vehicle_type: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm">
                  <option value="truck">Truck</option>
                  <option value="van">Van</option>
                  <option value="bike">Bike</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500">Capacity (kg)</label>
                <input type="number" value={form.capacity} onChange={(e) => setForm({ ...form, capacity: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" required />
              </div>
              <div>
                <label className="text-xs text-gray-500">Fuel Type</label>
                <select value={form.fuel_type} onChange={(e) => setForm({ ...form, fuel_type: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm">
                  <option value="diesel">Diesel</option>
                  <option value="petrol">Petrol</option>
                  <option value="electric">Electric</option>
                </select>
              </div>
              <div className="flex gap-2 pt-2">
                <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Add</button>
                <button type="button" onClick={() => setShowCreate(false)}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
