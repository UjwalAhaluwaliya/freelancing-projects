import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import API from '../api/axios'

export default function DemandForecast() {
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [days, setDays] = useState(30)

  // ETA Predictor
  const [etaForm, setEtaForm] = useState({
    distance_km: 200, traffic_factor: 1.0, weather_factor: 1.0,
    vehicle_type: 'truck', load_weight_kg: 500,
  })
  const [etaResult, setEtaResult] = useState(null)
  const [etaLoading, setEtaLoading] = useState(false)

  const fetchForecast = async () => {
    setLoading(true)
    try {
      const res = await API.get(`/ai/demand-forecast?days=${days}`)
      setForecast(res.data)
    } catch (err) { console.error(err) }
    finally { setLoading(false) }
  }

  useEffect(() => { fetchForecast() }, [days])

  const predictETA = async () => {
    setEtaLoading(true)
    try {
      const res = await API.post('/ai/predict-eta', {
        ...etaForm,
        distance_km: parseFloat(etaForm.distance_km),
        traffic_factor: parseFloat(etaForm.traffic_factor),
        weather_factor: parseFloat(etaForm.weather_factor),
        load_weight_kg: parseFloat(etaForm.load_weight_kg),
      })
      setEtaResult(res.data)
    } catch (err) { alert('ETA prediction failed') }
    finally { setEtaLoading(false) }
  }

  const chartData = forecast?.dates?.map((date, i) => ({
    date: date.slice(5),  // MM-DD
    'Linear Regression': forecast.predicted_shipments_lr[i],
    'Random Forest': forecast.predicted_shipments_rf[i],
  })) || []

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">AI Demand Forecasting & ETA Prediction</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Forecast Chart */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Shipment Demand Forecast</h2>
              <select value={days} onChange={(e) => setDays(parseInt(e.target.value))}
                className="px-3 py-1.5 border rounded-lg text-sm">
                <option value={14}>14 days</option>
                <option value={30}>30 days</option>
                <option value={60}>60 days</option>
                <option value={90}>90 days</option>
              </select>
            </div>
            {loading ? (
              <div className="text-center py-10">Loading forecast...</div>
            ) : (
              <ResponsiveContainer width="100%" height={350}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tick={{ fontSize: 11 }} interval={Math.floor(days / 10)} />
                  <YAxis tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="Linear Regression" stroke="#3b82f6" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="Random Forest" stroke="#10b981" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            )}
            <div className="mt-4 flex gap-4 text-sm text-gray-500">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                <span>Linear Regression — simple trend model</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span>Random Forest — captures complex patterns</span>
              </div>
            </div>
          </div>
        </div>

        {/* ETA Predictor */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <h2 className="text-lg font-semibold mb-4">ETA Prediction (AI)</h2>
            <div className="space-y-3">
              <div>
                <label className="text-xs text-gray-500">Distance (km)</label>
                <input type="number" value={etaForm.distance_km}
                  onChange={(e) => setEtaForm({ ...etaForm, distance_km: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" />
              </div>
              <div>
                <label className="text-xs text-gray-500">Traffic Factor (1.0 = normal)</label>
                <input type="number" step="0.1" value={etaForm.traffic_factor}
                  onChange={(e) => setEtaForm({ ...etaForm, traffic_factor: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" />
              </div>
              <div>
                <label className="text-xs text-gray-500">Weather Factor (1.0 = clear)</label>
                <input type="number" step="0.1" value={etaForm.weather_factor}
                  onChange={(e) => setEtaForm({ ...etaForm, weather_factor: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" />
              </div>
              <div>
                <label className="text-xs text-gray-500">Vehicle Type</label>
                <select value={etaForm.vehicle_type}
                  onChange={(e) => setEtaForm({ ...etaForm, vehicle_type: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm">
                  <option value="truck">Truck</option>
                  <option value="van">Van</option>
                  <option value="bike">Bike</option>
                </select>
              </div>
              <div>
                <label className="text-xs text-gray-500">Load Weight (kg)</label>
                <input type="number" value={etaForm.load_weight_kg}
                  onChange={(e) => setEtaForm({ ...etaForm, load_weight_kg: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm" />
              </div>
              <button onClick={predictETA} disabled={etaLoading}
                className="w-full py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 text-sm">
                {etaLoading ? 'Predicting...' : 'Predict ETA'}
              </button>
            </div>

            {etaResult && (
              <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm font-medium text-blue-800">Estimated Delivery Time:</p>
                <p className="text-2xl font-bold text-blue-900 mt-1">{etaResult.estimated_hours} hours</p>
                <p className="text-sm text-blue-600">({etaResult.estimated_minutes} minutes)</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
