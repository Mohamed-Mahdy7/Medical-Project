import { useState } from 'react'
import './styles/App.css'
import Login from "./pages/Login"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <main className="main-content">
        <div className="page">
          <Login />
        </div>
      </main>
    </>
  )
}

export default App
