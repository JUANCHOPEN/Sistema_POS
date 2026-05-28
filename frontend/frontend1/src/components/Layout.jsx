import { NavLink, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

const menu = [
  { label: 'Dashboard', path: '/dashboard' },
  { label: 'Punto de venta', path: '/pos' },
  { label: 'Inventario', path: '/inventario' },
  { label: 'Producto', path: '/productos' },
  { label: 'Clientes', path: '/clientes' }
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const closeSession = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="app-shell">
      <div className="pos-window">
        <header className="pos-header">
          <div className="pos-title">SISTEMA POS</div>
          <div className="admin-label">admin: {user?.nombre || 'Juan Chopen'}</div>
        </header>
        <div className="pos-body">
          <aside className="sidebar">
            <div className="sidebar-title">MENU</div>
            {menu.map((item) => (
              <NavLink to={item.path} key={item.path} className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                <span className="nav-marker" />
                <span>{item.label}</span>
              </NavLink>
            ))}
            <div className="sidebar-section">Admin</div>
            <NavLink to="/usuarios" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <span />
              <span>Usuarios</span>
            </NavLink>
            <NavLink to="/reportes" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
              <span />
              <span>Reportes</span>
            </NavLink>
            <button className="nav-item nav-link-blue" onClick={closeSession}>
              <span />
              <span>Cerrar Sesion</span>
            </button>
          </aside>
          <main className="content">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  )
}
