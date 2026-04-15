import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Dashboard from './components/Dashboard'
import CrearPaciente from './components/CrearPaciente'
import AgendarCita from './components/AgendarCita'

function App() {
  return (
    <div className="App bg-light min-vh-100">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/nuevo-paciente" element={<CrearPaciente />} />
        <Route path="/agendar-cita" element={<AgendarCita />} />
      </Routes>
    </div>
  )
}

export default App
