import { useState } from 'react'

export default function Customers() {
  const [nit, setNit] = useState('CF')
  const [nombre, setNombre] = useState('Consumidor Final')
  const [customers, setCustomers] = useState([
    { nit: 'CF', nombre: 'Consumidor Final', correo: 'cliente@demo.gt' },
    { nit: '1234567-8', nombre: 'Tienda Demo', correo: 'facturas@demo.gt' }
  ])

  const add = () => {
    if (!nit || !nombre) return
    setCustomers([{ nit, nombre, correo: 'pendiente@demo.gt' }, ...customers])
  }

  return (
    <>
      <h1 className="page-title">Clientes</h1>
      <div className="date-label">registro y busqueda por NIT para facturacion</div>
      <div className="simple-actions">
        <input className="search-input" value={nit} onChange={(e) => setNit(e.target.value)} placeholder="NIT" />
        <input className="search-input" value={nombre} onChange={(e) => setNombre(e.target.value)} placeholder="Nombre" />
        <button className="action-button" onClick={add}>Guardar cliente</button>
      </div>
      <table className="pos-table">
        <thead><tr><th>NIT</th><th>NOMBRE</th><th>CORREO</th></tr></thead>
        <tbody>
          {customers.map((item) => <tr key={item.nit}><td>{item.nit}</td><td>{item.nombre}</td><td>{item.correo}</td></tr>)}
        </tbody>
      </table>
    </>
  )
}
