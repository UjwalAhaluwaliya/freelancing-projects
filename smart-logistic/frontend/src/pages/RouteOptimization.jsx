import { useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import API from '../api/axios'

const defaultStops = [
  { name: 'Warehouse (Depot)', lat: 28.6139, lng: 77.209 },
  { name: 'Mumbai', lat: 19.076, lng: 72.8777 },
  { name: 'Bangalore', lat: 12.9716, lng: 77.5946 },
  { name: 'Chennai', lat: 13.0827, lng: 80.2707 },
  { name: 'Kolkata', lat: 22.5726, lng: 88.3639 },
  { name: 'Hyderabad', lat: 17.385, lng: 78.4867 },
]

export default function RouteOptimization() {
  const [depot, setDepot] = useState(defaultStops[0])
  const [stops, setStops] = useState(defaultStops.slice(1))
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [newStop, setNewStop] = useState({ name: '', lat: '', lng: '' })

  const optimizeRoute = async () => {
    setLoading(true)
    try {
      const res = await API.post('/ai/optimize-route', {
        depot,
        stops,
        num_vehicles: 1,
      })
      setResult(res.data)
    } catch (err) {
      alert(err.response?.data?.detail || 'Optimization failed')
    } finally {
      setLoading(false)
    }
  }

  const addStop = () => {
    if (newStop.name && newStop.lat && newStop.lng) {
      setStops([...stops, { name: newStop.name, lat: parseFloat(newStop.lat), lng: parseFloat(newStop.lng) }])
      setNewStop({ name: '', lat: '', lng: '' })
    }
  }

  const removeStop = (idx) => {
    setStops(stops.filter((_, i) => i !== idx))
  }

  const routePolyline = result?.route_polyline || []

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">AI Route Optimization</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <h2 className="font-semibold mb-3">Depot (Start Point)</h2>
            <p className="text-sm text-gray-600">{depot.name}</p>
            <p className="text-xs text-gray-400">({depot.lat}, {depot.lng})</p>
          </div>

          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <h2 className="font-semibold mb-3">Delivery Stops ({stops.length})</h2>
            <div className="space-y-2 max-h-60 overflow-y-auto">
              {stops.map((s, idx) => (
                <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm font-medium">{s.name}</p>
                    <p className="text-xs text-gray-400">({s.lat}, {s.lng})</p>
                  </div>
                  <button onClick={() => removeStop(idx)} className="text-red-500 text-xs hover:text-red-700">Remove</button>
                </div>
              ))}
            </div>

            <div className="mt-3 space-y-2">
              <input placeholder="Stop name" value={newStop.name} onChange={(e) => setNewStop({ ...newStop, name: e.target.value })}
                className="w-full px-3 py-1.5 border rounded-lg text-sm" />
              <div className="grid grid-cols-2 gap-2">
                <input type="number" step="any" placeholder="Lat" value={newStop.lat}
                  onChange={(e) => setNewStop({ ...newStop, lat: e.target.value })} className="px-3 py-1.5 border rounded-lg text-sm" />
                <input type="number" step="any" placeholder="Lng" value={newStop.lng}
                  onChange={(e) => setNewStop({ ...newStop, lng: e.target.value })} className="px-3 py-1.5 border rounded-lg text-sm" />
              </div>
              <button onClick={addStop} className="w-full py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">
                + Add Stop
              </button>
            </div>
          </div>

          <button onClick={optimizeRoute} disabled={loading || stops.length === 0}
            className="w-full py-3 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 disabled:opacity-50">
            {loading ? 'Optimizing...' : 'Optimize Route'}
          </button>

          {result && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-4">
              <h3 className="font-semibold text-green-800">Optimized Route</h3>
              <p className="text-sm text-green-700 mt-1">Total Distance: <strong>{result.total_distance_km} km</strong></p>
              <div className="mt-2 space-y-1">
                {result.optimized_order.map((loc, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm">
                    <span className="w-5 h-5 bg-green-200 rounded-full flex items-center justify-center text-xs font-bold">{idx + 1}</span>
                    <span>{loc.name}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Map */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div style={{ height: '500px' }}>
              <MapContainer center={[20.5937, 78.9629]} zoom={5} style={{ height: '100%', width: '100%', borderRadius: '0.5rem' }}>
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[depot.lat, depot.lng]}>
                  <Popup><strong>Depot:</strong> {depot.name}</Popup>
                </Marker>
                {stops.map((s, idx) => (
                  <Marker key={idx} position={[s.lat, s.lng]}>
                    <Popup><strong>Stop {idx + 1}:</strong> {s.name}</Popup>
                  </Marker>
                ))}
                {routePolyline.length > 1 && (
                  <Polyline positions={routePolyline} color="green" weight={3} dashArray="10 5" />
                )}
              </MapContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
