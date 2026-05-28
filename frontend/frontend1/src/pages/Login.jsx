import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [correo, setCorreo] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const submit = async (event) => {
    event.preventDefault()
    setError('')

    const result = await login(correo, password)
    if (!result.ok) {
      setError(result.message)
      return
    }

    navigate('/dashboard')
  }

  return (
    <div className="login-wrap">
      <div className="login-window">
        <form className="login-card" onSubmit={submit}>
          <h1 className="login-title">ACCESO AL SISTEMA</h1>
          <label className="login-row">
            <span>Correo Electronico</span>
            <input className="login-input" value={correo} onChange={(e) => setCorreo(e.target.value)} />
          </label>
          <label className="login-row">
            <span>Contraseña</span>
            <input className="login-input" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
          </label>
          <div className="login-help">olvidaste tu contraseña?</div>
          {error && <div className="error-box">{error}</div>}
          <button className="login-button" type="submit">Iniciar Sesión</button>
          <div className="login-note">Bloqueo tras 5 intentos fallidos</div>
        </form>
      </div>
    </div>
  )
}
