import { useState } from 'react'
import './styles/App.css'
import Login from "./pages/Login"
import Register from './pages/Register'
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
