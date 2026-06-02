import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/variables.css'
import './styles/theme-light.css'
import './styles/theme-dark.css'
import './styles/base.css'
import App from './App.jsx'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from "./context/AuthContext.jsx";
import { DoctorProvider } from './context/DoctorContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <DoctorProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </DoctorProvider>
    </AuthProvider>
  </StrictMode>,
)
