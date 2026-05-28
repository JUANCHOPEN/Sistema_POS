const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

function getToken() {
  return localStorage.getItem('pos_token')
}

async function request(path, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }

  const token = getToken()
  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined
  })

  const text = await response.text()
  let data = null

  try {
    data = text ? JSON.parse(text) : null
  } catch {
    data = text
  }

  if (!response.ok) {
    const message = data?.detail || data?.message || 'Error al consumir el backend'
    throw new Error(message)
  }

  return data
}

export function mapApiProduct(product, categorias = []) {
  const categoria = categorias.find((item) => Number(item.id_categoria) === Number(product.id_categoria))

  return {
    id: product.id_producto,
    id_producto: product.id_producto,
    id_categoria: product.id_categoria,
    codigo: product.codigo,
    nombre: product.nombre,
    categoria: categoria?.nombre || `Categoria ${product.id_categoria}`,
    precio: Number(product.precio_venta || 0),
    costo: Number(product.precio_costo || 0),
    stock: Number(product.stock_actual || 0),
    minimo: Number(product.stock_minimo || 0),
    activo: Boolean(product.activo)
  }
}

export function mapApiAlert(alert) {
  return {
    id: alert.id_producto,
    id_producto: alert.id_producto,
    codigo: alert.codigo,
    nombre: alert.nombre,
    stock: Number(alert.stock_actual || 0),
    minimo: Number(alert.stock_minimo || 0)
  }
}

export const api = {
  login(correo, contrasena) {
    return request('/auth/login', {
      method: 'POST',
      body: { correo, contrasena }
    })
  },

  crearUsuario(datos) {
    return request('/auth/usuarios', {
      method: 'POST',
      body: datos
    })
  },

  getCategorias() {
    return request('/productos/categorias')
  },

  crearCategoria(datos) {
    return request('/productos/categorias', {
      method: 'POST',
      body: datos
    })
  },

  getProductos() {
    return request('/productos/')
  },

  buscarProductos(termino) {
    return request(`/productos/buscar?termino=${encodeURIComponent(termino)}`)
  },

  getAlertasStock() {
    return request('/productos/alertas-stock')
  },

  crearProducto(datos) {
    return request('/productos/', {
      method: 'POST',
      body: datos
    })
  },

  actualizarProducto(idProducto, datos) {
    return request(`/productos/${idProducto}`, {
      method: 'PUT',
      body: datos
    })
  }
}
