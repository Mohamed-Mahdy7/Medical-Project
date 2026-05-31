import { useState } from 'react'
import './styles/App.css'
import Login from "./pages/Login"
import Register from './pages/Register'
import PatientProfilePage from './pages/PatientProfile'
import PatientAppointmentPage from './components/patients/PatientAppointments'
import PatientBookingPage from './pages/PatientBooking'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <main className="main-content">
        <div className="page">
          {/* <Login /> */}
          {/* <Register /> */}
          <PatientProfilePage />
          <PatientAppointmentPage />
          <PatientBookingPage />
        </div>
      </main>
    </>
  )
}

export default App
