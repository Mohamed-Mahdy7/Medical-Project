import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/variables.css'
import './styles/theme-light.css'
import './styles/theme-dark.css'
import './styles/base.css'
// import './styles/utilities.css'
import './styles/index.css'
import App from './App.jsx'
import { AuthProvider } from "./context/AuthContext.jsx";

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </StrictMode>,
)
