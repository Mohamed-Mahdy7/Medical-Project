import { useState } from 'react'
import './styles/App.css'
import Login from "./pages/Login"
import Register from './pages/Register'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <main className="main-content">
        <div className="page">
          {/* <Login /> */}
          <Register />
        </div>
      </main>
    </>
  )
}

export default App
