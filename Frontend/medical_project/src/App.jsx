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
import AvailabilityPage from './pages/Availability/AvailabilityPage'
import DoctorDashboard from './pages/Doctor/Doctordashboard'
import DoctorProfile from './pages/Doctor/Doctorprofile'
import DoctorAppointments from './pages/Doctor/DoctorAppointments';
import DoctorsList from './pages/Doctor/Doctorlist'
import DoctorsSpecialities from "./pages/Doctor/DoctorSpeciality";
import PatientProfile from './components/patients/Patients'

function App() {
  return (
    <>
      
      <main className="main-content">
        <div className="page">
          <Navbar />
          <Routes>
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
            <Route path="/doctors/me/" element={
              <ProtectedRoute>
                <DoctorProfile />
              </ProtectedRoute>
              } />
            <Route path="doctors/dashboard" element={
              <ProtectedRoute>
                <DoctorDashboard />
              </ProtectedRoute>
              } />
            <Route path="doctor/appointments" element={
              <ProtectedRoute>
                <DoctorAppointments />
              </ProtectedRoute>
              } />
            <Route path="doctors/specialties/" element={
              <ProtectedRoute>
                <DoctorsSpecialities />
              </ProtectedRoute>
              } />
          </Routes>
        </div>
      </main>
      
    </>
  )
}

export default App
