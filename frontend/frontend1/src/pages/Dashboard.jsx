import { useEffect, useState } from 'react'
import { api, mapApiAlert, mapApiProduct } from '../services/api.js'
import { getProducts, getSales, saveProducts } from '../utils/storage.js'
import { money } from '../utils/calculos.js'

export default function Dashboard() {
  const [products, setProducts] = useState(getProducts())
  const [alerts, setAlerts] = useState([])
  const [status, setStatus] = useState('Cargando dashboard desde backend')
  const sales = getSales()
  const todaySales = sales.filter((sale) => sale.fecha === '2026-04-11')
  const total = todaySales.reduce((acc, sale) => acc + Number(sale.total), 0)
  const topProducts = [
    ['Coca Cola 12 oz', 31],
    ['Frijol negro', 28],
    ['Jabon bex', 25],
    ['Consome de pollo', 20],
    ['Pepsi 3 litros', 19]
  ]

  useEffect(() => {
    async function cargarDatos() {
      try {
        const cats = await api.getCategorias()
        const data = await api.getProductos()
        const alertData = await api.getAlertasStock()
        const mapped = data.map((item) => mapApiProduct(item, cats))

        setProducts(mapped)
        setAlerts(alertData.map(mapApiAlert))
        saveProducts(mapped)
        setStatus('Productos y alertas conectados al backend')
      } catch (error) {
        setStatus(`Dashboard parcial en demo. ${error.message}`)
      }
    }

    cargarDatos()
  }, [])

  return (
    <>
      <h1 className="page-title-white">Dashboard</h1>
      <div className="date-label">sabado 11 de abril de 2026</div>
      <div className="date-label">{status}</div>
      <section className="card-grid">
        <div className="stat-card"><div className="stat-title">Ventas del Dia</div><div className="stat-value">{money(total || 2780)}</div></div>
        <div className="stat-card"><div className="stat-title">Transacciones</div><div className="stat-value">{todaySales.length || 36}</div></div>
        <div className="stat-card"><div className="stat-title">Productos</div><div className="stat-value">{products.length}</div></div>
        <div className="stat-card"><div className="stat-title">Alertas de Stock</div><div className="stat-value stat-alert">{alerts.length}</div></div>
      </section>
      <section className="panels-row">
        <div className="panel">
          <div className="panel-title">Top 5 productos del Dia</div>
          {topProducts.map((item, index) => (
            <div className="list-row" key={item[0]}>
              <span>{index + 1}. {item[0]}</span>
              <span className="green-text">{item[1]} unidades</span>
            </div>
          ))}
        </div>
        <div className="panel">
          <div className="panel-title">Alertas de Inventario</div>
          {alerts.length === 0 && <div>No hay alertas activas</div>}
          {alerts.slice(0, 5).map((item) => (
            <div className="list-row" key={item.id}>
              <span>{item.nombre}</span>
              <span className="red-text">Stock: {item.stock} (min {item.minimo})</span>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}
