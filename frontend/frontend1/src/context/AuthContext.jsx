import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { api } from '../services/api.js'

const AuthContext = createContext(null)

function normalizeUser(usuario) {
  if (!usuario) return null

  return {
    id: usuario.id_usuario || usuario.id || 0,
    nombre: usuario.nombre_completo || usuario.nombre || 'Usuario POS',
    correo: usuario.correo,
    rol: Number(usuario.id_rol) === 1 ? 'Administrador' : 'Cajero',
    id_rol: usuario.id_rol
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const raw = localStorage.getItem('pos_user')
    if (raw) setUser(JSON.parse(raw))
  }, [])

  const login = async (correo, password) => {
    try {
      const response = await api.login(correo, password)
      const current = normalizeUser(response.usuario)

      localStorage.setItem('pos_token', response.access_token)
      localStorage.setItem('pos_user', JSON.stringify(current))
      setUser(current)

      return { ok: true }
    } catch (error) {
      return { ok: false, message: error.message || 'No se pudo iniciar sesion con el backend' }
    }
  }

  const logout = () => {
    localStorage.removeItem('pos_token')
    localStorage.removeItem('pos_user')
    setUser(null)
  }

  const value = useMemo(() => ({ user, login, logout }), [user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => useContext(AuthContext)
