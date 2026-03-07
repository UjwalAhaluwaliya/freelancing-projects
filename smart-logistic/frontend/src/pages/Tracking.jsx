import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet'
import API from '../api/axios'

export default function Tracking() {
  const [shipments, setShipments] = useState([])
  const [selected, setSelected] = useState(null)
  const [trackingData, setTrackingData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    API.get('/shipments/').then((res) => {
      setShipments(res.data)
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const loadTracking = async (shipment) => {
    setSelected(shipment)
    try {
      const res = await API.get(`/tracking/${shipment.id}`)
      setTrackingData(res.data)
    } catch (err) { console.error(err) }
  }

  const simulateTracking = async () => {
    if (!selected) return
    try {
      await API.post(`/tracking/simulate/${selected.id}`)
      loadTracking(selected)
    } catch (err) { alert(err.response?.data?.detail || 'Cannot simulate') }
  }

  if (loading) return <div className="text-center py-10">Loading...</div>

  const mapCenter = trackingData.length > 0
    ? [trackingData[Math.floor(trackingData.length / 2)].latitude, trackingData[Math.floor(trackingData.length / 2)].longitude]
    : [20.5937, 78.9629]

  const polylinePositions = trackingData.map((t) => [t.latitude, t.longitude])

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Real-Time Tracking</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Shipment List */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 max-h-[600px] overflow-y-auto">
          <h2 className="font-semibold mb-3">Select Shipment</h2>
          {shipments.filter((s) => ['assigned', 'in_transit', 'delivered'].includes(s.status)).map((s) => (
            <div
              key={s.id}
              onClick={() => loadTracking(s)}
              className={`p-3 rounded-lg mb-2 cursor-pointer border transition-colors ${
                selected?.id === s.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
              }`}
            >
              <p className="font-mono text-xs text-gray-500">{s.tracking_number}</p>
              <p className="text-sm font-medium">{s.origin} → {s.destination}</p>
              <span className={`inline-block mt-1 px-2 py-0.5 rounded-full text-xs ${
                s.status === 'delivered' ? 'bg-green-100 text-green-800' :
                s.status === 'in_transit' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'
              }`}>{s.status}</span>
            </div>
          ))}
        </div>

        {/* Map */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="font-semibold">
                {selected ? `Tracking: ${selected.tracking_number}` : 'Select a shipment'}
              </h2>
              {selected && selected.origin_lat && (
                <button onClick={simulateTracking}
                  className="px-3 py-1.5 bg-purple-600 text-white rounded-lg text-xs hover:bg-purple-700">
                  Simulate GPS
                </button>
              )}
            </div>
            <div style={{ height: '400px' }}>
              <MapContainer center={mapCenter} zoom={5} style={{ height: '100%', width: '100%', borderRadius: '0.5rem' }}>
                <TileLayer
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {trackingData.map((point, idx) => (
                  <Marker key={idx} position={[point.latitude, point.longitude]}>
                    <Popup>
                      <strong>{point.status}</strong><br />
                      {point.notes}<br />
                      <small>{new Date(point.timestamp).toLocaleString()}</small>
                    </Popup>
                  </Marker>
                ))}
                {polylinePositions.length > 1 && (
                  <Polyline positions={polylinePositions} color="blue" weight={3} />
                )}
              </MapContainer>
            </div>
          </div>

          {/* Timeline */}
          {trackingData.length > 0 && (
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mt-4">
              <h2 className="font-semibold mb-3">Tracking Timeline</h2>
              <div className="space-y-3">
                {trackingData.map((t, idx) => (
                  <div key={idx} className="flex items-start gap-3">
                    <div className={`w-3 h-3 rounded-full mt-1 ${
                      t.status === 'delivered' ? 'bg-green-500' :
                      t.status === 'picked_up' ? 'bg-blue-500' : 'bg-purple-500'
                    }`} />
                    <div>
                      <p className="text-sm font-medium capitalize">{t.status}</p>
                      <p className="text-xs text-gray-500">{t.notes}</p>
                      <p className="text-xs text-gray-400">{new Date(t.timestamp).toLocaleString()}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
