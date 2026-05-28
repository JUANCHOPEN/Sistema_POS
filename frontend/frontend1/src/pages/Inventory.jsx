import { useEffect, useState } from 'react'
import { api, mapApiAlert, mapApiProduct } from '../services/api.js'
import { getProducts, saveProducts } from '../utils/storage.js'
import { lowStock } from '../utils/calculos.js'

export default function Inventory() {
  const [products, setProducts] = useState(getProducts())
  const [alerts, setAlerts] = useState(lowStock(getProducts()))
  const [status, setStatus] = useState('Cargando inventario desde backend')

  const cargarInventario = async () => {
    try {
      const cats = await api.getCategorias()
      const data = await api.getProductos()
      const alertData = await api.getAlertasStock()
      const mapped = data.map((item) => mapApiProduct(item, cats))
      const mappedAlerts = alertData.map(mapApiAlert)

      setProducts(mapped)
      setAlerts(mappedAlerts)
      saveProducts(mapped)
      setStatus('Inventario conectado al backend')
    } catch (error) {
      const localProducts = getProducts()
      setProducts(localProducts)
      setAlerts(lowStock(localProducts))
      setStatus(`Modo demo local. ${error.message}`)
    }
  }

  useEffect(() => {
    cargarInventario()
  }, [])

  const entrada = (id) => {
    const updated = products.map((item) => item.id === id ? { ...item, stock: item.stock + 5 } : item)
    setProducts(updated)
    saveProducts(updated)
    setStatus('Entrada simulada. Falta endpoint de entradas de inventario en backend')
  }

  const ajuste = (id) => {
    const updated = products.map((item) => item.id === id ? { ...item, stock: Math.max(0, item.stock - 1) } : item)
    setProducts(updated)
    saveProducts(updated)
    setStatus('Ajuste simulado. Falta endpoint de ajustes de inventario en backend')
  }

  return (
    <>
      <h1 className="page-title">Inventario</h1>
      <div className="date-label">entradas, ajustes y alertas de stock</div>
      <div className="date-label">{status}</div>
      <section className="panels-row">
        <div className="panel">
          <div className="panel-title">Productos con Stock minimo</div>
          {alerts.length === 0 && <div>No hay alertas activas</div>}
          {alerts.map((item) => (
            <div className="list-row" key={item.id}>
              <span>{item.nombre}</span>
              <span className="red-text">Stock: {item.stock} (min {item.minimo})</span>
            </div>
          ))}
        </div>
        <div className="panel">
          <div className="panel-title">Ajustes rapidos</div>
          {products.slice(0, 5).map((item) => (
            <div className="list-row" key={item.id}>
              <span>{item.nombre} stock {item.stock}</span>
              <span>
                <button className="soft-button" onClick={() => entrada(item.id)}>Entrada</button>
                <button className="soft-button" onClick={() => ajuste(item.id)}>Ajuste</button>
              </span>
            </div>
          ))}
        </div>
      </section>
    </>
  )
}
