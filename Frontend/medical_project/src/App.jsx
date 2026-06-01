import { useState } from 'react'
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from './components/accounts/ProtectedRoute';
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
<<<<<<< HEAD
import { Routes, Route } from "react-router-dom";

import PatientProfile from './components/patients/Patients'
import { DoctorProvider } from './context/doctorcontext'
=======
import PatientProfile from './components/patients/Patients'
>>>>>>> 0906caf882d3b95105c25eb13ddfa055436aa4d8

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      
      <main className="main-content">
        <div className="page">
          <Navbar />
          <Routes>
<<<<<<< HEAD
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
=======
            <Route path="/" element={<Home />} />
            <Route path="about" element={<About />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            <Route path="doctor/list" element={<PatientBookingPage />} />
            <Route path="patient/profile" element={
              <ProtectedRoute>
                <PatientProfilePage />
              </ProtectedRoute>
            } />
            <Route path="patient/appointment" element={
              <ProtectedRoute>
                <PatientAppointmentPage />
              </ProtectedRoute>
              } />
            <Route path="availability" element={
              <ProtectedRoute>
                <AvailabilityPage />
              </ProtectedRoute>
              } />
            <Route path="doctor/profile" element={
              <ProtectedRoute>
                <DoctorProfile />
              </ProtectedRoute>
              } />
            <Route path="doctors/dashboard" element={
              <ProtectedRoute>
                <DoctorDashboard />
              </ProtectedRoute>
              } />
>>>>>>> 0906caf882d3b95105c25eb13ddfa055436aa4d8
          </Routes>
        </div>
      </main>
      
    </>
  )
}

export default App
