export const demoUsers = [
  { id: 1, nombre: 'Juan Chopen', correo: 'admin@pos.gt', password: 'admin123', rol: 'Administrador' },
  { id: 2, nombre: 'Cajero Demo', correo: 'cajero@pos.gt', password: 'cajero123', rol: 'Cajero' }
]

export const initialProducts = [
  { id: 1, codigo: '0001', nombre: 'ARROZ', categoria: 'COMESTIBLE', precio: 6.00, costo: 4.00, stock: 27, minimo: 5 },
  { id: 2, codigo: '0002', nombre: 'FRIJOL', categoria: 'COMESTIBLE', precio: 8.00, costo: 5.00, stock: 32, minimo: 3 },
  { id: 3, codigo: '0003', nombre: 'AZUCAR', categoria: 'COMESTIBLE', precio: 5.00, costo: 3.00, stock: 42, minimo: 5 },
  { id: 4, codigo: '0004', nombre: 'CAFE', categoria: 'COMESTIBLE', precio: 2.50, costo: 1.20, stock: 85, minimo: 8 },
  { id: 5, codigo: '0005', nombre: 'CLORO', categoria: 'JABON', precio: 2.00, costo: 1.00, stock: 75, minimo: 10 },
  { id: 6, codigo: '0006', nombre: 'COCA COLA', categoria: 'BEBIDAS', precio: 20.00, costo: 15.00, stock: 15, minimo: 12 },
  { id: 7, codigo: '0007', nombre: 'Aceite 1 litro', categoria: 'COMESTIBLE', precio: 18.00, costo: 12.00, stock: 48, minimo: 3 },
  { id: 8, codigo: '0008', nombre: 'Salchicha', categoria: 'COMESTIBLE', precio: 12.00, costo: 8.00, stock: 20, minimo: 5 },
  { id: 9, codigo: '0009', nombre: 'Fideo italiana', categoria: 'COMESTIBLE', precio: 4.50, costo: 3.00, stock: 18, minimo: 5 },
  { id: 10, codigo: '0010', nombre: 'Cafe la jarrilla', categoria: 'COMESTIBLE', precio: 15.00, costo: 10.00, stock: 12, minimo: 5 },
  { id: 11, codigo: '0011', nombre: 'Sopa laky men vaso', categoria: 'COMESTIBLE', precio: 7.00, costo: 4.00, stock: 8, minimo: 5 },
  { id: 12, codigo: '0012', nombre: 'Papel nube blanca', categoria: 'HIGIENE', precio: 30.00, costo: 22.00, stock: 11, minimo: 4 },
  { id: 13, codigo: '0013', nombre: 'Mayonesa 4 oz', categoria: 'COMESTIBLE', precio: 9.00, costo: 6.00, stock: 16, minimo: 5 },
  { id: 14, codigo: '0014', nombre: 'Salsa dulce 8 oz', categoria: 'COMESTIBLE', precio: 10.00, costo: 7.00, stock: 19, minimo: 5 }
]

export const initialSales = [
  { id: 1, fecha: '2026-04-11', total: 81.50, metodoPago: 'Efectivo', factura: 'FEL-0001', productos: 3 },
  { id: 2, fecha: '2026-04-11', total: 126.00, metodoPago: 'Tarjeta', factura: 'FEL-0002', productos: 5 }
]
