import { demoUsers } from '../services/mockData.js'

export default function Users() {
  return (
    <>
      <h1 className="page-title">Usuarios</h1>
      <div className="date-label">control de acceso por rol</div>
      <table className="pos-table">
        <thead><tr><th>NOMBRE</th><th>CORREO</th><th>ROL</th><th>ESTADO</th></tr></thead>
        <tbody>
          {demoUsers.map((item) => (
            <tr key={item.id}><td>{item.nombre}</td><td>{item.correo}</td><td>{item.rol}</td><td>Activo</td></tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
