import { useEffect, useMemo, useState } from 'react'
import { api, mapApiProduct } from '../services/api.js'
import { getProducts, saveProducts } from '../utils/storage.js'
import { money } from '../utils/calculos.js'

export default function Products() {
  const [products, setProducts] = useState(getProducts())
  const [categorias, setCategorias] = useState([])
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('Cargando productos desde backend')

  const cargarProductos = async () => {
    try {
      const cats = await api.getCategorias()
      const data = await api.getProductos()
      const mapped = data.map((item) => mapApiProduct(item, cats))

      setCategorias(cats)
      setProducts(mapped)
      saveProducts(mapped)
      setStatus('Conectado al backend')
    } catch (error) {
      setStatus(`Modo demo local. ${error.message}`)
    }
  }

  useEffect(() => {
    cargarProductos()
  }, [])

  const filtered = useMemo(() => {
    const term = query.toLowerCase()
    return products.filter((item) => item.nombre.toLowerCase().includes(term) || String(item.codigo).includes(term))
  }, [products, query])

  const addProduct = async () => {
    const categoriaBase = categorias[0]

    if (!categoriaBase) {
      setStatus('Primero debe existir una categoria en SQL Server')
      return
    }

    const codigo = String(Date.now()).slice(-6)

    try {
      await api.crearProducto({
        id_categoria: categoriaBase.id_categoria,
        codigo,
        nombre: `NUEVO PRODUCTO ${codigo}`,
        precio_venta: 1,
        precio_costo: 1,
        stock_actual: 10,
        stock_minimo: 3
      })

      await cargarProductos()
      setStatus('Producto creado en el backend')
    } catch (error) {
      setStatus(error.message)
    }
  }

  return (
    <>
      <div className="inventory-head">
        <div>
          <h1 className="page-title">Productos e Inventarios</h1>
          <div className="date-label">sabado 11 de abril de 2026</div>
          <div className="inventory-count">{products.length} productos registrados</div>
          <div className="date-label">{status}</div>
        </div>
        <button className="add-product" onClick={addProduct}>AGREGAR PRODUCTO</button>
      </div>
      <input className="search-input" style={{ marginTop: 12, width: 350 }} value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Buscar producto por nombre o codigo" />
      <table className="pos-table">
        <thead>
          <tr>
            <th>CODIGO</th>
            <th>DESCRIPCION</th>
            <th>CATEGORIA</th>
            <th>PRECIO VENTA</th>
            <th>STOCK</th>
            <th>MINIMO</th>
          </tr>
        </thead>
        <tbody>
          {filtered.slice(0, 12).map((item) => (
            <tr key={item.id}>
              <td>{item.codigo}</td>
              <td>{item.nombre}</td>
              <td>{item.categoria}</td>
              <td>{money(item.precio)}</td>
              <td>{item.stock}</td>
              <td>{item.minimo}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  )
}
