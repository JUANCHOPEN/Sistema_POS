import { getProducts, getSales } from '../utils/storage.js'
import { money, totalStockValue } from '../utils/calculos.js'

export default function Reports() {
  const products = getProducts()
  const sales = getSales()
  const totalVentas = sales.reduce((acc, sale) => acc + Number(sale.total), 0)

  return (
    <>
      <h1 className="page-title">Reportes</h1>
      <div className="date-label">ventas, inventario y facturacion</div>
      <section className="card-grid">
        <div className="stat-card"><div className="stat-title">Ventas periodo</div><div className="stat-value">{money(totalVentas)}</div></div>
        <div className="stat-card"><div className="stat-title">Transacciones</div><div className="stat-value">{sales.length}</div></div>
        <div className="stat-card"><div className="stat-title">Valor inventario</div><div className="stat-value">{money(totalStockValue(products))}</div></div>
        <div className="stat-card"><div className="stat-title">Facturas FEL</div><div className="stat-value">{sales.length}</div></div>
      </section>
      <table className="pos-table">
        <thead><tr><th>FACTURA</th><th>FECHA</th><th>METODO</th><th>TOTAL</th></tr></thead>
        <tbody>
          {sales.map((item) => <tr key={item.id}><td>{item.factura}</td><td>{item.fecha}</td><td>{item.metodoPago}</td><td>{money(item.total)}</td></tr>)}
        </tbody>
      </table>
    </>
  )
}
