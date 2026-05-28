import { initialProducts, initialSales } from '../services/mockData.js'

const read = (key, fallback) => {
  const raw = localStorage.getItem(key)
  return raw ? JSON.parse(raw) : fallback
}

const write = (key, value) => {
  localStorage.setItem(key, JSON.stringify(value))
}

export const getProducts = () => read('pos_products', initialProducts)
export const saveProducts = (products) => write('pos_products', products)
export const getSales = () => read('pos_sales', initialSales)
export const saveSales = (sales) => write('pos_sales', sales)

export const resetDemo = () => {
  saveProducts(initialProducts)
  saveSales(initialSales)
}
