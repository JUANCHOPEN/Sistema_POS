export const money = (value) => `Q. ${Number(value || 0).toFixed(2)}`

export const subtotal = (items) => {
  return items.reduce((total, item) => total + Number(item.precio) * Number(item.cantidad), 0)
}

export const totalStockValue = (products) => {
  return products.reduce((total, item) => total + Number(item.precio) * Number(item.stock), 0)
}

export const lowStock = (products) => {
  return products.filter((item) => Number(item.stock) <= Number(item.minimo))
}
