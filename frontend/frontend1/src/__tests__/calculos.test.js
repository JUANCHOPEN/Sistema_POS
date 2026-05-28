import { describe, expect, it } from 'vitest'
import { lowStock, money, subtotal, totalStockValue } from '../utils/calculos.js'

describe('calculos POS', () => {
  it('formatea dinero en quetzales', () => {
    expect(money(12.5)).toBe('Q. 12.50')
  })

  it('calcula subtotal del carrito', () => {
    const items = [{ precio: 10, cantidad: 2 }, { precio: 5, cantidad: 3 }]
    expect(subtotal(items)).toBe(35)
  })

  it('calcula valor de inventario', () => {
    const products = [{ precio: 10, stock: 2 }, { precio: 5, stock: 3 }]
    expect(totalStockValue(products)).toBe(35)
  })

  it('detecta stock minimo', () => {
    const products = [{ stock: 2, minimo: 3 }, { stock: 8, minimo: 3 }]
    expect(lowStock(products)).toHaveLength(1)
  })
})
