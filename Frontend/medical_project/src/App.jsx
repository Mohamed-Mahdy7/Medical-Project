import { useState } from 'react'
import './styles/App.css'
import Login from "./pages/Login"
import Register from './pages/Register'
import DoctorDashboard from './pages/Doctor/Doctordashboard'
import DoctorProfile from './pages/Doctor/Doctorprofile'
import DoctorsList from './pages/Doctor/Doctorlist'
import { Routes, Route } from "react-router-dom";

import PatientProfile from './components/patients/Patients'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <main className="main-content">
        <div className="page">
          {/* <Login /> */}
          {/* <Register /> */}
          <PatientProfile />
        </div>
      </main>
    </>
  )
}

export default App
