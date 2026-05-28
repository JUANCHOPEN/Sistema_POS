import { useEffect, useMemo, useState } from 'react'
import { api, mapApiProduct } from '../services/api.js'
import { getProducts, getSales, saveProducts, saveSales } from '../utils/storage.js'
import { money, subtotal } from '../utils/calculos.js'

export default function POS() {
  const [products, setProducts] = useState(getProducts())
  const [sales, setSales] = useState(getSales())
  const [query, setQuery] = useState('')
  const [selected, setSelected] = useState(products[0])
  const [cantidad, setCantidad] = useState(1)
  const [cart, setCart] = useState([])
  const [metodo, setMetodo] = useState('Efectivo')
  const [nit, setNit] = useState('CF')
  const [message, setMessage] = useState('')
  const [status, setStatus] = useState('Cargando productos desde backend')

  useEffect(() => {
    async function cargarProductos() {
      try {
        const cats = await api.getCategorias()
        const data = await api.getProductos()
        const mapped = data.map((item) => mapApiProduct(item, cats))

        setProducts(mapped)
        setSelected(mapped[0])
        saveProducts(mapped)
        setStatus('Busqueda de productos conectada al backend')
      } catch (error) {
        const localProducts = getProducts()
        setProducts(localProducts)
        setSelected(localProducts[0])
        setStatus(`Modo demo local. ${error.message}`)
      }
    }

    cargarProductos()
  }, [])

  useEffect(() => {
    async function buscarEnBackend() {
      if (!query.trim()) return

      try {
        const cats = await api.getCategorias()
        const data = await api.buscarProductos(query)
        const mapped = data.map((item) => mapApiProduct(item, cats))
        setProducts(mapped)
        setStatus('Busqueda ejecutada contra backend')
      } catch {
        setStatus('Busqueda local. El backend no respondio')
      }
    }

    const timer = setTimeout(buscarEnBackend, 400)
    return () => clearTimeout(timer)
  }, [query])

  const filtered = useMemo(() => {
    const term = query.toLowerCase()
    return products.filter((item) => item.nombre.toLowerCase().includes(term) || String(item.codigo).includes(term))
  }, [products, query])

  const addToCart = () => {
    const qty = Number(cantidad)
    if (!selected || qty < 1 || qty > selected.stock) return

    setCart((current) => {
      const existing = current.find((item) => item.id === selected.id)
      if (existing) {
        return current.map((item) => item.id === selected.id ? { ...item, cantidad: item.cantidad + qty } : item)
      }
      return [...current, { ...selected, cantidad: qty }]
    })

    setMessage('Producto agregado al pedido')
  }

  const charge = () => {
    if (cart.length === 0) return

    const total = subtotal(cart)
    const sale = {
      id: Date.now(),
      fecha: '2026-04-11',
      total,
      metodoPago: metodo,
      factura: `FEL-${Date.now()}`,
      nit,
      productos: cart.length
    }

    const updatedProducts = getProducts().map((product) => {
      const item = cart.find((line) => line.id === product.id)
      return item ? { ...product, stock: product.stock - item.cantidad } : product
    })

    const updatedSales = [sale, ...sales]
    setProducts(updatedProducts)
    setSales(updatedSales)
    saveProducts(updatedProducts)
    saveSales(updatedSales)
    setCart([])
    setMessage('Venta simulada. Falta endpoint POST /ventas en el backend')
  }

  return (
    <>
      <h1 className="page-title">Punto de Venta</h1>
      <div className="date-label">sabado 11 de abril 2026</div>
      <div className="date-label">{status}</div>
      <section className="pos-sale-grid">
        <div className="product-list">
          <div>buscar Producto</div>
          <input className="search-input" value={query} onChange={(e) => setQuery(e.target.value)} />
          <div className="green-text">seleccionar producto</div>
          {filtered.slice(0, 11).map((item) => (
            <button key={item.id} onClick={() => setSelected(item)}>{item.nombre.toLowerCase()}</button>
          ))}
        </div>
        <div>
          <div className="selected-product">
            <div className="selected-title">Producto seleccionado</div>
            <div className="form-grid">
              <input className="small-input" value={selected?.nombre || ''} readOnly />
              <span />
              <span className="field-label">Cantidad</span>
              <span className="field-label">Subtotal <input className="small-input" value={money((selected?.precio || 0) * cantidad)} readOnly /></span>
              <input className="small-input" type="number" min="1" max={selected?.stock || 1} value={cantidad} onChange={(e) => setCantidad(e.target.value)} />
              <button className="action-button" onClick={addToCart}>agregar al pedido</button>
              <span className="field-label">precio {money(selected?.precio || 0)}</span>
              <span className="field-label">Stock Disponible <span className="red-text">{selected?.stock || 0}</span></span>
            </div>
          </div>
          <div className="total-panel">
            <span>TOTAL PEDIDO</span>
            <span className="total-box">{money(subtotal(cart) || 0)}</span>
          </div>
          <div className="simple-actions">
            <select className="search-input" value={metodo} onChange={(e) => setMetodo(e.target.value)}>
              <option>Efectivo</option>
              <option>Tarjeta</option>
              <option>Transferencia</option>
            </select>
            <input className="search-input" value={nit} onChange={(e) => setNit(e.target.value)} placeholder="NIT o CF" />
          </div>
          <button className="pay-button" onClick={charge}>Cobrar</button>
          {message && <div className="green-text" style={{ marginTop: 12 }}>{message}</div>}
        </div>
      </section>
    </>
  )
}
