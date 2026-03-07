import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import ProtectedRoute from './components/ProtectedRoute'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Shipments from './pages/Shipments'
import Vehicles from './pages/Vehicles'
import Tracking from './pages/Tracking'
import RouteOptimization from './pages/RouteOptimization'
import DemandForecast from './pages/DemandForecast'
import Analytics from './pages/Analytics'
import Notifications from './pages/Notifications'
import Users from './pages/Users'
import ChatBot from './pages/ChatBot'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Dashboard />} />
        <Route path="shipments" element={<Shipments />} />
        <Route path="vehicles" element={
          <ProtectedRoute roles={['admin', 'manager']}>
            <Vehicles />
          </ProtectedRoute>
        } />
        <Route path="tracking" element={<Tracking />} />
        <Route path="route-optimization" element={
          <ProtectedRoute roles={['admin', 'manager']}>
            <RouteOptimization />
          </ProtectedRoute>
        } />
        <Route path="demand-forecast" element={
          <ProtectedRoute roles={['admin', 'manager']}>
            <DemandForecast />
          </ProtectedRoute>
        } />
        <Route path="analytics" element={
          <ProtectedRoute roles={['admin', 'manager']}>
            <Analytics />
          </ProtectedRoute>
        } />
        <Route path="notifications" element={<Notifications />} />
        <Route path="users" element={
          <ProtectedRoute roles={['admin']}>
            <Users />
          </ProtectedRoute>
        } />
        <Route path="chat" element={
          <ProtectedRoute>
            <ChatBot />
          </ProtectedRoute>
        } />
      </Route>
    </Routes>
  )
}
