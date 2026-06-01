import { useState } from 'react'
import './styles/App.css'
import Home from './pages/Home'
import About from './pages/About'
import Navbar from './components/Navbar'
import Login from "./pages/Login"
import Register from './pages/Register'
import PatientProfilePage from './pages/PatientProfile'
import PatientAppointmentPage from './components/patients/PatientAppointments'
import PatientBookingPage from './pages/PatientBooking'
import AvailabilityPage from './components/availability/AvailabilityPage'
import DoctorDashboard from './pages/Doctor/Doctordashboard'
import DoctorProfile from './pages/Doctor/Doctorprofile'
import DoctorsList from './pages/Doctor/Doctorlist'
import { Routes, Route } from "react-router-dom";

import PatientProfile from './components/patients/Patients'
import { DoctorProvider } from './context/doctorcontext'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      
      <main className="main-content">
        <div className="page">
          <Navbar />
          <Routes>
            <Route path="/" element ={<Home />} />
            <Route path="about" element ={<About />} />
            <Route path="login" element ={<Login />} />
            <Route path="register" element ={<Register />} />
            <Route path="patient/profile" element ={<PatientProfilePage />} />
            <Route path="patient/appointment" element ={<PatientAppointmentPage />} />
            <Route path="doctor/list" element ={<PatientBookingPage />} />
            <Route path="availability" element ={<AvailabilityPage />} />
            <Route path="doctors/dashboard" element ={<DoctorDashboard />} />
            <Route path="doctor/profile/me" element ={<DoctorProfile />} />
          </Routes>
        </div>
      </main>
      
    </>
  )
}

export default App
